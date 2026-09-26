"""End-to-end tests for the QueryPreprocessingPipeline.

All external components (XGBoost, Fireworks API, ChromaDB) are mocked.
No model files, API keys or running services are required.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import numpy as np
import pytest
from pydantic import BaseModel

from src.rag.fireworks.llm import LLMError
from src.rag.fireworks.reranker import RerankResult
from src.rag.preprocessing.fusion import CandidateChunk, FusionConfig, FusionRouter
from src.rag.preprocessing.pipeline import QueryPreprocessingPipeline
from src.rag.preprocessing.schemas import RoutingMethod, StageStatus

# Shared constants
DEPARTMENTS = [
    "AI and Machine Learning",
    "Cloud Platform and DevOps",
    "Customer Support",
    "Finance",
    "Human Resources",
    "IT Operations",
    "Information Security",
    "Legal and Compliance",
    "Product Management",
    "Quality Engineering",
    "Sales",
    "Software Engineering",
    "UX and Design",
]

_GOOD_DOCUMENT = (
    "To request access to the production Kubernetes cluster, employees follow the standard "
    "privileged access request workflow. The request is made through the IT portal. "
    "The manager and cluster owner must both approve. Access is provisioned with "
    "least-privilege role bindings and reviewed quarterly."
)


# ---------------------------------------------------------------------------
# Test helpers
# ---------------------------------------------------------------------------


def _proba_row(dept: str, confidence: float = 0.8) -> list[float]:
    row = [0.0] * len(DEPARTMENTS)
    idx = DEPARTMENTS.index(dept)
    row[idx] = confidence
    remainder = (1.0 - confidence) / (len(DEPARTMENTS) - 1)
    for i in range(len(DEPARTMENTS)):
        if i != idx:
            row[i] = remainder
    return row


def _make_xgb_router(dept: str, confidence: float = 0.8) -> MagicMock:
    router = MagicMock()
    router.departments = DEPARTMENTS
    router.predict_proba.return_value = np.array([_proba_row(dept, confidence)])
    return router


def _make_reranker(
    scored: list[tuple[CandidateChunk, float]] | None = None,
) -> MagicMock:
    reranker = MagicMock()
    results = [
        RerankResult(item=c, index=i, relevance_score=s) for i, (c, s) in enumerate(scored or [])
    ]
    reranker.rerank = AsyncMock(return_value=results)
    return reranker


def _make_llm(
    expansion_queries: list[str] | None = None,
    hyde_document: str | None = None,
    expansion_error: Exception | None = None,
    hyde_error: Exception | None = None,
) -> MagicMock:
    """Return a mock LLM whose complete_json alternates between expansion and HyDE responses."""

    call_count = 0

    class _ExpR(BaseModel):
        queries: list[str]

    class _HyDE(BaseModel):
        document: str

    async def _complete_json(system, user, schema, **kwargs):
        nonlocal call_count
        call_count += 1
        # We can't easily tell the two calls apart by schema at runtime in tests,
        # so we alternate: first call = expansion, second = HyDE.
        # In practice asyncio.gather may fire them in any order but for the
        # deterministic mock we rely on the per-function mock below.
        raise NotImplementedError

    llm = MagicMock()

    async def _side_effect(system, user, schema, **kwargs):
        # Detect call by checking which schema is expected
        if schema.__name__ == "_ExpansionResponse" or "queries" in schema.model_fields:
            if expansion_error:
                raise expansion_error
            return _ExpR(queries=expansion_queries or ["expanded q1", "expanded q2"])
        # HyDE
        if hyde_error:
            raise hyde_error
        return _HyDE(document=hyde_document or _GOOD_DOCUMENT)

    llm.complete_json = AsyncMock(side_effect=_side_effect)
    return llm


def _make_embeddings(dim: int = 356) -> MagicMock:
    emb = MagicMock()
    emb.embed_query = AsyncMock(return_value=np.zeros(dim, dtype=np.float32))
    emb.embed_documents = AsyncMock(return_value=np.random.rand(1, dim).astype(np.float32))
    return emb


def _make_pipeline(
    dept: str = "Cloud Platform and DevOps",
    candidates: list[CandidateChunk] | None = None,
    expansion_queries: list[str] | None = None,
    hyde_document: str | None = None,
    expansion_error: Exception | None = None,
    hyde_error: Exception | None = None,
) -> QueryPreprocessingPipeline:
    xgb = _make_xgb_router(dept)
    reranker = _make_reranker([(c, 0.9) for c in (candidates or [])])
    fusion = FusionRouter(xgb, reranker, FusionConfig(max_alternatives=2))
    llm = _make_llm(expansion_queries, hyde_document, expansion_error, hyde_error)
    embeddings = _make_embeddings()

    return QueryPreprocessingPipeline(
        fusion_router=fusion,
        llm=llm,
        embeddings=embeddings,
        chroma_collection=None,  # no ChromaDB in unit tests
        expansion_count=3,
        hyde_enabled=True,
    )


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_pipeline_full_happy_path():
    pipeline = _make_pipeline(
        dept="Cloud Platform and DevOps",
        expansion_queries=["query 1", "query 2", "query 3"],
        hyde_document=_GOOD_DOCUMENT,
    )
    result = await pipeline.process("How do I access K8s prod?")

    assert result.original_query == "How do I access K8s prod?"
    assert result.routing.primary_department == "Cloud Platform and DevOps"
    assert result.routing.routing_method == RoutingMethod.XGBOOST_ONLY  # no candidates
    assert result.query_expansion.status == StageStatus.COMPLETED
    assert len(result.query_expansion.queries) >= 1
    assert result.hyde.status == StageStatus.COMPLETED
    assert result.hyde.hypothetical_document != ""


@pytest.mark.asyncio
async def test_pipeline_whitespace_query_raises():
    pipeline = _make_pipeline()
    with pytest.raises(ValueError, match="empty"):
        await pipeline.process("   ")


@pytest.mark.asyncio
async def test_pipeline_query_is_stripped():
    pipeline = _make_pipeline()
    result = await pipeline.process("  How do I submit expenses?  ")
    assert result.original_query == "How do I submit expenses?"


# ---------------------------------------------------------------------------
# Partial failure: expansion fails, HyDE succeeds
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_pipeline_expansion_fails_hyde_succeeds():
    pipeline = _make_pipeline(
        expansion_error=LLMError("expansion timeout"),
        hyde_document=_GOOD_DOCUMENT,
    )
    result = await pipeline.process("VPN setup steps?")

    assert result.query_expansion.status == StageStatus.FAILED
    assert result.hyde.status == StageStatus.COMPLETED
    # Routing must still work
    assert result.routing.primary_department != ""


@pytest.mark.asyncio
async def test_pipeline_hyde_fails_expansion_succeeds():
    pipeline = _make_pipeline(
        expansion_queries=["q1", "q2"],
        hyde_error=LLMError("hyde model error"),
    )
    result = await pipeline.process("leave policy")

    assert result.query_expansion.status == StageStatus.COMPLETED
    assert result.hyde.status == StageStatus.FAILED
    assert result.query_expansion.queries == ["q1", "q2"]


# ---------------------------------------------------------------------------
# HyDE disabled
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_pipeline_hyde_disabled_skips_hyde():
    xgb = _make_xgb_router("Finance")
    reranker = _make_reranker()
    fusion = FusionRouter(xgb, reranker)
    llm = _make_llm(expansion_queries=["q1"])
    embeddings = _make_embeddings()

    pipeline = QueryPreprocessingPipeline(
        fusion_router=fusion,
        llm=llm,
        embeddings=embeddings,
        chroma_collection=None,
        expansion_count=3,
        hyde_enabled=False,
    )
    result = await pipeline.process("How are expenses processed?")

    assert result.hyde.status == StageStatus.SKIPPED


# ---------------------------------------------------------------------------
# to_api_dict excludes embedding
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_pipeline_api_dict_excludes_embedding():
    pipeline = _make_pipeline(hyde_document=_GOOD_DOCUMENT)
    result = await pipeline.process("query")
    api = result.to_api_dict()

    assert "embedding" not in api["hyde"]
    assert "hypothetical_document" in api["hyde"]
    assert "routing" in api
    assert "query_expansion" in api


# ---------------------------------------------------------------------------
# Concurrent execution
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_expansion_and_hyde_run_concurrently():
    """Both tasks must be awaited; gather ensures concurrency (smoke test)."""
    import asyncio

    call_order: list[str] = []

    class _ExpR(BaseModel):
        queries: list[str]

    class _HyDE(BaseModel):
        document: str

    async def _slow_llm(system, user, schema, **_):
        await asyncio.sleep(0.01)
        if "queries" in schema.model_fields:
            call_order.append("expansion")
            return _ExpR(queries=["q1"])
        call_order.append("hyde")
        return _HyDE(document=_GOOD_DOCUMENT)

    xgb = _make_xgb_router("Human Resources")
    reranker = _make_reranker()
    fusion = FusionRouter(xgb, reranker)
    llm = MagicMock()
    llm.complete_json = AsyncMock(side_effect=_slow_llm)
    embeddings = _make_embeddings()

    pipeline = QueryPreprocessingPipeline(
        fusion_router=fusion,
        llm=llm,
        embeddings=embeddings,
        chroma_collection=None,
        expansion_count=1,
        hyde_enabled=True,
    )
    result = await pipeline.process("onboarding documents")

    # Both stages must have been called
    assert set(call_order) == {"expansion", "hyde"}
    assert result.query_expansion.status == StageStatus.COMPLETED
    assert result.hyde.status == StageStatus.COMPLETED
