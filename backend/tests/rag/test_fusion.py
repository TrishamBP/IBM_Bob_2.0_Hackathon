"""Unit tests for the fusion routing module.

All XGBoost and reranker calls are mocked — no model files or API credentials
are required to run these tests.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import numpy as np
import pytest

from src.rag.fireworks.reranker import RerankResult
from src.rag.preprocessing.fusion import (
    CandidateChunk,
    FusionConfig,
    FusionRouter,
    aggregate_reranker_evidence,
    compute_fusion_scores,
    normalize_reranker_scores,
)
from src.rag.preprocessing.schemas import RoutingMethod

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


# ---------------------------------------------------------------------------
# FusionConfig
# ---------------------------------------------------------------------------


def test_fusion_config_defaults():
    cfg = FusionConfig()
    assert abs(cfg.xgboost_weight + cfg.reranker_weight - 1.0) < 1e-6


def test_fusion_config_invalid_weights():
    with pytest.raises(ValueError, match="sum to 1.0"):
        FusionConfig(xgboost_weight=0.5, reranker_weight=0.3)


def test_fusion_config_negative_alternatives():
    with pytest.raises(ValueError, match="max_alternatives"):
        FusionConfig(max_alternatives=-1)


# ---------------------------------------------------------------------------
# aggregate_reranker_evidence
# ---------------------------------------------------------------------------


def test_aggregate_takes_max_per_department():
    chunks = [
        CandidateChunk("text1", "Cloud Platform and DevOps"),
        CandidateChunk("text2", "Cloud Platform and DevOps"),
        CandidateChunk("text3", "IT Operations"),
    ]
    scored = [(chunks[0], 0.4), (chunks[1], 0.9), (chunks[2], 0.6)]
    result = aggregate_reranker_evidence(scored)
    assert result["Cloud Platform and DevOps"] == pytest.approx(0.9)
    assert result["IT Operations"] == pytest.approx(0.6)


def test_aggregate_empty_input():
    assert aggregate_reranker_evidence([]) == {}


def test_aggregate_single_chunk():
    chunk = CandidateChunk("text", "Finance")
    result = aggregate_reranker_evidence([(chunk, 0.75)])
    assert result == {"Finance": pytest.approx(0.75)}


# ---------------------------------------------------------------------------
# normalize_reranker_scores
# ---------------------------------------------------------------------------


def test_normalize_scales_to_0_1():
    dept_scores = {"Cloud Platform and DevOps": 0.2, "IT Operations": 0.8}
    norm = normalize_reranker_scores(dept_scores, DEPARTMENTS)
    assert norm["Cloud Platform and DevOps"] == pytest.approx(0.0)
    assert norm["IT Operations"] == pytest.approx(1.0)


def test_normalize_missing_departments_get_zero():
    dept_scores = {"Finance": 0.5}
    norm = normalize_reranker_scores(dept_scores, DEPARTMENTS)
    for dept in DEPARTMENTS:
        if dept != "Finance":
            assert norm[dept] == pytest.approx(0.0)


def test_normalize_empty_scores():
    norm = normalize_reranker_scores({}, DEPARTMENTS)
    assert all(v == pytest.approx(0.0) for v in norm.values())


def test_normalize_single_dept_gives_one():
    """When only one department has a score, it should normalise to 1.0."""
    dept_scores = {"Sales": 0.4}
    norm = normalize_reranker_scores(dept_scores, DEPARTMENTS)
    assert norm["Sales"] == pytest.approx(1.0)


def test_normalize_all_same_score():
    """All identical scores should normalise to 1.0 (span=0 edge case)."""
    dept_scores = {"IT Operations": 0.5, "Finance": 0.5}
    norm = normalize_reranker_scores(dept_scores, DEPARTMENTS)
    assert norm["IT Operations"] == pytest.approx(1.0)
    assert norm["Finance"] == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# compute_fusion_scores
# ---------------------------------------------------------------------------


def test_fusion_scores_weighted_combination():
    cfg = FusionConfig(xgboost_weight=0.2, reranker_weight=0.8)
    xgb = {"Cloud Platform and DevOps": 0.7, "IT Operations": 0.2}
    rnk = {"Cloud Platform and DevOps": 0.9, "IT Operations": 0.1}
    scores = compute_fusion_scores(xgb, rnk, cfg)
    expected_cloud = 0.2 * 0.7 + 0.8 * 0.9
    assert scores["Cloud Platform and DevOps"] == pytest.approx(expected_cloud)


def test_fusion_scores_xgboost_only_weight():
    """With w_xgb=1.0 the reranker signal is ignored."""
    cfg = FusionConfig(xgboost_weight=1.0, reranker_weight=0.0)
    xgb = {"Finance": 0.6, "Sales": 0.4}
    rnk = {"Finance": 0.0, "Sales": 1.0}
    scores = compute_fusion_scores(xgb, rnk, cfg)
    assert scores["Finance"] == pytest.approx(0.6)
    assert scores["Sales"] == pytest.approx(0.4)


def test_fusion_includes_all_departments():
    """A department present in only one signal must still appear in the output."""
    cfg = FusionConfig()
    xgb = {"Human Resources": 0.8}
    rnk = {"Software Engineering": 0.9}
    scores = compute_fusion_scores(xgb, rnk, cfg)
    assert "Human Resources" in scores
    assert "Software Engineering" in scores


# ---------------------------------------------------------------------------
# FusionRouter integration tests (mocked)
# ---------------------------------------------------------------------------


def _make_xgb_router(departments: list[str], proba_row: list[float]) -> MagicMock:
    router = MagicMock()
    router.departments = departments
    proba_array = np.array([proba_row])
    router.predict_proba.return_value = proba_array
    return router


def _make_reranker(scored_results: list[tuple[CandidateChunk, float]]) -> MagicMock:
    reranker = MagicMock()
    reranker.rerank = AsyncMock(
        return_value=[
            RerankResult(item=c, index=i, relevance_score=s)
            for i, (c, s) in enumerate(scored_results)
        ]
    )
    return reranker


@pytest.mark.asyncio
async def test_fusion_router_no_candidates_uses_xgboost():
    proba = [0.0] * len(DEPARTMENTS)
    proba[DEPARTMENTS.index("Cloud Platform and DevOps")] = 0.85
    xgb = _make_xgb_router(DEPARTMENTS, proba)
    reranker = _make_reranker([])

    fr = FusionRouter(xgb, reranker)
    result = await fr.route("How do I access K8s?", candidates=[])

    assert result.routing_method == RoutingMethod.XGBOOST_ONLY
    assert result.primary_department == "Cloud Platform and DevOps"
    assert result.xgboost_score == pytest.approx(0.85)


@pytest.mark.asyncio
async def test_fusion_router_reranker_can_override_xgboost():
    """Reranker evidence should be able to flip the routing decision."""
    proba = [0.0] * len(DEPARTMENTS)
    proba[DEPARTMENTS.index("IT Operations")] = 0.6  # XGBoost says IT Ops
    proba[DEPARTMENTS.index("Cloud Platform and DevOps")] = 0.3
    xgb = _make_xgb_router(DEPARTMENTS, proba)

    # Reranker strongly prefers Cloud Platform and DevOps
    chunks = [
        CandidateChunk("Kubernetes production access guide", "Cloud Platform and DevOps"),
        CandidateChunk("General IT setup", "IT Operations"),
    ]
    reranker = _make_reranker([(chunks[0], 0.95), (chunks[1], 0.1)])

    fr = FusionRouter(xgb, reranker)
    result = await fr.route("How do I access K8s prod?", candidates=chunks)

    assert result.routing_method == RoutingMethod.FUSION
    assert result.primary_department == "Cloud Platform and DevOps"


@pytest.mark.asyncio
async def test_fusion_router_reranker_failure_falls_back():
    proba = [0.0] * len(DEPARTMENTS)
    proba[DEPARTMENTS.index("Finance")] = 0.7
    xgb = _make_xgb_router(DEPARTMENTS, proba)

    reranker = MagicMock()
    reranker.rerank = AsyncMock(side_effect=RuntimeError("reranker unavailable"))

    chunks = [CandidateChunk("some text", "Finance")]
    fr = FusionRouter(xgb, reranker)
    result = await fr.route("How do I submit expenses?", candidates=chunks)

    assert result.routing_method == RoutingMethod.XGBOOST_ONLY
    assert result.error is not None


@pytest.mark.asyncio
async def test_fusion_router_xgboost_failure_returns_fallback():
    xgb = MagicMock()
    xgb.departments = DEPARTMENTS
    xgb.predict_proba.side_effect = RuntimeError("model file missing")

    reranker = MagicMock()
    chunks: list[CandidateChunk] = []

    fr = FusionRouter(xgb, reranker)
    result = await fr.route("anything", candidates=chunks)

    assert result.routing_method == RoutingMethod.FALLBACK
    assert result.error is not None


@pytest.mark.asyncio
async def test_fusion_router_alternatives_excluded_from_primary():
    proba = [0.0] * len(DEPARTMENTS)
    proba[DEPARTMENTS.index("Software Engineering")] = 0.6
    proba[DEPARTMENTS.index("AI and Machine Learning")] = 0.25
    proba[DEPARTMENTS.index("Cloud Platform and DevOps")] = 0.1
    xgb = _make_xgb_router(DEPARTMENTS, proba)
    reranker = _make_reranker([])

    fr = FusionRouter(xgb, reranker, FusionConfig(max_alternatives=2))
    result = await fr.route("implement ML pipeline", candidates=[])

    assert result.primary_department not in result.alternatives
