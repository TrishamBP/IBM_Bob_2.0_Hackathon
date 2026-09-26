"""Unit tests for hyde.py.

Fireworks LLM and embedding calls are mocked — no API credentials required.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import numpy as np
import pytest

from src.rag.fireworks.llm import LLMError
from src.rag.preprocessing.hyde import _MIN_DOC_WORDS, generate_hyde
from src.rag.preprocessing.schemas import StageStatus

_GOOD_DOC = (
    "To request access to the production Kubernetes cluster, employees should follow the "
    "standard privileged access request workflow. The request is initiated through the IT "
    "Service Management portal, where the employee specifies the required namespace and "
    "role. The manager and the cluster owner must both approve the request. Once approved, "
    "IT Operations provisions the role binding using least-privilege principles. The "
    "employee should verify connectivity using the kubectl CLI after receiving credentials. "
    "Any issues should be reported to the IT helpdesk. Access is reviewed quarterly and "
    "revoked if no longer required."
)


def _mock_llm(document: str | None = None, raise_exc: Exception | None = None) -> MagicMock:
    from pydantic import BaseModel

    class _R(BaseModel):
        document: str

    llm = MagicMock()
    if raise_exc is not None:
        llm.complete_json = AsyncMock(side_effect=raise_exc)
    else:
        llm.complete_json = AsyncMock(return_value=_R(document=document or ""))
    return llm


def _mock_embeddings(dim: int = 356) -> MagicMock:
    emb = MagicMock()
    vector = np.random.rand(1, dim).astype(np.float32)
    emb.embed_documents = AsyncMock(return_value=vector)
    return emb


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_hyde_returns_document_and_embedding():
    llm = _mock_llm(document=_GOOD_DOC)
    embeddings = _mock_embeddings(dim=356)
    result = await generate_hyde(llm, embeddings, "K8s access", "Cloud Platform and DevOps")

    assert result.status == StageStatus.COMPLETED
    assert result.hypothetical_document == _GOOD_DOC
    assert result.embedding_dimensions == 356
    assert len(result.embedding) == 356
    assert result.error is None


@pytest.mark.asyncio
async def test_hyde_embedding_dimensions_set_correctly():
    llm = _mock_llm(document=_GOOD_DOC)
    embeddings = _mock_embeddings(dim=356)
    result = await generate_hyde(llm, embeddings, "leave policy", "Human Resources")

    assert result.embedding_dimensions == len(result.embedding)


@pytest.mark.asyncio
async def test_hyde_embedding_array_conversion():
    llm = _mock_llm(document=_GOOD_DOC)
    embeddings = _mock_embeddings(dim=356)
    result = await generate_hyde(llm, embeddings, "VPN setup", "IT Operations")

    arr = result.embedding_as_array()
    assert arr.dtype == np.float32
    assert arr.shape == (356,)


# ---------------------------------------------------------------------------
# LLM failure modes
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_hyde_handles_llm_error():
    llm = _mock_llm(raise_exc=LLMError("rate limit"))
    embeddings = _mock_embeddings()
    result = await generate_hyde(llm, embeddings, "query", "Finance")

    assert result.status == StageStatus.FAILED
    assert "rate limit" in result.error


@pytest.mark.asyncio
async def test_hyde_handles_unexpected_llm_exception():
    llm = _mock_llm(raise_exc=ConnectionError("network unavailable"))
    embeddings = _mock_embeddings()
    result = await generate_hyde(llm, embeddings, "query", "Legal and Compliance")

    assert result.status == StageStatus.FAILED
    assert result.hypothetical_document == ""


@pytest.mark.asyncio
async def test_hyde_empty_document_returns_failed():
    llm = _mock_llm(document="")
    embeddings = _mock_embeddings()
    result = await generate_hyde(llm, embeddings, "query", "Sales")

    assert result.status == StageStatus.FAILED
    assert "empty" in result.error.lower()


@pytest.mark.asyncio
async def test_hyde_too_short_document_returns_failed():
    short_doc = " ".join(["word"] * (_MIN_DOC_WORDS - 1))
    llm = _mock_llm(document=short_doc)
    embeddings = _mock_embeddings()
    result = await generate_hyde(llm, embeddings, "query", "Quality Engineering")

    assert result.status == StageStatus.FAILED
    assert "short" in result.error.lower()


# ---------------------------------------------------------------------------
# Embedding failure
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_hyde_embedding_failure_preserves_document():
    """If embedding fails, the document text is still returned."""
    llm = _mock_llm(document=_GOOD_DOC)
    embeddings = MagicMock()
    embeddings.embed_documents = AsyncMock(side_effect=RuntimeError("embedding service down"))
    result = await generate_hyde(llm, embeddings, "query", "Software Engineering")

    assert result.status == StageStatus.FAILED
    assert result.hypothetical_document == _GOOD_DOC
    assert result.embedding == []
    assert "embedding" in result.error.lower()


# ---------------------------------------------------------------------------
# Empty query
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_hyde_empty_query_returns_failed():
    llm = _mock_llm(document=_GOOD_DOC)
    embeddings = _mock_embeddings()
    result = await generate_hyde(llm, embeddings, "  ", "IT Operations")

    assert result.status == StageStatus.FAILED
    # LLM should not be called at all
    llm.complete_json.assert_not_called()
