"""Query expansion using DeepSeek V4.1 Flash.

Generates semantically diverse alternative search queries from the original
employee question, informed by the routed department.

The LLM is asked to return a ``{"queries": [...]}`` JSON object.  The result
is validated with Pydantic and deduplicated before being returned.  Any failure
is caught and surfaced as a ``QueryExpansionResult`` with ``status=FAILED``
rather than propagating an exception.
"""

from __future__ import annotations

import logging

from pydantic import BaseModel, Field

from src.rag.fireworks.llm import FireworksLLM, LLMError
from src.rag.preprocessing.prompts import (
    QUERY_EXPANSION_ALT_CONTEXT,
    QUERY_EXPANSION_CONVERSATION_CONTEXT,
    QUERY_EXPANSION_SYSTEM,
    QUERY_EXPANSION_USER,
)
from src.rag.preprocessing.schemas import QueryExpansionResult, StageStatus

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# LLM response schema (internal — not part of the public API)
# ---------------------------------------------------------------------------


class _ExpansionResponse(BaseModel):
    queries: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Query expansion function
# ---------------------------------------------------------------------------


async def expand_query(
    llm: FireworksLLM,
    query: str,
    department: str,
    *,
    alternative_departments: list[str] | None = None,
    n: int = 3,
    conversation_context: str | None = None,
    extra: dict | None = None,
) -> QueryExpansionResult:
    """Generate ``n`` alternative search queries using the LLM.

    Parameters
    ----------
    llm:
        Configured :class:`FireworksLLM` instance.
    query:
        The original employee question.
    department:
        Primary department determined by the fusion router.
    alternative_departments:
        Optional list of alternative departments to mention in the prompt.
    n:
        Number of expanded queries to generate.

    Returns
    -------
    :class:`QueryExpansionResult` — always succeeds; failures are captured as
    ``status=FAILED`` with an ``error`` field.
    """
    if not query.strip():
        return QueryExpansionResult(
            queries=[],
            status=StageStatus.FAILED,
            error="Query must not be empty",
        )

    alt_context = ""
    if alternative_departments:
        alt_context = QUERY_EXPANSION_ALT_CONTEXT.format(alts=", ".join(alternative_departments))

    system_prompt = QUERY_EXPANSION_SYSTEM.format(n=n)
    user_prompt = QUERY_EXPANSION_USER.format(
        query=query,
        department=department,
        alt_context=alt_context,
        n=n,
    )
    if conversation_context:
        user_prompt += QUERY_EXPANSION_CONVERSATION_CONTEXT.format(context=conversation_context)

    try:
        parsed: _ExpansionResponse = await llm.complete_json(
            system_prompt,
            user_prompt,
            _ExpansionResponse,
            extra=extra,
        )
    except LLMError as exc:
        logger.warning("Query expansion LLM error: %s", exc)
        return QueryExpansionResult(
            queries=[],
            status=StageStatus.FAILED,
            error=str(exc),
        )
    except Exception as exc:  # noqa: BLE001
        logger.exception("Unexpected error during query expansion: %s", exc)
        return QueryExpansionResult(
            queries=[],
            status=StageStatus.FAILED,
            error=f"Unexpected error: {exc}",
        )

    # Pydantic validator on QueryExpansionResult handles deduplication
    result = QueryExpansionResult(queries=parsed.queries[:n], status=StageStatus.COMPLETED)
    if not result.queries:
        logger.warning("Query expansion returned no valid queries for: %r", query)
        return QueryExpansionResult(
            queries=[],
            status=StageStatus.FAILED,
            error="LLM returned an empty queries list",
        )

    return result
