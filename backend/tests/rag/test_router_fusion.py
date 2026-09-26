"""Fusion of calibrated XGBoost probabilities with reranker evidence."""

from __future__ import annotations

import numpy as np
import pytest

from src.chroma.client import ChunkHit
from src.rag.fireworks import FireworksAPIError, RerankResult
from src.rag.router.fusion import (
    FusionConfig,
    FusionRouter,
    aggregate_evidence,
    normalize_evidence,
)
from src.rag.router.router import apply_temperature

DEPTS = ["Finance", "Human Resources", "IT Operations"]


def hit(chunk_id: str, department: str, text: str = "text") -> ChunkHit:
    return ChunkHit(chunk_id, text, {"department": department, "title": "Doc"}, 0.3)


class FakeEmbedder:
    async def embed_query(self, query):
        return np.ones(4, dtype=np.float32)


class FakeRouter:
    def __init__(self, probs):
        self.embedder = FakeEmbedder()
        self.departments = DEPTS
        self.probs = np.asarray([probs])

    async def predict_proba_from_embeddings(self, embedding):
        return self.probs


class FakeRetriever:
    def __init__(self, balanced, global_hits=()):
        self.balanced, self.global_hits = list(balanced), list(global_hits)
        self.global_calls = 0

    async def retrieve(self, embedding, **kwargs):
        return self.balanced[: kwargs.get("limit")]

    async def retrieve_global(self, embedding, k):
        self.global_calls += 1
        return self.global_hits[:k]


class FakeReranker:
    def __init__(self, scores: dict[str, float], error: Exception | None = None):
        self.scores, self.error, self.calls = scores, error, []

    async def rerank(self, query, items, texts):
        self.calls.append([i.id for i in items])
        if self.error:
            raise self.error
        results = [RerankResult(item, i, self.scores[item.id]) for i, item in enumerate(items)]
        return sorted(results, key=lambda r: r.relevance_score, reverse=True)


def by_department(result):
    return {p["department"]: p for p in result["predictions"]}


async def test_weighted_formula_and_evidence_overrides_prior():
    retriever = FakeRetriever([hit("f1", "Finance"), hit("h1", "Human Resources")])
    reranker = FakeReranker({"f1": 0.05 + 0.0, "h1": 0.9})
    fusion = FusionRouter(FakeRouter([0.7, 0.2, 0.1]), retriever, reranker)
    result = await fusion.route("How do I claim travel expenses?")
    scores = by_department(result)
    assert scores["Finance"]["final_score"] == pytest.approx(0.2 * 0.7 + 0.8 * 0.05)
    assert scores["Human Resources"]["final_score"] == pytest.approx(0.2 * 0.2 + 0.8 * 0.9)
    assert result["primary_department"] == "Human Resources"
    assert scores["Human Resources"]["has_evidence"] is True
    assert result["retrieved_chunks"][0]["chunk_id"] == "h1"
    assert result["diagnostics"]["fallback_used"] is False


async def test_department_without_evidence_is_not_zeroed():
    retriever = FakeRetriever([hit("f1", "Finance")])
    fusion = FusionRouter(FakeRouter([0.1, 0.1, 0.8]), retriever, FakeReranker({"f1": 0.3}))
    scores = by_department(await fusion.route("q"))
    it = scores["IT Operations"]
    assert it["has_evidence"] is False and it["reranker_score"] is None
    assert it["final_score"] == pytest.approx(0.8)  # XGBoost only, weights renormalized


async def test_neutral_missing_evidence_policy():
    config = FusionConfig(missing_evidence="neutral", neutral_evidence=0.5)
    retriever = FakeRetriever([hit("f1", "Finance")])
    fusion = FusionRouter(FakeRouter([0.1, 0.1, 0.8]), retriever, FakeReranker({"f1": 0.3}), config)
    scores = by_department(await fusion.route("q"))
    assert scores["IT Operations"]["final_score"] == pytest.approx(0.2 * 0.8 + 0.8 * 0.5)


