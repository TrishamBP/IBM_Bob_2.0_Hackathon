"""RAG HTTP endpoints.

``POST /api/v1/rag/upload`` follows the frontend contract (``frontend/src/lib/api/
documents.ts``): request-level problems return a non-2xx status with a *string*
``detail``, while per-file problems return 200 with an ``errors`` list so partially
successful batches are reported file-by-file.
"""

from __future__ import annotations

import logging
from typing import Annotated

from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile, status

from src.config import get_settings
from src.rag.departments import DEPARTMENTS
from src.rag.documents import build_document_view
from src.rag.fireworks import FireworksError
from src.rag.ingestion import FileIngestResult, StageResult, safe_filename
from src.rag.router.router import RouterCompatibilityError
from src.rag.schemas import (
    DocumentView,
    FileError,
    FileResult,
    IngestionStages,
    RouteRequest,
    RouteResponse,
    StageReport,
    UploadResponse,
)
from src.rag.service import RagServices

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/rag", tags=["rag"])

READ_CHUNK_BYTES = 1024 * 1024


def _services(request: Request) -> RagServices:
    services: RagServices | None = getattr(request.app.state, "rag", None)
    if services is None:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            "Document ingestion is unavailable: the embedding service is not configured",
        )
    return services


async def _read_limited(upload: UploadFile, limit: int) -> bytes | None:
    """Read an upload fully, or return ``None`` as soon as it exceeds ``limit`` bytes."""
    if upload.size is not None and upload.size > limit:
        return None
    parts: list[bytes] = []
    total = 0
    while chunk := await upload.read(READ_CHUNK_BYTES):
        total += len(chunk)
        if total > limit:
            return None
        parts.append(chunk)
    return b"".join(parts)


def _report(stage: StageResult) -> StageReport:
    return StageReport(status=stage.status, detail=stage.detail)


@router.post("/upload", response_model=UploadResponse)
async def upload_documents(
    request: Request,
    department: Annotated[str | None, Form()] = None,
    files: Annotated[list[UploadFile] | None, File()] = None,
) -> UploadResponse:
    settings = get_settings()
    # Fields are validated here (not by FastAPI) so errors are a plain string ``detail``.
    if not department or department not in DEPARTMENTS:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"A valid department is required. Choose one of: {', '.join(DEPARTMENTS)}",
        )
    if not files:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No files were uploaded")
    if len(files) > settings.upload_max_files:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"Too many files: {len(files)} (maximum {settings.upload_max_files} per request)",
        )
    services = _services(request)
    max_mb = settings.upload_max_file_bytes // (1024 * 1024)

    results: list[FileIngestResult] = []
    # Files are processed one at a time to bound memory; within a file, DeepSeek and
    # embedding requests run concurrently up to their configured limits.
    for upload in files:
        name = safe_filename(upload.filename or "")
        try:
            content = await _read_limited(upload, settings.upload_max_file_bytes)
        finally:
            await upload.close()
        if content is None:
            rejected = FileIngestResult(
                name, "failed", f"File exceeds the {max_mb} MB size limit", department
            )
            rejected.stages["validation"] = StageResult("failed", rejected.message)
            results.append(rejected)
            continue
        results.append(await services.ingestion.ingest_file(department, name, content))
        del content

    ok = [r for r in results if r.ok]
    failed = [r for r in results if not r.ok]
    if not failed:
        message = f"{len(ok)} file(s) ingested into {department}"
    elif not ok:
        message = f"All {len(failed)} file(s) failed"
    else:
        message = f"{len(ok)} file(s) ingested, {len(failed)} failed"
    return UploadResponse(
        uploaded=len(ok),
        errors=[FileError(filename=r.filename, message=r.message) for r in failed],
        message=message,
        department=department,
        results=[
            FileResult(
                filename=r.filename,
                department=r.department,
                status=r.status,
                message=r.message,
                document_id=r.document_id,
                document_version=r.document_version,
                chunks=r.chunks,
                segmentation_method=r.segmentation_method,
                stages=IngestionStages(**{k: _report(v) for k, v in r.stages.items()}),
                error=None if r.ok else r.message,
            )
            for r in results
        ],
    )


@router.post("/route", response_model=RouteResponse)
async def route_query(request: Request, body: RouteRequest) -> RouteResponse:
    """Fused department routing (XGBoost prior + reranked retrieval evidence)."""
    services = _services(request)
    if services.fusion is None:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            "Fusion routing is unavailable: FIREWORKS_RERANKER_MODEL is not configured",
        )
    try:
        result = await services.fusion.route(body.query)
    except ValueError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc)) from exc
    except (FileNotFoundError, RouterCompatibilityError) as exc:
        logger.error("Department router unavailable: %s", exc)
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE, "Department router model is unavailable"
        ) from exc
    except FireworksError as exc:
        logger.warning("Fireworks error during routing: %s", exc)
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, "Embedding service error") from exc
    return RouteResponse.model_validate(result)


@router.get("/documents/{document_id}", response_model=DocumentView)
async def get_document(request: Request, document_id: str) -> DocumentView:
    """The current version of a document, rebuilt from its chunks (citation viewer)."""
    services = _services(request)
    chunks = await services.store.get_document_chunks(document_id)
    if not chunks:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "This document is no longer available. It may have been removed or replaced.",
        )
    return build_document_view(document_id, chunks)
