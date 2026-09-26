"""Pydantic request/response models for the RAG API."""

from typing import Any, Literal

from pydantic import BaseModel, Field


class FileError(BaseModel):
    filename: str
    message: str


StageStatus = Literal["succeeded", "fallback", "skipped", "failed", "not_run"]


class StageReport(BaseModel):
    status: StageStatus = "not_run"
    detail: str | None = None


class IngestionStages(BaseModel):
    """Per-stage outcome. ``fallback`` = completed without DeepSeek (source metadata only /
    structural segmentation); ``skipped`` = not needed (e.g. unchanged document)."""

    validation: StageReport = Field(default_factory=StageReport)
    extraction: StageReport = Field(default_factory=StageReport)
    metadata: StageReport = Field(default_factory=StageReport)
    chunking: StageReport = Field(default_factory=StageReport)
    embedding: StageReport = Field(default_factory=StageReport)
    persistence: StageReport = Field(default_factory=StageReport)


class FileResult(BaseModel):
    filename: str
    department: str | None = None
    status: Literal["ingested", "unchanged", "failed"]
    message: str
    document_id: str | None = None
    document_version: str | None = None
    chunks: int = 0
    segmentation_method: Literal["llm", "structural", "mixed"] | None = None
    stages: IngestionStages = Field(default_factory=IngestionStages)
    error: str | None = None


class UploadResponse(BaseModel):
    """Matches the frontend's ``UploadBatchResponse`` (``uploaded``/``errors``/``message``)."""

    uploaded: int
    errors: list[FileError] = Field(default_factory=list)
    message: str
    department: str
    results: list[FileResult] = Field(default_factory=list)


class RouteRequest(BaseModel):
    query: str = Field(min_length=1, max_length=2000)


class DepartmentScore(BaseModel):
    department: str
    xgboost_score: float
    reranker_score: float | None
    raw_reranker_score: float | None
    final_score: float
    has_evidence: bool


class RetrievedChunk(BaseModel):
    chunk_id: str
    department: str | None
    title: str | None
    source_filename: str | None
    section_heading: str | None
    page_start: int | None
    reranker_score: float
    vector_similarity: float
    text: str
    metadata: dict[str, Any]


class RouteResponse(BaseModel):
    query: str
    primary_department: str
    selected_departments: list[str]
    predictions: list[DepartmentScore]
    retrieved_chunks: list[RetrievedChunk]
    diagnostics: dict[str, Any]
