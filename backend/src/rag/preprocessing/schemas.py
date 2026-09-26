"""Pydantic schemas for the query preprocessing pipeline.

These models define the public contract of the pipeline.  Internal helpers
and LLM response parsers each have their own minimal schemas (defined inline
in their respective modules) to keep the surface area small.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Annotated

import numpy as np
from pydantic import BaseModel, Field, field_validator, model_validator

# ---------------------------------------------------------------------------
# Routing
# ---------------------------------------------------------------------------


class RoutingMethod(StrEnum):
    """How the routing decision was reached."""

    FUSION = "fusion"
    XGBOOST_ONLY = "xgboost_only"  # no ChromaDB candidates available
    FALLBACK = "fallback"  # both classifiers failed; result is unreliable


class RoutingResult(BaseModel):
    """Output of the fusion department-routing stage."""

    primary_department: str
    alternatives: list[str] = Field(default_factory=list)
    xgboost_score: Annotated[float, Field(ge=0.0, le=1.0)]
    reranker_score: Annotated[float, Field(ge=0.0, le=1.0)] = 0.0
    fusion_score: Annotated[float, Field(ge=0.0, le=1.0)]
    routing_method: RoutingMethod = RoutingMethod.FUSION
    error: str | None = None


# ---------------------------------------------------------------------------
# Stage status
# ---------------------------------------------------------------------------


class StageStatus(StrEnum):
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


# ---------------------------------------------------------------------------
# Query expansion
# ---------------------------------------------------------------------------


class QueryExpansionResult(BaseModel):
    """Output of the query-expansion stage."""

    queries: list[str] = Field(default_factory=list)
    status: StageStatus = StageStatus.COMPLETED
    error: str | None = None

    @field_validator("queries")
    @classmethod
    def deduplicate(cls, v: list[str]) -> list[str]:
        seen: set[str] = set()
        out: list[str] = []
        for q in v:
            stripped = q.strip()
            if stripped and stripped not in seen:
                seen.add(stripped)
                out.append(stripped)
        return out


# ---------------------------------------------------------------------------
# HyDE
# ---------------------------------------------------------------------------


class HyDEResult(BaseModel):
    """Output of the HyDE stage.

    The embedding is stored as a plain list for JSON-serialisability.
    Use ``include_embedding=True`` on the parent ``PreprocessingResult`` only
    when the embedding is actually needed downstream; omit it from API responses
    to avoid returning large float arrays.
    """

    hypothetical_document: str = ""
    embedding: list[float] = Field(default_factory=list, exclude=True)
    embedding_dimensions: int = 0
    status: StageStatus = StageStatus.COMPLETED
    error: str | None = None

    model_config = {"arbitrary_types_allowed": True}

    @model_validator(mode="after")
    def set_embedding_dimensions(self) -> HyDEResult:
        if self.embedding and self.embedding_dimensions == 0:
            self.embedding_dimensions = len(self.embedding)
        return self

    def embedding_as_array(self) -> np.ndarray:
        """Return the embedding as a float32 NumPy array."""
        return np.asarray(self.embedding, dtype=np.float32)


# ---------------------------------------------------------------------------
# Top-level preprocessing result
# ---------------------------------------------------------------------------


class PreprocessingResult(BaseModel):
    """Full output of :class:`QueryPreprocessingPipeline`."""

    original_query: str
    routing: RoutingResult
    query_expansion: QueryExpansionResult
    hyde: HyDEResult

    def to_api_dict(self) -> dict:
        """Serialise for an API response; the HyDE embedding vector is excluded."""
        return self.model_dump(
            exclude={"hyde": {"embedding"}},
        )


# ---------------------------------------------------------------------------
# API request / response wrappers
# ---------------------------------------------------------------------------


class PreprocessRequest(BaseModel):
    query: Annotated[str, Field(min_length=1, max_length=2000)]

    @field_validator("query")
    @classmethod
    def strip_query(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("query must not be empty or whitespace")
        return v
