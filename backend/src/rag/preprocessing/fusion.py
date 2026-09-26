"""Weighted fusion department routing.

Combines XGBoost classifier probabilities with Qwen3 Reranker evidence from
cross-department ChromaDB candidates to produce a single department routing
decision.

Fusion formula
--------------
For each department d:

    fusion_score(d) = w_xgb * xgb_prob(d) + w_rnk * norm_reranker(d)

where:
- ``xgb_prob(d)``      — raw XGBoost softmax probability in [0, 1].
- ``norm_reranker(d)`` — reranker evidence for d, min-max normalised to [0, 1]
                         across all departments seen in the candidate set.
- ``w_xgb + w_rnk == 1.0``.

If no ChromaDB candidates are available, the result falls back to XGBoost only.
If the XGBoost classifier itself fails, ``RoutingResult.routing_method`` is set
to ``RoutingMethod.FALLBACK`` with an error message.
"""

from __future__ import annotations

import logging
from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np

from src.rag.fireworks.reranker import FireworksReranker
from src.rag.preprocessing.schemas import RoutingMethod, RoutingResult
from src.rag.router.router import DepartmentRouter

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

XGBOOST_WEIGHT = 0.20
RERANKER_WEIGHT = 0.80

_WEIGHT_TOLERANCE = 1e-6


@dataclass(frozen=True)
class FusionConfig:
    xgboost_weight: float = XGBOOST_WEIGHT
    reranker_weight: float = RERANKER_WEIGHT
    max_alternatives: int = 2

    def __post_init__(self) -> None:
        if abs(self.xgboost_weight + self.reranker_weight - 1.0) > _WEIGHT_TOLERANCE:
            raise ValueError(
                f"Fusion weights must sum to 1.0, got "
                f"{self.xgboost_weight} + {self.reranker_weight}"
            )
        if self.max_alternatives < 0:
            raise ValueError("max_alternatives must be >= 0")


# ---------------------------------------------------------------------------
# Candidate chunk type (minimal; avoids importing ChromaDB here)
# ---------------------------------------------------------------------------


@dataclass
class CandidateChunk:
    """A retrieved document chunk with its department label."""

    text: str
    department: str
    chunk_id: str = ""


# ---------------------------------------------------------------------------
# Reranker evidence aggregation
# ---------------------------------------------------------------------------


def aggregate_reranker_evidence(
    scored_chunks: Sequence[tuple[CandidateChunk, float]],
) -> dict[str, float]:
    """Aggregate per-chunk reranker scores into a per-department score.

    Strategy: for each department, take the *maximum* relevance score among all
    its candidate chunks.  Using max (rather than mean) is robust to noisy
    low-scoring chunks and rewards departments that have at least one highly
    relevant document.

    Parameters
    ----------
    scored_chunks:
        Iterable of ``(CandidateChunk, relevance_score)`` pairs as returned by
        the reranker.

    Returns
    -------
    dict[department, max_score] — only departments present in the candidate set.
    """
    dept_scores: dict[str, float] = {}
    for chunk, score in scored_chunks:
        dept = chunk.department
        if dept not in dept_scores or score > dept_scores[dept]:
            dept_scores[dept] = score
    return dept_scores


def normalize_reranker_scores(
    dept_scores: dict[str, float],
    all_departments: Sequence[str],
) -> dict[str, float]:
    """Min-max normalise reranker department scores to [0, 1].

    Departments with no candidate chunks receive a score of 0.0.  If all
    scores are identical (including the degenerate single-candidate case) the
    normalised score is 1.0 for all present departments.

    Parameters
    ----------
    dept_scores:
        Raw aggregated scores from :func:`aggregate_reranker_evidence`.
    all_departments:
        Full list of department names (from the XGBoost label encoder).
    """
    normalised: dict[str, float] = {d: 0.0 for d in all_departments}
    if not dept_scores:
        return normalised

    scores = list(dept_scores.values())
    lo, hi = min(scores), max(scores)
    span = hi - lo

    for dept, score in dept_scores.items():
        if dept in normalised:
            normalised[dept] = 1.0 if span < 1e-9 else (score - lo) / span

    return normalised


# ---------------------------------------------------------------------------
# Fusion scoring
# ---------------------------------------------------------------------------


def compute_fusion_scores(
    xgb_probs: dict[str, float],
    normalised_reranker: dict[str, float],
    config: FusionConfig,
) -> dict[str, float]:
    """Combine XGBoost and reranker signals into a single score per department."""
    departments = set(xgb_probs) | set(normalised_reranker)
    return {
        dept: (
            config.xgboost_weight * xgb_probs.get(dept, 0.0)
            + config.reranker_weight * normalised_reranker.get(dept, 0.0)
        )
        for dept in departments
    }


