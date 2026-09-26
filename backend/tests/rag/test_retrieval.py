"""BM25, weighted RRF, MMR, evidence filtering and hybrid retrieval over ChromaDB."""

import numpy as np
import pytest

from src.rag.ingestion import IngestionService
from src.rag.retrieval import (
    BM25Index,
    EvidenceConfig,
    HybridRetriever,
    QueryVectors,
    RetrievalConfig,
    plan_departments,
)
from src.rag.retrieval.bm25 import tokenize
from src.rag.retrieval.filtering import Candidate, filter_evidence, sufficiency
from src.rag.retrieval.fusion import RankedList, reciprocal_rank_fusion
from src.rag.retrieval.mmr import mmr_select
from tests.conftest import DIMS

VPN = (
    b"# VPN Guide\n\n## Connecting\n\nInstall GlobalProtect and connect to the corporate VPN "
    b"with your SSO account.\n\n## Troubleshooting\n\nIf GlobalProtect does not connect, "
    b"restart the client and check your MFA enrollment. Reference policy SEC-101.\n"
)
REPO = (
    b"# Engineering Repositories\n\nClone the acme-payments-api repository from GitHub "
    b"Enterprise after your access request is approved.\n"
)
BENEFITS = (
    b"# Benefits Overview\n\nEnroll in health insurance within 30 days of your start date "
    b"through the Workday benefits portal.\n"
)

LOOSE = EvidenceConfig(
    min_chars=10,
    min_similarity=0.05,
    min_bm25_score=0.5,
    sufficient_similarity=0.1,
    sufficient_bm25_score=1.0,
)


@pytest.fixture
async def corpus(store, embedder):
    ingestion = IngestionService(store, embedder, max_chunk_tokens=200, overlap_tokens=20)
    await ingestion.ingest_file("IT Operations", "vpn.md", VPN)
    await ingestion.ingest_file("Software Engineering", "repos.md", REPO)
    await ingestion.ingest_file("Human Resources", "benefits.md", BENEFITS)
    return store


async def vectors_for(embedder, query, expansions=(), hyde=None) -> QueryVectors:
    original = await embedder.embed_query(query)
    exp = (
        await embedder.embed_queries(list(expansions))
        if expansions
        else np.empty((0, DIMS), dtype=np.float32)
    )
    hyde_vec = (await embedder.embed_documents([hyde]))[0] if hyde else None
    return QueryVectors(original, exp, hyde_vec)


# ---------------------------------------------------------------------- BM25


def test_tokenizer_keeps_identifiers_and_their_parts():
    tokens = tokenize("Clone acme-payments-api; see SEC-101 and v2.3 of the VPN guide")
    assert {"acme-payments-api", "acme", "payments", "api", "sec-101", "v2.3", "vpn"} <= set(tokens)
    assert "the" not in tokens and "of" not in tokens


async def test_bm25_finds_exact_terms_and_filters_departments(corpus):
    index = BM25Index(corpus)
    hits = await index.search("acme-payments-api", 5)
    assert hits and hits[0].metadata["source_filename"] == "repos.md"
    assert hits[0].id.startswith(hits[0].metadata["document_id"])  # same ids as Chroma
    policy = await index.search("SEC-101", 5)
    assert policy and "SEC-101" in policy[0].text
    assert await index.search("SEC-101", 5, departments=["Human Resources"]) == []
    assert await index.search("the of and", 5) == []  # stopwords only


async def test_bm25_refreshes_after_ingest(corpus, embedder):
    index = BM25Index(corpus)
    assert await index.search("parking", 5) == []
    size = index.size
    ingestion = IngestionService(corpus, embedder, max_chunk_tokens=200, overlap_tokens=20)
    await ingestion.ingest_file("Finance", "parking.md", b"# Parking\n\nParking permits.")
    assert (await index.search("parking permits", 5))[0].metadata["source_filename"] == "parking.md"
    assert index.size == size + 1


# ----------------------------------------------------------------------- RRF


