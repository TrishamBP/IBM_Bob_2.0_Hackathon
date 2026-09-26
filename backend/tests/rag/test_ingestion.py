"""Semantic ingestion into ChromaDB: metadata, idempotency, replacement and failures."""

import json

import numpy as np
import pytest

from src.chroma.client import ChromaCompatibilityError, ChromaStore
from src.rag.ingestion import IngestionService, make_document_id, safe_filename
from src.rag.semantic import MetadataGenerator, SemanticSegmenter
from tests.conftest import DIMS, MODEL

REQUIRED_METADATA = {
    "chunk_id",
    "document_id",
    "document_version",
    "title",
    "department",
    "department_source",
    "file_type",
    "source_filename",
    "source_path",
    "chunk_index",
    "section_heading",
    "section_title",
    "heading_path_json",
    "segmentation_method",
    "contextualized_text",
    "ingested_at",
    "pipeline_version",
    "embedding_dimensions",
}

DOC_V1 = b"# Laptop Policy\n\nEveryone gets a laptop.\n\n## Returns\n\nReturn it when leaving."
DOC_V2 = b"# Laptop Policy\n\nEveryone gets a laptop and a monitor."


@pytest.fixture
def ingestion(store, embedder) -> IngestionService:
    """Without DeepSeek: structural segmentation, source-only metadata."""
    return IngestionService(store, embedder, max_chunk_tokens=200, overlap_tokens=20)


@pytest.fixture
def llm_ingestion(store, embedder, llm) -> IngestionService:
    return IngestionService(
        store,
        embedder,
        metadata=MetadataGenerator(llm),
        segmenter=SemanticSegmenter(llm),
        max_chunk_tokens=200,
        overlap_tokens=20,
        llm_model=llm.model,
    )


async def all_chunks(store: ChromaStore) -> dict:
    collection = await store._coll()
    return collection.get(include=["metadatas", "documents", "embeddings"])


async def test_ingest_stores_chunks_with_required_metadata(ingestion, store):
    result = await ingestion.ingest_file("IT Operations", "laptops.md", DOC_V1)
    assert result.status == "ingested" and result.chunks == 2
    assert result.segmentation_method == "structural"
    assert result.stages["metadata"].status == "skipped"
    assert result.stages["chunking"].status == "fallback"
    assert result.stages["persistence"].status == "succeeded"
    stored = await all_chunks(store)
    assert len(stored["ids"]) == 2
    for chunk_id, meta in zip(stored["ids"], stored["metadatas"], strict=True):
        assert REQUIRED_METADATA <= meta.keys()
        assert all(isinstance(v, str | int | float | bool) for v in meta.values())
        assert meta["chunk_id"] == chunk_id and chunk_id.startswith(result.document_id)
        assert meta["department"] == "IT Operations"
        assert meta["department_source"] == "hr_selection"
        assert meta["source_path"] == "upload://IT Operations/laptops.md"
        assert meta["embedding_dimensions"] == DIMS
    assert {m["section_heading"] for m in stored["metadatas"]} == {"Laptop Policy", "Returns"}
    returns = next(m for m in stored["metadatas"] if m["section_heading"] == "Returns")
    assert json.loads(returns["heading_path_json"]) == ["Laptop Policy", "Returns"]
    assert returns["parent_section"] == "Laptop Policy"
    # Original content is stored separately from the contextualized embedding input.
    index = stored["metadatas"].index(returns)
    assert stored["documents"][index] == "Returns\n\nReturn it when leaving."
    assert returns["contextualized_text"].startswith(
        "Document: Laptop Policy\nDepartment: IT Operations\nSection: Returns\n\n"
    )
    assert all(len(e) == DIMS for e in stored["embeddings"])


