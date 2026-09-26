"""Deterministic evaluation metrics and the curated dataset parser (needs `--group eval`)."""

from __future__ import annotations

import pytest

pytest.importorskip("deepeval")

from deepeval.test_case import LLMTestCase  # noqa: E402

from evals import metrics as m  # noqa: E402
from evals.dataset import DEFAULT_EXAMPLES, load_curated  # noqa: E402


def case(output: str = "Answer [S1].", **meta) -> LLMTestCase:
    return LLMTestCase(input="q", actual_output=output, metadata=meta)


def test_routing_accuracy():
    metric = m.RoutingAccuracyMetric()
    assert metric.measure(case(expected_department="Finance", primary_department="Finance")) == 1
    near = case(
        expected_department="Finance",
        primary_department="Sales",
        routing_top=[{"department": "Sales"}, {"department": "Finance"}],
    )
    assert metric.measure(near) == 0.5 and metric.is_successful()
    assert metric.measure(case(expected_department="Finance", primary_department="Sales")) == 0
    assert not metric.is_successful()


def test_department_coverage():
    metric = m.DepartmentCoverageMetric()
    score = metric.measure(
        case(
            expected_departments=["Finance", "Legal and Compliance"], filter_departments=["Finance"]
        )
    )
    assert score == 0.5 and "Legal and Compliance" in metric.reason


def test_retrieval_rank():
    metric = m.RetrievalRankMetric()
    meta = dict(
        source_chunk_id="c2",
        source_document_id="d1",
        retrieved_chunk_ids=["c1", "c2"],
        retrieved_document_ids=["d1", "d1"],
    )
    assert metric.measure(case(**meta)) == 0.5
    assert (
        metric.measure(case(**{**meta, "source_chunk_id": "c9"})) == 0.5
    )  # doc rank 1, half weight
    assert (
        metric.measure(case(**{**meta, "source_chunk_id": "c9", "source_document_id": "d9"})) == 0
    )


def test_citation_integrity():
    metric = m.CitationIntegrityMetric()
    assert (
        metric.measure(case(context_sources=3, cited_sources=["S1"], invalid_citations=["S9"]))
        == 0.5
    )
    assert metric.measure(case(context_sources=3, cited_sources=[])) == 0
    assert metric.measure(case(context_sources=0)) == 1


def test_latency_and_health():
    fast = case(timings={"total_ms": 10_000, "generation_ms": 4_000, "first_token_ms": 1_000})
    assert m.LatencyMetric().measure(fast) == 1
    slow = case(timings={"total_ms": 60_000})
    assert m.LatencyMetric().measure(slow) == 0.5

    health = m.GenerationHealthMetric()
    assert health.measure(case(finish_reason="stop")) == 1
    assert health.measure(case(finish_reason="length")) == 0
    assert health.measure(case(output="", error="boom")) == 0


def test_secret_leak():
    metric = m.SecretLeakMetric(secret="super-secret-value")
    assert metric.measure(case("nothing here")) == 1
    assert metric.measure(case("key is super-secret-value")) == 0
    assert metric.measure(case("fw_" + "a" * 24)) == 0


def test_metric_errors_are_reported_not_raised():
    metric = m.RoutingAccuracyMetric()
    assert metric.measure(case()) == 0  # expected_department missing
    assert metric.error and not metric.is_successful()


@pytest.mark.skipif(not DEFAULT_EXAMPLES.exists(), reason="frontend examples not present")
def test_load_curated():
    cases = load_curated()
    suites = {c.suite for c in cases}
    assert {"department", "cross_department", "edge_case", "conversation"} <= suites
    assert all(c.expected_department for c in cases if c.suite == "department")
    assert all(len(c.turns) > 1 for c in cases if c.suite == "conversation")
    edge = [c for c in cases if c.suite == "edge_case"]
    assert edge and all(c.expected_output for c in edge)
    assert len({c.id for c in cases}) == len(cases)
