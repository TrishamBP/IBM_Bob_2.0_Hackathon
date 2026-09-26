"""Fusion router: XGBoost department prior + neural reranker evidence.

For every department ``d``::

    final(d) = w_xgb * calibrated_xgboost_probability(d)
             + w_rr  * normalized_reranker_evidence(d)

with ``w_xgb = 0.20`` and ``w_rr = 0.80`` by default.

Pipeline for one query:

1. Embed the query once (Fireworks); the vector feeds both XGBoost and ChromaDB.
2. XGBoost gives calibrated probabilities for all 13 departments.
3. Department-balanced retrieval: each department is searched separately plus one
   global search. Nothing is pre-filtered by the XGBoost prediction.
4. The retrieved chunks are reranked against the query.
5. Reranker scores are aggregated per department (``max`` by default) and normalized.
6. If the evidence is insufficient (too few candidates or best score below
   ``min_evidence_score``) a wider global search is reranked instead.

Missing evidence is not treated as irrelevance. A department with no retrieved chunks
(for example, one with no documents uploaded yet) is scored from XGBoost alone by default
(``missing_evidence="xgboost_only"``), so the weights are renormalized for that
department. With ``"neutral"`` it receives ``neutral_evidence`` in place of the
reranker term.

Limitations: reranker scores are uncalibrated relevance scores whose scale depends on
the reranker model and passage length. The default ``clip`` normalization uses the raw
[0, 1] scores. ``max`` and ``minmax`` are relative to the current query's candidates and
exaggerate small differences when all evidence is weak.
"""

from __future__ import annotations

import logging
from collections import defaultdict
from dataclasses import asdict, dataclass
from typing import Any, Literal

import numpy as np

from src.chroma.client import ChunkHit
from src.rag.chunking import format_passage
from src.rag.fireworks import FireworksError, FireworksReranker, RerankResult
from src.rag.retriever import DepartmentBalancedRetriever
from src.rag.router.router import DepartmentRouter

logger = logging.getLogger(__name__)

Aggregation = Literal["max", "mean_top_k"]
Normalization = Literal["clip", "max", "minmax"]
MissingEvidence = Literal["xgboost_only", "neutral"]


@dataclass(frozen=True)
class FusionConfig:
    xgboost_weight: float = 0.20
    reranker_weight: float = 0.80
    aggregation: Aggregation = "max"
    aggregation_top_k: int = 2
    normalization: Normalization = "clip"
    missing_evidence: MissingEvidence = "xgboost_only"
    neutral_evidence: float = 0.0
    per_department_k: int = 3
    global_k: int = 20
    max_rerank_candidates: int = 40
    min_candidates: int = 1
    min_evidence_score: float = 0.05
    fallback_global_k: int = 50
    selection_margin: float = 0.10
    max_selected_departments: int = 3
    return_chunks: int = 10

    def __post_init__(self) -> None:
        if self.xgboost_weight < 0 or self.reranker_weight < 0:
            raise ValueError("Fusion weights must be non-negative")
        if not np.isclose(self.xgboost_weight + self.reranker_weight, 1.0):
            raise ValueError("xgboost_weight + reranker_weight must equal 1.0")
        if self.aggregation not in ("max", "mean_top_k"):
            raise ValueError(f"Unknown aggregation {self.aggregation!r}")
        if self.normalization not in ("clip", "max", "minmax"):
            raise ValueError(f"Unknown normalization {self.normalization!r}")
        if self.missing_evidence not in ("xgboost_only", "neutral"):
            raise ValueError(f"Unknown missing_evidence policy {self.missing_evidence!r}")
        for name in (
            "aggregation_top_k",
            "per_department_k",
            "max_rerank_candidates",
            "min_candidates",
            "max_selected_departments",
        ):
            if getattr(self, name) < 1:
                raise ValueError(f"{name} must be >= 1")
        if not 0.0 <= self.neutral_evidence <= 1.0:
            raise ValueError("neutral_evidence must be between 0 and 1")


def aggregate_evidence(
    results: list[RerankResult[ChunkHit]], method: Aggregation, top_k: int
) -> dict[str, float]:
    """Per-department raw reranker evidence."""
    by_department: dict[str, list[float]] = defaultdict(list)
    for result in results:
        department = result.item.metadata.get("department")
        if department:
            by_department[str(department)].append(result.relevance_score)
    evidence: dict[str, float] = {}
    for department, scores in by_department.items():
        scores.sort(reverse=True)
        evidence[department] = scores[0] if method == "max" else float(np.mean(scores[:top_k]))
    return evidence


def normalize_evidence(raw: dict[str, float], method: Normalization) -> dict[str, float]:
    if not raw:
        return {}
    if method == "clip":
        return {d: float(np.clip(s, 0.0, 1.0)) for d, s in raw.items()}
    high, low = max(raw.values()), min(raw.values())
    if method == "max":
        return {d: (s / high if high > 0 else 0.0) for d, s in raw.items()}
    if high == low:
        return {d: (1.0 if high > 0 else 0.0) for d in raw}
    return {d: (s - low) / (high - low) for d, s in raw.items()}