# ---------------------------------------------------------------------------
# Main fusion router
# ---------------------------------------------------------------------------


class FusionRouter:
    """Combines XGBoost routing with Qwen3 Reranker evidence.

    Parameters
    ----------
    xgb_router:
        Loaded :class:`DepartmentRouter` instance.
    reranker:
        Loaded :class:`FireworksReranker` instance.
    config:
        Fusion weights and hyper-parameters.
    """

    def __init__(
        self,
        xgb_router: DepartmentRouter,
        reranker: FireworksReranker,
        config: FusionConfig | None = None,
    ) -> None:
        self.xgb_router = xgb_router
        self.reranker = reranker
        self.config = config or FusionConfig()

    async def route(
        self,
        query: str,
        candidates: Sequence[CandidateChunk],
    ) -> RoutingResult:
        """Run fusion routing and return a :class:`RoutingResult`.

        Parameters
        ----------
        query:
            Raw employee query string.
        candidates:
            Document chunks fetched from ChromaDB across all departments.
            May be empty — in which case the XGBoost classifier is used alone.
        """
        # ── Step 1: XGBoost probabilities ────────────────────────────────
        try:
            xgb_probs_array: np.ndarray = self.xgb_router.predict_proba([query])[0]
            xgb_probs: dict[str, float] = {
                dept: float(prob)
                for dept, prob in zip(self.xgb_router.departments, xgb_probs_array, strict=False)
            }
        except Exception as exc:  # noqa: BLE001
            logger.exception("XGBoost classification failed: %s", exc)
            return RoutingResult(
                primary_department=self.xgb_router.departments[0],
                alternatives=[],
                xgboost_score=0.0,
                fusion_score=0.0,
                routing_method=RoutingMethod.FALLBACK,
                error=f"XGBoost failed: {exc}",
            )

        primary_xgb_dept = max(xgb_probs, key=lambda d: xgb_probs[d])
        primary_xgb_score = xgb_probs[primary_xgb_dept]

        # ── Step 2: Reranker evidence (requires candidates) ───────────────
        if not candidates:
            logger.info("No ChromaDB candidates available — falling back to XGBoost-only routing")
            alternatives = self._build_alternatives(xgb_probs, primary_xgb_dept)
            return RoutingResult(
                primary_department=primary_xgb_dept,
                alternatives=alternatives,
                xgboost_score=round(primary_xgb_score, 4),
                reranker_score=0.0,
                fusion_score=round(primary_xgb_score, 4),
                routing_method=RoutingMethod.XGBOOST_ONLY,
            )

        try:
            items = list(candidates)
            texts = [c.text for c in items]
            rerank_results = await self.reranker.rerank(query, items, texts)
            scored_chunks = [(r.item, r.relevance_score) for r in rerank_results]
        except Exception as exc:  # noqa: BLE001
            logger.warning("Reranker failed (%s) — falling back to XGBoost-only routing", exc)
            alternatives = self._build_alternatives(xgb_probs, primary_xgb_dept)
            return RoutingResult(
                primary_department=primary_xgb_dept,
                alternatives=alternatives,
                xgboost_score=round(primary_xgb_score, 4),
                reranker_score=0.0,
                fusion_score=round(primary_xgb_score, 4),
                routing_method=RoutingMethod.XGBOOST_ONLY,
                error=f"Reranker failed: {exc}",
            )

        # ── Step 3: Aggregate and normalise reranker scores ───────────────
        dept_reranker = aggregate_reranker_evidence(scored_chunks)
        normalised_reranker = normalize_reranker_scores(dept_reranker, self.xgb_router.departments)

        # ── Step 4: Compute fusion scores ─────────────────────────────────
        fusion_scores = compute_fusion_scores(xgb_probs, normalised_reranker, self.config)
        primary_dept = max(fusion_scores, key=lambda d: fusion_scores[d])
        primary_fusion_score = fusion_scores[primary_dept]
        primary_reranker_score = normalised_reranker.get(primary_dept, 0.0)

        # ── Step 5: Build alternatives ────────────────────────────────────
        alternatives = self._build_alternatives(fusion_scores, primary_dept)

        return RoutingResult(
            primary_department=primary_dept,
            alternatives=alternatives,
            xgboost_score=round(primary_xgb_score, 4),
            reranker_score=round(primary_reranker_score, 4),
            fusion_score=round(primary_fusion_score, 4),
            routing_method=RoutingMethod.FUSION,
        )

    def _build_alternatives(
        self,
        scores: dict[str, float],
        primary: str,
    ) -> list[str]:
        """Return the top-N alternative departments (excluding primary)."""
        ranked = sorted(
            (d for d in scores if d != primary),
            key=lambda d: scores[d],
            reverse=True,
        )
        return ranked[: self.config.max_alternatives]
