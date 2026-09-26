"""Fireworks reranking client (Qwen3 Reranker).

Scores are returned in [0, 1] by the API but are *not* calibrated probabilities: their
scale depends on the model, the task instruction and the passage length. Treat them as
relative relevance evidence.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass

from src.observability import observe, update_span
from src.rag.fireworks.client import FireworksClient, FireworksResponseError


@dataclass(frozen=True)
class RerankResult[T]:
    """A candidate with its reranker score; ``item`` is the caller's original object."""

    item: T
    index: int
    relevance_score: float


class FireworksReranker:
    def __init__(
        self,
        client: FireworksClient,
        model: str,
        *,
        url: str = "",
        max_candidates: int = 40,
        task: str = "",
        timeout: float | None = None,
    ) -> None:
        if not model:
            raise ValueError("A reranker model must be configured (FIREWORKS_RERANKER_MODEL)")
        if max_candidates < 1:
            raise ValueError("max_candidates must be >= 1")
        self.client = client
        self.model = model
        self.url = url or "rerank"
        self.max_candidates = max_candidates
        self.task = task
        self.timeout = timeout

    @observe("tool", name="rerank")
    async def rerank[T](
        self, query: str, items: Sequence[T], texts: Sequence[str]
    ) -> list[RerankResult[T]]:
        """Score ``texts`` against ``query``; results keep a reference to ``items[i]``.

        Only the first ``max_candidates`` items are sent. Results are sorted by
        descending relevance.
        """
        if len(items) != len(texts):
            raise ValueError("items and texts must have the same length")
        if not query.strip():
            raise ValueError("query must not be empty")
        items, texts = list(items)[: self.max_candidates], list(texts)[: self.max_candidates]
        if not items:
            return []

        payload = {
            "model": self.model,
            "query": query,
            "documents": texts,
            "top_n": len(texts),
            "return_documents": False,
        }
        if self.task:
            payload["task"] = self.task
        body = await self.client.post_json(self.url, payload, timeout=self.timeout)
        scores = parse_rerank_response(body, expected_count=len(texts))
        results = [RerankResult(items[i], i, score) for i, score in scores.items()]
        results.sort(key=lambda r: r.relevance_score, reverse=True)
        update_span(
            input=query,
            output=f"{len(results)} scored passages",
            model=self.model,
            candidates=len(texts),
            max_score=results[0].relevance_score if results else None,
        )
        return results


def parse_rerank_response(body: dict, *, expected_count: int) -> dict[int, float]:
    """Validate a ``/rerank`` response; returns ``{original_index: relevance_score}``."""
    data = body.get("data", body.get("results"))
    if not isinstance(data, list):
        raise FireworksResponseError("Rerank response is missing a 'data' list")
    scores: dict[int, float] = {}
    for item in data:
        if not isinstance(item, dict):
            raise FireworksResponseError("Rerank result is not an object")
        index, score = item.get("index"), item.get("relevance_score")
        if not isinstance(index, int) or not 0 <= index < expected_count:
            raise FireworksResponseError(f"Rerank result has invalid index {index!r}")
        if index in scores:
            raise FireworksResponseError(f"Duplicate rerank index {index}")
        if not isinstance(score, int | float) or not math.isfinite(score):
            raise FireworksResponseError(f"Rerank result {index} has invalid score {score!r}")
        scores[index] = float(score)
    if len(scores) != expected_count:
        raise FireworksResponseError(
            f"Rerank response scored {len(scores)} of {expected_count} documents"
        )
    return scores
