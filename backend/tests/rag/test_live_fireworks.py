"""Live Fireworks connectivity (opt-in, costs a few hundred tokens).

Run with:  uv run pytest -m live
Skipped unless FIREWORKS_API_KEY and FIREWORKS_RERANKER_MODEL are configured.
"""

import json

import numpy as np
import pytest

from src.config import Settings
from src.rag.embeddings import build_embedder, build_fireworks_client, build_reranker

settings = Settings()

pytestmark = [
    pytest.mark.live,
    pytest.mark.skipif(
        not settings.fireworks_api_key.get_secret_value() or not settings.fireworks_reranker_model,
        reason="FIREWORKS_API_KEY / FIREWORKS_RERANKER_MODEL not configured",
    ),
]


async def test_live_embedding_and_rerank():
    async with build_fireworks_client(settings) as client:
        embedder = build_embedder(settings, client)
        vectors = await embedder.embed_documents(["VPN setup guide", "Holiday policy"])
        assert vectors.shape == (2, settings.fireworks_embedding_dimensions)
        np.testing.assert_allclose(np.linalg.norm(vectors, axis=1), 1.0, atol=1e-4)

        reranker = build_reranker(settings, client)
        assert reranker is not None
        results = await reranker.rerank(
            "How do I connect to the VPN?",
            ["vpn", "holiday"],
            ["Install the VPN client and sign in with SSO.", "Employees get 25 days off."],
        )
        assert results[0].item == "vpn"
        assert results[0].relevance_score > results[1].relevance_score


LIVE_GUIDE = b"""# IT Employee Onboarding Guide

Version: 2.3. Owned by the IT Service Desk.

## 1. Development Environment

### 1.1 VS Code Installation

Install Visual Studio Code from the Software Center. Sign in with your ACME SSO account
so settings sync is enabled.

### 1.2 GitHub Copilot Setup

Follow these steps:

1. Request a GitHub Copilot seat through ServiceNow (catalog item "Developer Tools").
2. Wait for the approval email from your manager.
3. Install the GitHub Copilot extension in VS Code and sign in with your ACME GitHub account.

## 2. Corporate Network

### 2.1 VPN Configuration

Install GlobalProtect and connect to vpn.acme.example. MFA enrollment is required before
the first connection.

### 2.2 VPN Troubleshooting

If the VPN does not connect, restart GlobalProtect, confirm MFA is working and open a
ServiceNow ticket with the IT Service Desk if the problem persists.
"""


async def test_live_semantic_ingestion(tmp_path, capsys):
    """One small document through DeepSeek metadata/segmentation and Qwen3 embeddings."""
    from src.chroma.client import ChromaStore
    from src.rag.semantic.serialization import unflatten_metadata
    from src.rag.service import build_ingestion

    async with build_fireworks_client(settings) as client:
        embedder = build_embedder(settings, client)
        store = ChromaStore(
            tmp_path / "chroma",
            "live_ingest",
            embedding_model=embedder.model,
            embedding_dimensions=embedder.dimensions,
        )
        await store.open()
        service = build_ingestion(settings, client, embedder, store)
        result = await service.ingest_file("IT Operations", "it-onboarding.md", LIVE_GUIDE)
        stored = (await store._coll()).get(include=["metadatas", "documents", "embeddings"])

    with capsys.disabled():
        print("\nRESULT", result.status, result.message, result.segmentation_method)
        for name, stage in result.stages.items():
            print(f"  {name}: {stage.status} - {stage.detail}")
        order = sorted(
            range(len(stored["ids"])), key=lambda i: stored["metadatas"][i]["chunk_index"]
        )
        first = unflatten_metadata(stored["metadatas"][order[0]])
        doc_keys = [k for k in first if k.startswith(("llm_", "doc_", "src_", "title"))]
        print("METADATA", json.dumps({k: first[k] for k in doc_keys}, indent=1, ensure_ascii=False))
        for i in order:
            meta = stored["metadatas"][i]
            print("---- CHUNK", meta["chunk_index"], meta.get("heading_path_text"))
            print(meta["contextualized_text"])
    assert result.status == "ingested"
    assert all(len(e) == settings.fireworks_embedding_dimensions for e in stored["embeddings"])