def test_rrf_formula_weights_and_dedup():
    fused = reciprocal_rank_fusion(
        [
            RankedList("a", ["x", "y", "x"], 1.0),  # duplicate x counts once
            RankedList("b", ["y", "z"], 0.5),
        ],
        k=60,
    )
    scores = {f.id: f.score for f in fused}
    assert scores["x"] == pytest.approx(1 / 61)
    assert scores["y"] == pytest.approx(1 / 62 + 0.5 / 61)
    assert scores["z"] == pytest.approx(0.5 / 62)
    assert [f.id for f in fused] == ["y", "x", "z"]
    assert fused[0].ranks == {"a": 2, "b": 1}


def test_rrf_split_weight_prevents_expansion_overcounting():
    # Three expansions sharing weight 1.0 must not outvote one original list of weight 1.0.
    lists = [RankedList("orig", ["a", "b"], 1.0)] + [
        RankedList("exp", ["b", "a"], 1.0 / 3) for _ in range(3)
    ]
    fused = reciprocal_rank_fusion(lists, k=60)
    assert fused[0].id == "a"


# ----------------------------------------------------------------------- MMR


def test_mmr_removes_near_duplicates_and_diversifies():
    base = np.ones(4)
    embeddings = {
        "a": base,
        "a_dup": base + 1e-4,
        "b": np.array([1.0, 1.0, -1.0, -1.0]),
        "c": np.array([1.0, -1.0, 1.0, -1.0]),
    }
    relevance = {"a": 1.0, "a_dup": 0.99, "b": 0.5, "c": 0.4}
    picked = mmr_select(list(embeddings), relevance, embeddings, k=20, lambda_=0.7)
    assert picked[0] == "a" and "a_dup" not in picked
    assert set(picked) == {"a", "b", "c"}  # never padded to k


def test_mmr_caps_k_and_per_document():
    ids = [f"c{i}" for i in range(30)]
    rng = np.random.default_rng(0)
    embeddings = {i: rng.normal(size=8) for i in ids}
    relevance = {i: 1.0 - n / 100 for n, i in enumerate(ids)}
    assert len(mmr_select(ids, relevance, embeddings, k=20)) == 20
    docs = {i: ("d1" if n < 25 else "d2") for n, i in enumerate(ids)}
    picked = mmr_select(ids, relevance, embeddings, k=20, document_of=docs, max_per_document=3)
    assert {docs[i] for i in picked} == {"d1", "d2"} and len(picked) == 6
    with pytest.raises(ValueError):
        mmr_select(ids, relevance, embeddings, lambda_=1.5)


# ------------------------------------------------------------------ filtering


def test_plan_departments_adds_alternatives_when_unsure():
    confident = {
        "primary_department": "IT Operations",
        "selected_departments": ["IT Operations"],
        "predictions": [{"department": "IT Operations", "final_score": 0.9}],
        "diagnostics": {"evidence_used": True},
    }
    assert plan_departments(confident) == ["IT Operations"]
    unsure = {
        "primary_department": "IT Operations",
        "selected_departments": ["IT Operations"],
        "predictions": [
            {"department": "IT Operations", "final_score": 0.4},
            {"department": "Information Security", "final_score": 0.35},
            {"department": "Finance", "final_score": 0.1},
            {"department": "Sales", "final_score": 0.05},
        ],
        "diagnostics": {"evidence_used": True},
    }
    assert plan_departments(unsure, max_departments=3) == [
        "IT Operations",
        "Information Security",
        "Finance",
    ]
    assert plan_departments(unsure, mode="none") is None
    assert plan_departments(None) is None


def test_evidence_filter_rejects_empty_invalid_duplicate_and_unrelated():
    meta = {"department": "IT Operations", "title": "VPN"}
    cands = [
        Candidate("1", "Restart GlobalProtect if the VPN drops.", meta, evidence_similarity=0.6),
        Candidate("2", "restart globalprotect if the VPN drops. ", meta, evidence_similarity=0.6),
        Candidate("3", "   ", meta, evidence_similarity=0.9),
        Candidate("4", "Valid text but no metadata here.", {}, evidence_similarity=0.9),
        Candidate("5", "Unrelated cafeteria menu for Friday.", meta, evidence_similarity=0.1),
        Candidate("6", "Policy SEC-101 covers VPN access.", meta, 0.0, bm25_score=4.0),
    ]
    kept, rejected = filter_evidence(cands, EvidenceConfig())
    assert [c.id for c in kept] == ["1", "6"]
    assert rejected == {"duplicate": 1, "empty": 1, "invalid_metadata": 1, "low_relevance": 1}
    assert sufficiency(kept, EvidenceConfig()) is None
    weak = [Candidate("7", "x" * 30, meta, evidence_similarity=0.36)]
    assert sufficiency(weak, EvidenceConfig()) == "weak_evidence"
    assert sufficiency([], EvidenceConfig()) == "no_relevant_chunks"


