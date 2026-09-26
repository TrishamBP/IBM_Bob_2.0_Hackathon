"""Semantic document ingestion.

extract structure -> DeepSeek metadata + semantic sections -> hierarchical chunks ->
Qwen3 embeddings (contextualized text) -> ChromaDB.

Only extracted text, embeddings and metadata are stored. Uploaded files are held in
memory for the duration of the request and never written to permanent storage.

Identifiers are deterministic so re-uploading is idempotent:

- ``document_id`` = hash of (HR department, lower-cased filename): the same file
  uploaded to the same department replaces its previous version.
- ``document_version`` = hash of the file bytes plus the pipeline configuration
  (prompts, models, chunk limits). Re-uploading identical content is a no-op
  (``unchanged``) unless the stored version was built with a fallback while DeepSeek
  is now available, in which case it is reprocessed.
- chunk id = ``{document_id}-{hash(version, chunk index, content)}``.

The department is the one selected by HR; DeepSeek never overrides it and the XGBoost
router is intentionally not used to classify documents.
"""

from __future__ import annotations

import asyncio
import hashlib
import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import PureWindowsPath
from typing import Any, Literal

from src.chroma.client import ChromaStore, PersistenceError
from src.rag.departments import DEPARTMENTS
from src.rag.extraction import ExtractedDocument, ExtractionError, extract_document
from src.rag.fireworks import FireworksEmbeddings, FireworksError
from src.rag.semantic.chunks import SemanticChunk, build_chunks, contextualize
from src.rag.semantic.metadata import MetadataGenerator
from src.rag.semantic.prompts import PROMPT_VERSION
from src.rag.semantic.schemas import DocumentMetadata
from src.rag.semantic.segmentation import (
    SegmentationResult,
    SemanticSegmenter,
    structural_sections,
)
from src.rag.semantic.serialization import flatten_metadata

logger = logging.getLogger(__name__)

PIPELINE_VERSION = f"semantic-v1/prompts-{PROMPT_VERSION}"
STAGES = ("validation", "extraction", "metadata", "chunking", "embedding", "persistence")

Status = Literal["ingested", "unchanged", "failed"]
StageStatus = Literal["succeeded", "fallback", "skipped", "failed", "not_run"]


@dataclass
class StageResult:
    status: StageStatus = "not_run"
    detail: str | None = None


def new_stages() -> dict[str, StageResult]:
    return {name: StageResult() for name in STAGES}


@dataclass
class FileIngestResult:
    filename: str
    status: Status
    message: str
    department: str | None = None
    document_id: str | None = None
    document_version: str | None = None
    chunks: int = 0
    segmentation_method: str | None = None
    stages: dict[str, StageResult] = field(default_factory=new_stages)

    @property
    def ok(self) -> bool:
        return self.status != "failed"


def safe_filename(filename: str) -> str:
    """Strip any client-supplied directory components (handles both / and \\)."""
    name = PureWindowsPath(filename or "").name.strip()
    return name or "untitled"


def make_document_id(department: str, filename: str) -> str:
    key = f"{department}|{safe_filename(filename).lower()}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:32]


def make_chunk_id(document_id: str, version: str, index: int, content: str) -> str:
    digest = hashlib.sha256(f"{version}|{index}|{content}".encode()).hexdigest()[:16]
    return f"{document_id}-{digest}"