class FusionRouter:
    def __init__(
        self,
        router: DepartmentRouter,
        retriever: DepartmentBalancedRetriever,
        reranker: FireworksReranker,
        config: FusionConfig | None = None,
    ) -> None:
        self.router = router
        self.retriever = retriever
        self.reranker = reranker
        self.config = config or FusionConfig()

    async def route(self, query: str, *, embedding: np.ndarray | None = None) -> dict[str, Any]:
        """Route ``query``; pass ``embedding`` (its query vector) to skip re-embedding."""
        cfg = self.config
        query = DepartmentRouter._validate_query(query)

        if embedding is None:
            embedding = await self.router.embedder.embed_query(query)
        xgb_probs = (await self.router.predict_proba_from_embeddings(embedding))[0]
        xgb_scores = dict(zip(self.router.departments, map(float, xgb_probs), strict=True))

        diagnostics: dict[str, Any] = {
            "fallback_used": False,
            "fallback_reason": None,
            "reranker_error": None,
            "config": asdict(cfg),
        }

        candidates = await self.retriever.retrieve(
            embedding,
            per_department_k=cfg.per_department_k,
            global_k=cfg.global_k,
            limit=cfg.max_rerank_candidates,
        )
        diagnostics["balanced_candidates"] = len(candidates)
        reranked = await self._rerank(query, candidates, diagnostics)

        reason = self._insufficient(reranked)
        if reason and diagnostics["reranker_error"] is None:
            diagnostics["fallback_used"] = True
            diagnostics["fallback_reason"] = reason
            fallback = await self.retriever.retrieve_global(embedding, cfg.fallback_global_k)
            known = {c.id for c in candidates}
            # Only chunks not already scored are sent to the reranker, then merged.
            extra = [c for c in fallback if c.id not in known][: cfg.max_rerank_candidates]
            diagnostics["fallback_candidates"] = len(extra)
            if extra:
                reranked = sorted(
                    reranked + await self._rerank(query, extra, diagnostics),
                    key=lambda r: r.relevance_score,
                    reverse=True,
                )
        # Evidence that is still insufficient after the fallback is not used for scoring:
        # weak scores across the board say nothing about which department is right.
        evidence_used = self._insufficient(reranked) is None
        diagnostics["evidence_used"] = evidence_used
        raw_evidence = (
            aggregate_evidence(reranked, cfg.aggregation, cfg.aggregation_top_k)
            if evidence_used
            else {}
        )
        evidence = normalize_evidence(raw_evidence, cfg.normalization)
        predictions = self._fuse(xgb_scores, raw_evidence, evidence)

        top_score = predictions[0]["final_score"]
        selected = [
            p["department"]
            for p in predictions
            if top_score - p["final_score"] <= cfg.selection_margin
        ][: cfg.max_selected_departments]

        diagnostics["reranked_candidates"] = len(reranked)
        diagnostics["departments_with_evidence"] = sorted(raw_evidence)
        return {
            "query": query,
            "primary_department": predictions[0]["department"],
            "selected_departments": selected,
            "predictions": predictions,
            "retrieved_chunks": [self._chunk_view(r) for r in reranked[: cfg.return_chunks]],
            "diagnostics": diagnostics,
        }

    async def _rerank(
        self, query: str, candidates: list[ChunkHit], diagnostics: dict[str, Any]
    ) -> list[RerankResult[ChunkHit]]:
        if not candidates:
            return []
        texts = [
            format_passage(
                str(c.metadata.get("title", "")), c.metadata.get("section_heading"), c.text
            )
            for c in candidates
        ]
        try:
            return await self.reranker.rerank(query, candidates, texts)
        except FireworksError as exc:
            # Degrade to XGBoost-only routing rather than failing the request.
            logger.warning("Reranker failed; routing on XGBoost only: %s", exc)
            diagnostics["reranker_error"] = str(exc)
            return []

    def _insufficient(self, reranked: list[RerankResult[ChunkHit]]) -> str | None:
        if len(reranked) < self.config.min_candidates:
            return "too_few_candidates"
        if max(r.relevance_score for r in reranked) < self.config.min_evidence_score:
            return "low_evidence"
        return None

    def _fuse(
        self,
        xgb_scores: dict[str, float],
        raw_evidence: dict[str, float],
        evidence: dict[str, float],
    ) -> list[dict[str, Any]]:
        cfg = self.config
        predictions = []
        for department, xgb in xgb_scores.items():
            has_evidence = department in evidence
            if has_evidence:
                reranker_score: float | None = evidence[department]
                final = cfg.xgboost_weight * xgb + cfg.reranker_weight * evidence[department]
            elif cfg.missing_evidence == "neutral":
                reranker_score = None
                final = cfg.xgboost_weight * xgb + cfg.reranker_weight * cfg.neutral_evidence
            else:
                reranker_score = None
                final = xgb  # weights renormalized onto the only available signal
            predictions.append(
                {
                    "department": department,
                    "xgboost_score": round(xgb, 6),
                    "reranker_score": None if reranker_score is None else round(reranker_score, 6),
                    "raw_reranker_score": (
                        round(raw_evidence[department], 6) if has_evidence else None
                    ),
                    "final_score": round(final, 6),
                    "has_evidence": has_evidence,
                }
            )
        predictions.sort(key=lambda p: (p["final_score"], p["xgboost_score"]), reverse=True)
        return predictions

    @staticmethod
    def _chunk_view(result: RerankResult[ChunkHit]) -> dict[str, Any]:
        hit = result.item
        return {
            "chunk_id": hit.id,
            "department": hit.metadata.get("department"),
            "title": hit.metadata.get("title"),
            "source_filename": hit.metadata.get("source_filename"),
            "section_heading": hit.metadata.get("section_heading"),
            "page_start": hit.metadata.get("page_start"),
            "reranker_score": round(result.relevance_score, 6),
            "vector_similarity": round(hit.similarity, 6),
            "text": hit.text,
            "metadata": hit.metadata,
        }