# --------------------------------------------------------------------- hybrid


async def test_query_many_filters_and_batches(corpus, embedder):
    queries = await embedder.embed_queries(["vpn connect", "health insurance"])
    lists = await corpus.query_many(queries, 5, departments=["IT Operations", "Human Resources"])
    assert len(lists) == 2
    assert all(h.metadata["department"] in {"IT Operations", "Human Resources"} for h in lists[0])
    only_hr = await corpus.query_many(queries, 5, departments=["Human Resources"])
    assert {h.metadata["department"] for hits in only_hr for h in hits} == {"Human Resources"}
    stored = await corpus.get_embeddings([lists[0][0].id, "missing"])
    assert list(stored) == [lists[0][0].id] and stored[lists[0][0].id].shape == (DIMS,)


async def test_hybrid_retrieval_fuses_sources_and_caps_top_k(corpus, embedder):
    retriever = HybridRetriever(corpus, BM25Index(corpus), RetrievalConfig(evidence=LOOSE))
    query = "GlobalProtect does not connect"
    vectors = await vectors_for(
        embedder, query, ["VPN troubleshooting", "restart VPN client"], "Restart the VPN client."
    )
    result = await retriever.retrieve(query, ["VPN troubleshooting"], vectors, ["IT Operations"])
    assert result.sufficient and result.departments == ["IT Operations"]
    assert 1 <= len(result.chunks) <= 20
    top = result.chunks[0]
    assert "GlobalProtect" in top.text and top.metadata["department"] == "IT Operations"
    assert {"semantic_original", "bm25_original"} <= set(top.ranks)
    attempt = result.attempts[0]
    assert attempt["semantic_queries"] == 4  # original + 2 expansions + HyDE, one call


async def test_hyde_similarity_is_not_evidence(corpus, embedder):
    retriever = HybridRetriever(corpus, BM25Index(corpus), RetrievalConfig(evidence=LOOSE))
    # The HyDE text matches the benefits document exactly; the query does not.
    vectors = await vectors_for(embedder, "zzz qqq", hyde=BENEFITS.decode())
    chunks, _ = await retriever.search("zzz qqq", [], vectors, None)
    benefits = [c for c in chunks if c.metadata["source_filename"] == "benefits.md"]
    assert not benefits  # found via HyDE, but rejected: no query/BM25 evidence


async def test_retrieval_broadens_departments_when_evidence_is_missing(corpus, embedder):
    retriever = HybridRetriever(corpus, BM25Index(corpus), RetrievalConfig(evidence=LOOSE))
    query = "health insurance enrollment Workday"
    vectors = await vectors_for(embedder, query)
    result = await retriever.retrieve(query, [], vectors, ["Finance"])  # misrouted
    assert result.sufficient and result.departments is None
    assert result.attempts[0]["departments"] == ["Finance"]
    assert result.chunks[0].metadata["department"] == "Human Resources"


async def test_empty_collection_is_reported(store, embedder):
    retriever = HybridRetriever(store, BM25Index(store), RetrievalConfig(evidence=LOOSE))
    result = await retriever.retrieve("vpn", [], await vectors_for(embedder, "vpn"), None)
    assert result.collection_empty and not result.chunks and result.reason == "no_documents"


async def test_wrong_query_dimensions_are_rejected(corpus):
    retriever = HybridRetriever(corpus, BM25Index(corpus))
    bad = QueryVectors(np.ones(512, dtype=np.float32), np.empty((0, 512)))
    with pytest.raises(ValueError, match="dims"):
        await retriever.retrieve("vpn", [], bad, None)


def test_config_rejects_more_than_20_chunks():
    with pytest.raises(ValueError):
        RetrievalConfig(top_k=21)