class IngestionService:
    def __init__(
        self,
        store: ChromaStore,
        embedder: FireworksEmbeddings,
        *,
        metadata: MetadataGenerator | None = None,
        segmenter: SemanticSegmenter | None = None,
        max_chunk_tokens: int = 450,
        overlap_tokens: int = 40,
        llm_model: str | None = None,
    ) -> None:
        if not 0 <= overlap_tokens < max_chunk_tokens // 2:
            raise ValueError("overlap_tokens must be >= 0 and less than half of max_tokens")
        self.store = store
        self.embedder = embedder
        self.metadata = metadata or MetadataGenerator(None)
        self.segmenter = segmenter or SemanticSegmenter(None)
        self.max_chunk_tokens = max_chunk_tokens
        self.overlap_tokens = overlap_tokens
        self.llm_model = llm_model if self.segmenter.llm is not None else None
        self._config_signature = "|".join(
            str(part)
            for part in (
                PIPELINE_VERSION,
                embedder.model,
                embedder.dimensions,
                max_chunk_tokens,
                overlap_tokens,
                self.llm_model or "no-llm",
            )
        ).encode()

    @property
    def llm_enabled(self) -> bool:
        return self.segmenter.llm is not None

    def make_version(self, content: bytes) -> str:
        return hashlib.sha256(content + b"\x00" + self._config_signature).hexdigest()[:16]

    async def ingest_file(self, department: str, filename: str, content: bytes) -> FileIngestResult:
        """Ingest one file. Never raises for per-file problems; returns a failed result."""
        name = safe_filename(filename)
        result = FileIngestResult(name, "failed", "", department)
        stages = result.stages
        if department not in DEPARTMENTS:
            stages["validation"] = StageResult("failed", f"Unknown department '{department}'")
            result.message = stages["validation"].detail or ""
            return result
        stages["validation"] = StageResult("succeeded")
        result.document_id = document_id = make_document_id(department, name)
        result.document_version = version = self.make_version(content)
        stage = "extraction"
        try:
            existing = await self.store.get_document_info(document_id)
            if (
                existing
                and existing.get("document_version") == version
                and not (self.llm_enabled and existing.get("document_segmentation_method") != "llm")
            ):
                result.status, result.message = "unchanged", "Identical document already ingested"
                result.chunks = await self.store.count_document_chunks(document_id, version)
                result.segmentation_method = existing.get("document_segmentation_method")
                for name_ in STAGES[1:]:
                    stages[name_] = StageResult("skipped", "unchanged")
                return result

            doc = await extract_document(name, content)
            stages["extraction"] = StageResult(
                "succeeded", f"{len(doc.blocks)} blocks, {len(doc.outline())} headings"
            )

            stage = "metadata"
            doc_meta, segmentation = await asyncio.gather(
                self.metadata.generate(doc, department, name),
                self.segmenter.segment(doc, title=doc.title, department=department),
            )
            stages["metadata"] = StageResult(
                doc_meta.llm_status,
                doc_meta.llm_error
                or ("DeepSeek metadata validated" if doc_meta.llm_status == "succeeded" else None),
            )

            stage = "chunking"
            chunks, segmentation = await self._build_chunks(doc, segmentation)
            result.segmentation_method = segmentation.method
            detail = (
                f"{len(chunks)} chunks from {len(segmentation.sections)} sections "
                f"({segmentation.method})"
            )
            if segmentation.fallback_reasons:
                detail += f"; fallback: {segmentation.fallback_reasons[0]}"
            stages["chunking"] = StageResult(
                "succeeded" if segmentation.method == "llm" else "fallback", detail
            )

            stage = "embedding"
            texts = [contextualize(c, title=doc_meta.title, department=department) for c in chunks]
            embeddings = await self.embedder.embed_documents(texts)
            stages["embedding"] = StageResult(
                "succeeded", f"{embeddings.shape[0]} x {embeddings.shape[1]} dimensions"
            )

            stage = "persistence"
            ids = [make_chunk_id(document_id, version, c.index, c.content) for c in chunks]
            metadatas = self._chunk_metadata(
                doc, doc_meta, segmentation, chunks, texts, ids, name, version, document_id
            )
            stored = await self.store.replace_document(
                document_id, version, ids, [c.content for c in chunks], embeddings, metadatas
            )
            stages["persistence"] = StageResult("succeeded", f"{stored} chunks stored")
        except ExtractionError as exc:
            return self._fail(result, stage, str(exc))
        except FireworksError as exc:
            logger.warning("Fireworks error during %s for %s: %s", stage, name, exc)
            return self._fail(result, stage, "Embedding service error; please retry later")
        except PersistenceError as exc:
            return self._fail(result, stage, str(exc))
        except Exception:
            logger.exception("Unexpected ingestion failure for %s", name)
            return self._fail(result, stage, "Internal error while ingesting document")

        result.status, result.chunks = "ingested", stored
        result.message = f"Ingested {stored} chunks ({segmentation.method} segmentation)"
        return result

    @staticmethod
    def _fail(result: FileIngestResult, stage: str, message: str) -> FileIngestResult:
        result.stages[stage] = StageResult("failed", message)
        result.status, result.message = "failed", message
        return result

    async def _build_chunks(
        self, doc: ExtractedDocument, segmentation: SegmentationResult
    ) -> tuple[list[SemanticChunk], SegmentationResult]:
        build = lambda sections: build_chunks(  # noqa: E731
            doc,
            sections,
            max_tokens=self.max_chunk_tokens,
            overlap_tokens=self.overlap_tokens,
        )
        try:
            return await asyncio.to_thread(build, segmentation.sections), segmentation
        except Exception as exc:  # defensive: sections are validated before this point
            if segmentation.method == "structural":
                raise
            logger.warning("LLM sections could not be chunked (%s); using structure", exc)
            fallback = SegmentationResult(
                structural_sections(doc.blocks, 0, len(doc.blocks) - 1),
                "structural",
                segmentation.windows,
                0,
                [*segmentation.fallback_reasons, f"chunk construction failed: {exc}"],
                segmentation.llm_attempts,
            )
            return await asyncio.to_thread(build, fallback.sections), fallback

    def _chunk_metadata(
        self,
        doc: ExtractedDocument,
        meta: DocumentMetadata,
        segmentation: SegmentationResult,
        chunks: list[SemanticChunk],
        texts: list[str],
        ids: list[str],
        filename: str,
        version: str,
        document_id: str,
    ) -> list[dict[str, Any]]:
        llm = meta.llm
        source = meta.source
        document_level: dict[str, Any] = {
            "document_id": document_id,
            "document_version": version,
            "title": meta.title,
            "title_source": meta.title_source,
            "department": meta.department,
            "department_source": "hr_selection",
            "source_filename": filename,
            "source_path": f"upload://{meta.department}/{filename}",
            "file_type": doc.file_type,
            "page_count": doc.page_count,
            "chunk_count": len(chunks),
            "document_segmentation_method": segmentation.method,
            "ingested_at": datetime.now(UTC).isoformat(),
            "pipeline_version": PIPELINE_VERSION,
            "embedding_model": self.embedder.model,
            "embedding_dimensions": self.embedder.dimensions,
            # Resolved facts, each with provenance ("source" or "llm_grounded")
            "doc_owner": meta.owner,
            "doc_owner_source": meta.owner_source,
            "doc_version": meta.version,
            "doc_version_source": meta.version_source,
            "doc_effective_date": meta.effective_date,
            "doc_effective_date_source": meta.effective_date_source,
            "doc_review_date": meta.review_date,
            "doc_review_date_source": meta.review_date_source,
            "metadata_conflicts": [c.model_dump() for c in meta.conflicts],
            # Read from the file itself
            "src_title": source.title,
            "src_owner": source.owner,
            "src_version": source.version,
            "src_effective_date": source.effective_date,
            "src_review_date": source.review_date,
            "src_department": source.department,
            "src_document_identifiers": source.document_identifiers,
            "src_keywords": source.keywords,
            "src_raw": source.raw,
            "src_outline": meta.source_outline,
            # Generated by DeepSeek
            "llm_metadata_status": meta.llm_status,
            "llm_model": self.llm_model,
        }
        if llm is not None:
            document_level.update(
                {
                    "llm_title": llm.title,
                    "llm_document_type": llm.document_type,
                    "llm_suggested_department": llm.suggested_primary_department,
                    "llm_secondary_departments": llm.secondary_departments,
                    "llm_relevant_roles": llm.relevant_roles,
                    "llm_topics": llm.topics,
                    "llm_keywords": llm.keywords,
                    "llm_summary": llm.summary,
                    "llm_intended_audience": llm.intended_audience,
                    "llm_purpose": llm.purpose,
                    "llm_major_sections": llm.major_sections,
                    "llm_referenced_systems": llm.referenced_systems,
                    "llm_referenced_products": llm.referenced_products,
                    "llm_referenced_policies": llm.referenced_policies,
                    "llm_document_identifiers": llm.document_identifiers,
                    "llm_ungrounded_fields": meta.ungrounded_fields,
                }
            )

        metadatas = []
        for chunk_id, chunk, text in zip(ids, chunks, texts, strict=True):
            values = {
                **document_level,
                "chunk_id": chunk_id,
                "chunk_index": chunk.index,
                "section_index": chunk.section_index,
                "section_part": chunk.part,
                "section_part_count": chunk.part_count,
                "section_title": chunk.section_title,
                "section_title_source": chunk.section_title_source,
                "section_heading": chunk.section_title or "",  # used by fusion routing
                "parent_section": chunk.parent_section,
                "heading_path": list(chunk.heading_path),
                "heading_path_text": " > ".join(chunk.heading_path),
                "heading_depth": len(chunk.heading_path),
                "page_start": chunk.page_start,
                "page_end": chunk.page_end,
                "block_start": chunk.block_start,
                "block_end": chunk.block_end,
                "char_start": chunk.char_start,
                "char_end": chunk.char_end,
                "block_kinds": list(chunk.block_kinds),
                "token_count": chunk.token_count,
                "segmentation_method": chunk.segmentation_method,
                "contextualized_text": text,
                "llm_section_title": chunk.llm_title,
                "llm_section_summary": chunk.summary,
                "llm_section_keywords": list(chunk.keywords) if chunk.keywords else None,
                "llm_section_roles": list(chunk.roles) if chunk.roles else None,
                "llm_section_context": chunk.context,
            }
            metadatas.append(flatten_metadata(values))
        return metadatas