async def test_llm_ingestion_records_generated_metadata(llm_ingestion, store, fake_fireworks):
    result = await llm_ingestion.ingest_file("IT Operations", "laptops.md", DOC_V1)
    assert result.status == "ingested" and result.segmentation_method == "llm"
    assert result.stages["metadata"].status == "succeeded"
    assert result.stages["chunking"].status == "succeeded"
    assert fake_fireworks.chat_calls("metadata") == 1
    assert fake_fireworks.chat_calls("segmentation") == 1
    meta = (await all_chunks(store))["metadatas"][0]
    assert meta["llm_metadata_status"] == "succeeded"
    assert meta["llm_document_type"] == "guide" and "llm_summary" in meta
    assert meta["llm_section_context"].startswith("This section covers")
    assert meta["segmentation_method"] == "llm"
    assert "doc_owner" not in meta  # never invented


async def test_embedded_text_is_contextualized_with_exact_dims(ingestion, fake_fireworks):
    await ingestion.ingest_file("IT Operations", "laptops.md", DOC_V1)
    request = next(r for r in fake_fireworks.requests if r["path"].endswith("/embeddings"))
    assert request["body"]["dimensions"] == DIMS
    assert request["body"]["input"][0].startswith("Document: Laptop Policy\n")


async def test_wrong_embedding_dimensions_fail_without_storing(ingestion, store, fake_fireworks):
    fake_fireworks.embedding_dims = 512
    result = await ingestion.ingest_file("IT Operations", "laptops.md", DOC_V1)
    assert result.status == "failed" and result.stages["embedding"].status == "failed"
    assert await store.count() == 0


async def test_reupload_identical_is_unchanged_and_makes_no_api_calls(
    ingestion, store, fake_fireworks
):
    await ingestion.ingest_file("IT Operations", "laptops.md", DOC_V1)
    calls = len(fake_fireworks.requests)
    again = await ingestion.ingest_file("IT Operations", "laptops.md", DOC_V1)
    assert again.status == "unchanged" and again.ok and again.chunks == 2
    assert again.stages["embedding"].status == "skipped"
    assert len(fake_fireworks.requests) == calls
    assert await store.count() == 2


async def test_structural_fallback_is_reprocessed_once_llm_is_available(
    ingestion, llm_ingestion, store
):
    await ingestion.ingest_file("IT Operations", "laptops.md", DOC_V1)
    # Different config signature (LLM model) -> new version; replaces the structural one.
    upgraded = await llm_ingestion.ingest_file("IT Operations", "laptops.md", DOC_V1)
    assert upgraded.status == "ingested" and upgraded.segmentation_method == "llm"
    again = await llm_ingestion.ingest_file("IT Operations", "laptops.md", DOC_V1)
    assert again.status == "unchanged"
    stored = await all_chunks(store)
    assert {m["document_version"] for m in stored["metadatas"]} == {upgraded.document_version}


async def test_new_version_replaces_stale_chunks(ingestion, store):
    first = await ingestion.ingest_file("IT Operations", "laptops.md", DOC_V1)
    second = await ingestion.ingest_file("IT Operations", "LAPTOPS.md", DOC_V2)
    assert second.document_id == first.document_id
    assert second.document_version != first.document_version
    stored = await all_chunks(store)
    assert len(stored["ids"]) == 1
    assert {m["document_version"] for m in stored["metadatas"]} == {second.document_version}
    assert "monitor" in stored["documents"][0]


class FailingUpserts:
    """Collection proxy whose n-th upsert call raises."""

    def __init__(self, collection, fail_on: int) -> None:
        self._collection, self._fail_on, self.calls = collection, fail_on, 0

    def upsert(self, **kwargs):
        self.calls += 1
        if self.calls == self._fail_on:
            raise RuntimeError("disk full")
        return self._collection.upsert(**kwargs)

    def __getattr__(self, name):
        return getattr(self._collection, name)


