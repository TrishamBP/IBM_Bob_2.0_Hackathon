"""Fireworks client, embeddings and reranker (mocked HTTP)."""

import asyncio

import numpy as np
import pytest

from src.rag.fireworks import (
    FireworksAPIError,
    FireworksClient,
    FireworksEmbeddings,
    FireworksError,
    FireworksResponseError,
)
from src.rag.fireworks.embeddings import parse_embedding_response
from src.rag.fireworks.reranker import parse_rerank_response
from tests.conftest import DIMS, MODEL, fake_vector


async def test_embeddings_are_normalized_ordered_and_356d(embedder, fake_fireworks):
    texts = [f"document number {i} about laptops" for i in range(10)]
    vectors = await embedder.embed_documents(texts)
    assert vectors.shape == (10, DIMS)
    assert vectors.dtype == np.float32
    np.testing.assert_allclose(np.linalg.norm(vectors, axis=1), 1.0, atol=1e-5)
    # Mock returns items in reverse order; the client must reorder by index.
    expected = np.asarray(fake_vector(texts[3], DIMS))
    np.testing.assert_allclose(vectors[3], expected / np.linalg.norm(expected), atol=1e-5)
    assert fake_fireworks.embedding_calls == 3  # batch_size=4
    assert all(r["body"]["dimensions"] == DIMS for r in fake_fireworks.requests)


async def test_query_instruction_applied_only_to_queries(embedder, fake_fireworks):
    await embedder.embed_query("how do I get a laptop")
    await embedder.embed_documents(["laptop policy"])
    query_input, doc_input = (r["body"]["input"] for r in fake_fireworks.requests)
    assert query_input == ["Instruct: Find docs\nQuery: how do I get a laptop"]
    assert doc_input == ["laptop policy"]


async def test_wrong_dimensions_are_rejected_not_truncated(embedder, fake_fireworks):
    fake_fireworks.embedding_dims = 4096  # Fireworks' silent fallback for unsupported sizes
    with pytest.raises(FireworksResponseError, match="4096 dimensions, expected 356"):
        await embedder.embed_documents(["text"])


async def test_empty_text_rejected(embedder):
    with pytest.raises(ValueError):
        await embedder.embed_documents(["ok", "   "])


async def test_concurrency_is_bounded(client):
    embedder = FireworksEmbeddings(client, MODEL, DIMS, batch_size=1, max_concurrency=2)
    active = peak = 0
    original = client.post_json

    async def tracking(*args, **kwargs):
        nonlocal active, peak
        active += 1
        peak = max(peak, active)
        await asyncio.sleep(0.01)
        try:
            return await original(*args, **kwargs)
        finally:
            active -= 1

    client.post_json = tracking
    await embedder.embed_documents([f"t{i}" for i in range(8)])
    assert peak == 2


@pytest.mark.parametrize(
    "body, match",
    [
        ({}, "missing a 'data' list"),
        ({"data": []}, "Expected 1 embeddings"),
        ({"data": [{"index": 5, "embedding": [0.1] * DIMS}]}, "Invalid embedding index"),
        ({"data": [{"index": 0, "embedding": [0.0] * DIMS}]}, "zero-length"),
        ({"data": [{"index": 0, "embedding": ["x"] * DIMS}]}, "non-numeric"),
        ({"data": [{"index": 0, "embedding": [float("nan")] * DIMS}]}, "non-numeric"),
    ],
)
def test_parse_embedding_response_validation(body, match):
    with pytest.raises(FireworksResponseError, match=match):
        parse_embedding_response(body, expected_count=1, dimensions=DIMS)


async def test_retries_transient_errors_then_succeeds(embedder, fake_fireworks):
    fake_fireworks.fail_next = [429, 503]
    vectors = await embedder.embed_documents(["hello"])
    assert vectors.shape == (1, DIMS)
    assert len(fake_fireworks.requests) == 3


async def test_non_retryable_error_raises_immediately(embedder, fake_fireworks):
    fake_fireworks.fail_next = [401]
    with pytest.raises(FireworksAPIError) as info:
        await embedder.embed_documents(["hello"])
    assert info.value.status_code == 401
    assert len(fake_fireworks.requests) == 1


async def test_retries_exhausted(make_client, fake_fireworks):
    fake_fireworks.fail_next = [500, 500, 500]
    async with make_client(max_retries=2) as c:
        with pytest.raises(FireworksAPIError):
            await FireworksEmbeddings(c, MODEL, DIMS).embed_documents(["x"])
    assert len(fake_fireworks.requests) == 3


def test_missing_api_key_rejected():
    with pytest.raises(FireworksError, match="FIREWORKS_API_KEY"):
        FireworksClient("")


async def test_reranker_maps_scores_back_to_items(reranker, fake_fireworks):
    items = [{"id": "a"}, {"id": "b"}, {"id": "c"}]
    texts = ["cats and dogs", "vpn setup guide for laptops", "vpn"]
    results = await reranker.rerank("how to set up vpn on laptops", items, texts)
    assert [r.item["id"] for r in results] == ["b", "c", "a"]
    assert results[0].relevance_score > results[1].relevance_score > results[2].relevance_score
    sent = fake_fireworks.requests[0]["body"]
    assert sent["model"] == "fireworks/qwen3-reranker-8b"
    assert sent["documents"] == texts and sent["return_documents"] is False


async def test_reranker_respects_candidate_limit(client, fake_fireworks):
    from src.rag.fireworks import FireworksReranker

    reranker = FireworksReranker(client, "m", max_candidates=2)
    results = await reranker.rerank("q", [1, 2, 3], ["a", "b", "c"])
    assert len(results) == 2
    assert len(fake_fireworks.requests[0]["body"]["documents"]) == 2


async def test_reranker_custom_url(client, fake_fireworks):
    from src.rag.fireworks import FireworksReranker

    url = "https://api.fireworks.ai/inference/v1/rerank"
    await FireworksReranker(client, "m", url=url).rerank("q", [1], ["q"])
    assert fake_fireworks.requests[0]["path"] == "/inference/v1/rerank"


@pytest.mark.parametrize(
    "body, match",
    [
        ({"data": [{"index": 3, "relevance_score": 0.5}]}, "invalid index"),
        ({"data": [{"index": 0, "relevance_score": "high"}]}, "invalid score"),
        (
            {"data": [{"index": 0, "relevance_score": 0.1}, {"index": 0, "relevance_score": 0.2}]},
            "Duplicate",
        ),
        ({"data": []}, "scored 0 of 1"),
    ],
)
def test_parse_rerank_response_validation(body, match):
    with pytest.raises(FireworksResponseError, match=match):
        parse_rerank_response(body, expected_count=1)
