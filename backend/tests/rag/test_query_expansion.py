"""Unit tests for query_expansion.py.

Fireworks LLM calls are mocked — no API credentials required.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.rag.fireworks.llm import LLMError
from src.rag.preprocessing.query_expansion import expand_query
from src.rag.preprocessing.schemas import StageStatus


def _mock_llm(queries: list[str] | None = None, raise_exc: Exception | None = None) -> MagicMock:
    llm = MagicMock()
    if raise_exc is not None:
        llm.complete_json = AsyncMock(side_effect=raise_exc)
    else:
        from pydantic import BaseModel

        class _R(BaseModel):
            queries: list[str]

        llm.complete_json = AsyncMock(return_value=_R(queries=queries or []))
    return llm


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_expansion_returns_n_queries():
    q = ["What is the K8s access process?", "How do I get K8s access?", "K8s prod permissions?"]
    llm = _mock_llm(queries=q)
    result = await expand_query(llm, "K8s access", "Cloud Platform and DevOps", n=3)

    assert result.status == StageStatus.COMPLETED
    assert len(result.queries) == 3
    assert result.error is None


@pytest.mark.asyncio
async def test_expansion_deduplicates_queries():
    q = ["duplicate query", "  duplicate query  ", "unique query"]
    llm = _mock_llm(queries=q)
    result = await expand_query(llm, "something", "IT Operations", n=3)

    assert len(result.queries) == 2
    assert result.queries[0] == "duplicate query"
    assert result.queries[1] == "unique query"


@pytest.mark.asyncio
async def test_expansion_removes_empty_strings():
    q = ["", "  ", "valid query"]
    llm = _mock_llm(queries=q)
    result = await expand_query(llm, "test", "Human Resources", n=3)

    assert result.queries == ["valid query"]


@pytest.mark.asyncio
async def test_expansion_passes_alternatives_in_prompt():
    llm = _mock_llm(queries=["expanded query"])
    await expand_query(
        llm,
        "VPN setup",
        "IT Operations",
        alternative_departments=["Information Security"],
        n=1,
    )
    call_args = llm.complete_json.call_args
    user_prompt: str = call_args[0][1]
    assert "Information Security" in user_prompt


# ---------------------------------------------------------------------------
# Failure modes
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_expansion_handles_llm_error():
    llm = _mock_llm(raise_exc=LLMError("model timeout"))
    result = await expand_query(llm, "valid query", "Finance", n=3)

    assert result.status == StageStatus.FAILED
    assert "model timeout" in result.error
    assert result.queries == []


@pytest.mark.asyncio
async def test_expansion_handles_unexpected_exception():
    llm = _mock_llm(raise_exc=RuntimeError("connection reset"))
    result = await expand_query(llm, "valid query", "Sales", n=3)

    assert result.status == StageStatus.FAILED
    assert result.queries == []


@pytest.mark.asyncio
async def test_expansion_empty_query_returns_failed():
    llm = _mock_llm(queries=["irrelevant"])
    result = await expand_query(llm, "   ", "Legal and Compliance", n=3)

    assert result.status == StageStatus.FAILED
    assert result.queries == []


@pytest.mark.asyncio
async def test_expansion_llm_returns_empty_list():
    llm = _mock_llm(queries=[])
    result = await expand_query(llm, "valid query", "Product Management", n=3)

    assert result.status == StageStatus.FAILED
    assert "empty" in result.error.lower()


# ---------------------------------------------------------------------------
# Prompt content checks
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_expansion_prompt_includes_department():
    llm = _mock_llm(queries=["q1"])
    await expand_query(llm, "onboarding steps", "Human Resources", n=2)
    system_prompt: str = llm.complete_json.call_args[0][0]
    user_prompt: str = llm.complete_json.call_args[0][1]
    assert "Human Resources" in user_prompt or "Human Resources" in system_prompt


@pytest.mark.asyncio
async def test_expansion_prompt_includes_original_query():
    llm = _mock_llm(queries=["q1"])
    await expand_query(llm, "how do I reset my password", "IT Operations")
    user_prompt: str = llm.complete_json.call_args[0][1]
    assert "reset my password" in user_prompt