async def test_failed_replacement_keeps_previous_version(ingestion, store, monkeypatch):
    first = await ingestion.ingest_file("IT Operations", "laptops.md", DOC_V1)
    proxy = FailingUpserts(await store._coll(), fail_on=2)

    async def coll():
        return proxy

    monkeypatch.setattr(store, "_coll", coll)
    monkeypatch.setattr(store, "_max_batch_size", 1)  # one upsert per chunk
    doc = DOC_V1 + b"\n\n## Loans\n\nLoaners are available."
    result = await ingestion.ingest_file("IT Operations", "laptops.md", doc)
    assert result.status == "failed" and result.stages["persistence"].status == "failed"
    stored = await all_chunks(store)
    # The partial new version was rolled back; the old version is intact.
    assert {m["document_version"] for m in stored["metadatas"]} == {first.document_version}
    assert len(stored["ids"]) == first.chunks


async def test_same_file_in_other_department_is_separate(ingestion, store):
    await ingestion.ingest_file("IT Operations", "laptops.md", DOC_V1)
    await ingestion.ingest_file("Finance", "laptops.md", DOC_V1)
    assert await store.count() == 4


async def test_extraction_failure_is_reported_not_raised(ingestion, store):
    result = await ingestion.ingest_file("Finance", "report.pdf", b"not a pdf")
    assert result.status == "failed" and "not a valid PDF" in result.message
    assert result.stages["extraction"].status == "failed"
    assert await store.count() == 0


async def test_embedding_failure_is_reported(ingestion, store, fake_fireworks):
    fake_fireworks.fail_embeddings = [400]
    result = await ingestion.ingest_file("Finance", "notes.txt", b"Expense rules")
    assert result.status == "failed" and "Embedding service error" in result.message
    assert result.stages["embedding"].status == "failed"
    assert await store.count() == 0


async def test_deepseek_failure_falls_back_and_still_ingests(llm_ingestion, fake_fireworks):
    fake_fireworks.chat_queue = {"metadata": [400], "segmentation": [400]}
    result = await llm_ingestion.ingest_file("Finance", "notes.md", b"# Expenses\n\nRules.")
    assert result.status == "ingested" and result.segmentation_method == "structural"
    assert result.stages["metadata"].status == "fallback"
    assert result.stages["chunking"].status == "fallback"
    assert "DeepSeek request failed" in result.stages["chunking"].detail


async def test_unknown_department_rejected(ingestion):
    result = await ingestion.ingest_file("Marketing", "a.txt", b"hello")
    assert result.status == "failed" and result.stages["validation"].status == "failed"


def test_ids_are_stable_and_path_safe():
    assert safe_filename("C:\\fakepath\\..\\policy.pdf") == "policy.pdf"
    assert safe_filename("../../etc/passwd") == "passwd"
    assert make_document_id("Finance", "A.pdf") == make_document_id("Finance", "a.pdf")
    assert make_document_id("Finance", "a.pdf") != make_document_id("Sales", "a.pdf")


async def test_store_refuses_other_embedding_space(tmp_path):
    path = tmp_path / "chroma"
    await ChromaStore(path, "coll_x", embedding_model=MODEL, embedding_dimensions=DIMS).open()
    old = ChromaStore(path, "coll_x", embedding_model="all-MiniLM-L6-v2", embedding_dimensions=384)
    with pytest.raises(ChromaCompatibilityError):
        await old.open()


async def test_store_rejects_wrong_vector_shape_and_duplicate_ids(store):
    with pytest.raises(ValueError, match="shape"):
        await store.replace_document("d", "v", ["d-0"], ["t"], np.zeros((1, 384)), [{"a": 1}])
    with pytest.raises(ValueError, match="unique"):
        await store.replace_document(
            "d", "v", ["d-0", "d-0"], ["t", "t"], np.ones((2, DIMS)), [{"a": 1}, {"a": 1}]
        )


async def test_department_filtered_query(ingestion, store, embedder):
    await ingestion.ingest_file("IT Operations", "laptops.md", DOC_V1)
    await ingestion.ingest_file("Finance", "expenses.txt", b"Submit expense reports monthly.")
    query = await embedder.embed_query("expense reports")
    hits = await store.query(query, 5, department="Finance")
    assert hits and all(h.metadata["department"] == "Finance" for h in hits)
    assert await store.query(query, 5, department="Sales") == []
