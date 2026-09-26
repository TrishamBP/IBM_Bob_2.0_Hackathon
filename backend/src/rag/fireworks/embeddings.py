"""Fireworks embedding client (Qwen3 Embedding 8B by default).

Vectors are validated strictly: the API silently falls back to the model's full size
(4096 for Qwen3 8B) for unsupported ``dimensions`` values, so every returned vector's
length is checked against the requested size. Nothing is truncated or padded.

Qwen3 embeddings are not unit-length (and the ``normalize`` request flag was observed
not to normalize them), so vectors are L2-normalized client-side before use with cosine
similarity or the XGBoost router.
"""

from __future__ import annotations

import asyncio
import math
from collections.abc import Sequence

import numpy as np

from src.rag.fireworks.client import FireworksClient, FireworksResponseError


class FireworksEmbeddings:
    def __init__(
        self,
        client: FireworksClient,
        model: str,
        dimensions: int,
        *,
        batch_size: int = 32,
        max_concurrency: int = 4,
        query_instruction: str = "",
    ) -> None:
        if batch_size < 1 or max_concurrency < 1:
            raise ValueError("batch_size and max_concurrency must be >= 1")
        self.client = client
        self.model = model
        self.dimensions = dimensions
        self.batch_size = batch_size
        self.query_instruction = query_instruction
        self._semaphore = asyncio.Semaphore(max_concurrency)

    def format_query(self, query: str) -> str:
        """Apply the Qwen3 query instruction format; documents are embedded as-is."""
        if not self.query_instruction:
            return query
        return f"Instruct: {self.query_instruction}\nQuery: {query}"

    async def embed_query(self, query: str) -> np.ndarray:
        return (await self.embed_queries([query]))[0]

    async def embed_queries(self, queries: Sequence[str]) -> np.ndarray:
        return await self._embed([self.format_query(q) for q in queries])

    async def embed_documents(self, documents: Sequence[str]) -> np.ndarray:
        return await self._embed(list(documents))

    async def _embed(self, texts: list[str]) -> np.ndarray:
        if not texts:
            return np.empty((0, self.dimensions), dtype=np.float32)
        for i, text in enumerate(texts):
            if not isinstance(text, str) or not text.strip():
                raise ValueError(f"Cannot embed empty text at position {i}")
        batches = [texts[i : i + self.batch_size] for i in range(0, len(texts), self.batch_size)]
        results = await asyncio.gather(*(self._embed_batch(batch) for batch in batches))
        return np.vstack(results)

    async def _embed_batch(self, texts: list[str]) -> np.ndarray:
        async with self._semaphore:
            body = await self.client.post_json(
                "embeddings",
                {"model": self.model, "input": texts, "dimensions": self.dimensions},
            )
        return parse_embedding_response(body, expected_count=len(texts), dimensions=self.dimensions)


def parse_embedding_response(body: dict, *, expected_count: int, dimensions: int) -> np.ndarray:
    """Validate an ``/embeddings`` response and return L2-normalized float32 vectors."""
    data = body.get("data")
    if not isinstance(data, list):
        raise FireworksResponseError("Embedding response is missing a 'data' list")
    if len(data) != expected_count:
        raise FireworksResponseError(f"Expected {expected_count} embeddings, received {len(data)}")

    vectors: list[list[float] | None] = [None] * expected_count
    for position, item in enumerate(data):
        index = item.get("index", position) if isinstance(item, dict) else None
        embedding = item.get("embedding") if isinstance(item, dict) else None
        if not isinstance(index, int) or not 0 <= index < expected_count:
            raise FireworksResponseError(f"Invalid embedding index {index!r}")
        if vectors[index] is not None:
            raise FireworksResponseError(f"Duplicate embedding index {index}")
        if not isinstance(embedding, list):
            raise FireworksResponseError(f"Embedding {index} is not a list")
        if len(embedding) != dimensions:
            raise FireworksResponseError(
                f"Embedding {index} has {len(embedding)} dimensions, expected {dimensions}. "
                "The model may not support this output size."
            )
        if not all(isinstance(v, int | float) and math.isfinite(v) for v in embedding):
            raise FireworksResponseError(f"Embedding {index} contains non-numeric values")
        vectors[index] = embedding

    matrix = np.asarray(vectors, dtype=np.float32)
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    if np.any(norms == 0):
        raise FireworksResponseError("Received a zero-length embedding vector")
    return matrix / norms