async def test_global_fallback_when_evidence_is_low():
    retriever = FakeRetriever(
        [hit("f1", "Finance")], global_hits=[hit("f1", "Finance"), hit("i9", "IT Operations")]
    )
    reranker = FakeReranker({"f1": 0.01, "i9": 0.7})
    fusion = FusionRouter(FakeRouter([0.5, 0.3, 0.2]), retriever, reranker)
    result = await fusion.route("q")
    diag = result["diagnostics"]
    assert diag["fallback_used"] and diag["fallback_reason"] == "low_evidence"
    assert reranker.calls == [["f1"], ["i9"]]  # already-scored chunk is not re-sent
    assert result["primary_department"] == "IT Operations"
    assert diag["evidence_used"] is True


async def test_empty_collection_routes_on_xgboost_only():
    fusion = FusionRouter(FakeRouter([0.2, 0.7, 0.1]), FakeRetriever([]), FakeReranker({}))
    result = await fusion.route("q")
    assert result["primary_department"] == "Human Resources"
    assert result["diagnostics"]["fallback_reason"] == "too_few_candidates"
    assert result["diagnostics"]["evidence_used"] is False
    assert not any(p["has_evidence"] for p in result["predictions"])


async def test_reranker_failure_degrades_gracefully():
    reranker = FakeReranker({}, error=FireworksAPIError(500, "down"))
    retriever = FakeRetriever([hit("f1", "Finance")])
    result = await FusionRouter(FakeRouter([0.6, 0.3, 0.1]), retriever, reranker).route("q")
    assert result["primary_department"] == "Finance"
    assert "down" in result["diagnostics"]["reranker_error"]
    assert retriever.global_calls == 0


async def test_selected_departments_within_margin():
    retriever = FakeRetriever([hit("f1", "Finance"), hit("h1", "Human Resources")])
    reranker = FakeReranker({"f1": 0.80, "h1": 0.78})
    result = await FusionRouter(FakeRouter([0.4, 0.4, 0.2]), retriever, reranker).route("q")
    assert set(result["selected_departments"]) == {"Finance", "Human Resources"}


def test_aggregation_methods():
    results = [
        RerankResult(hit("a", "Finance"), 0, 0.9),
        RerankResult(hit("b", "Finance"), 1, 0.5),
        RerankResult(hit("c", "Sales"), 2, 0.2),
    ]
    assert aggregate_evidence(results, "max", 2) == {"Finance": 0.9, "Sales": 0.2}
    assert aggregate_evidence(results, "mean_top_k", 2)["Finance"] == pytest.approx(0.7)


def test_normalization_methods():
    raw = {"A": 0.2, "B": 0.4}
    assert normalize_evidence(raw, "clip") == raw
    assert normalize_evidence(raw, "max") == {"A": 0.5, "B": 1.0}
    assert normalize_evidence(raw, "minmax") == {"A": 0.0, "B": 1.0}
    assert normalize_evidence({"A": 0.3}, "minmax") == {"A": 1.0}


@pytest.mark.parametrize(
    "kwargs",
    [
        {"xgboost_weight": 0.5, "reranker_weight": 0.6},
        {"aggregation": "sum"},
        {"normalization": "zscore"},
        {"missing_evidence": "zero"},
        {"per_department_k": 0},
    ],
)
def test_invalid_config(kwargs):
    with pytest.raises(ValueError):
        FusionConfig(**kwargs)


def test_temperature_scaling_preserves_argmax_and_softens():
    probs = np.array([[0.9, 0.08, 0.02], [0.2, 0.5, 0.3]])
    softened = apply_temperature(probs, 2.0)
    np.testing.assert_allclose(softened.sum(axis=1), 1.0)
    assert (softened.argmax(axis=1) == probs.argmax(axis=1)).all()
    assert softened[0, 0] < probs[0, 0]
    assert apply_temperature(probs, 1.0) is probs
