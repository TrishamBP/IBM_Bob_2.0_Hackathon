"""DepartmentRouter against the trained v2 artifacts (embeddings mocked)."""

import numpy as np
import pytest

from src.config import Settings
from src.rag.departments import DEPARTMENTS
from src.rag.fireworks import FireworksEmbeddings
from src.rag.router.router import (
    DEFAULT_MODEL_DIR,
    METADATA_FILENAME,
    DepartmentRouter,
    RouterCompatibilityError,
)

pytestmark = pytest.mark.skipif(
    not (DEFAULT_MODEL_DIR / METADATA_FILENAME).exists(), reason="router not trained"
)


@pytest.fixture
def production_embedder(client) -> FireworksEmbeddings:
    s = Settings(_env_file=None)
    return FireworksEmbeddings(
        client,
        s.fireworks_embedding_model,
        s.fireworks_embedding_dimensions,
        query_instruction=s.fireworks_query_instruction,
    )


async def test_routes_with_valid_probabilities(production_embedder):
    router = DepartmentRouter(production_embedder)
    result = await router.route("How do I reset my VPN password?", top_k=3)
    assert result["primary_department"] in DEPARTMENTS
    assert len(result["predictions"]) == 3
    probs = await router.predict_proba(["a question", "another question"])
    assert probs.shape == (2, 13)
    np.testing.assert_allclose(probs.sum(axis=1), 1.0, atol=1e-5)
    assert router.metadata["embedding_dimensions"] == 356
    batch = await router.predict_batch(["q1", "q2"])
    assert len(batch) == 2
    single = await router.predict_department("q1")
    assert set(single) == {"department", "confidence", "low_confidence"}


async def test_embedder_mismatch_rejected(client):
    for embedder in (
        FireworksEmbeddings(client, "fireworks/qwen3-embedding-8b", 512),
        FireworksEmbeddings(client, "other-model", 356),
        FireworksEmbeddings(client, "fireworks/qwen3-embedding-8b", 356, query_instruction="x"),
    ):
        with pytest.raises(RouterCompatibilityError):
            await DepartmentRouter(embedder).load()


async def test_input_validation(production_embedder):
    router = DepartmentRouter(production_embedder)
    with pytest.raises(ValueError):
        await router.route("   ")
    with pytest.raises(TypeError):
        await router.route("q", top_k=True)
    with pytest.raises(TypeError):
        await router.predict_batch("not a list")
