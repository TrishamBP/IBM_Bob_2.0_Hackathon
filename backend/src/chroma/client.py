"""Async wrapper around a persistent ChromaDB collection.

ChromaDB's client is synchronous, so every call is offloaded with ``asyncio.to_thread``.
Writes are serialized with an ``asyncio.Lock`` so concurrent uploads cannot interleave
the upsert/stale-delete steps for the same document.

The collection records the embedding model and dimensionality in its metadata. Opening
an existing collection with a different model or size fails loudly, so vectors from
different embedding spaces are never mixed.
"""

from __future__ import annotations

import asyncio
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import chromadb
import numpy as np


class ChromaCompatibilityError(RuntimeError):
    """The persisted collection was built with a different embedding configuration."""


class PersistenceError(RuntimeError):
    """Chunks could not be verified as stored; the write was rolled back."""


@dataclass(frozen=True)
class ChunkHit:
    id: str
    text: str
    metadata: dict[str, Any]
    distance: float

    @property
    def similarity(self) -> float:
        return 1.0 - self.distance


class ChromaStore:
    def __init__(
        self,
        persist_dir: str | Path,
        collection_name: str,
        *,
        embedding_model: str,
        embedding_dimensions: int,
    ) -> None:
        self.persist_dir = Path(persist_dir)
        self.collection_name = collection_name
        self.embedding_model = embedding_model
        self.embedding_dimensions = embedding_dimensions
        self._collection: Any = None
        self._open_lock = asyncio.Lock()
        self._write_lock = asyncio.Lock()
        self._max_batch_size = 1000
        # Bumped after every successful write so derived indexes (BM25) know to rebuild.
        self.generation = 0

    async def open(self) -> None:
        async with self._open_lock:
            if self._collection is None:
                self._collection = await asyncio.to_thread(self._open_sync)

    def _open_sync(self) -> Any:
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        client = chromadb.PersistentClient(path=str(self.persist_dir))
        self._max_batch_size = min(self._max_batch_size, client.get_max_batch_size())
        collection = client.get_or_create_collection(
            name=self.collection_name,
            configuration={"hnsw": {"space": "cosine"}},
            metadata={
                "embedding_model": self.embedding_model,
                "embedding_dimensions": self.embedding_dimensions,
            },
        )
        meta = collection.metadata or {}
        if (
            meta.get("embedding_model") != self.embedding_model
            or meta.get("embedding_dimensions") != self.embedding_dimensions
        ):
            raise ChromaCompatibilityError(
                f"Collection '{self.collection_name}' was built with "
                f"{meta.get('embedding_model')} ({meta.get('embedding_dimensions')}d), but "
                f"{self.embedding_model} ({self.embedding_dimensions}d) is configured. "
                "Use a new collection name instead of mixing embedding spaces."
            )
        space = (collection.configuration or {}).get("hnsw", {}).get("space")
        if space not in (None, "cosine"):
            raise ChromaCompatibilityError(
                f"Collection '{self.collection_name}' uses '{space}' distance, expected cosine"
            )
        return collection

    async def _coll(self) -> Any:
        if self._collection is None:
            await self.open()
        return self._collection

    def _check_vectors(self, embeddings: np.ndarray, count: int) -> None:
        if embeddings.ndim != 2 or embeddings.shape != (count, self.embedding_dimensions):
            raise ValueError(
                f"Expected embeddings of shape ({count}, {self.embedding_dimensions}), "
                f"got {embeddings.shape}"
            )

    async def replace_document(
        self,
        document_id: str,
        version: str,
        ids: list[str],
        texts: list[str],
        embeddings: np.ndarray,
        metadatas: list[dict[str, Any]],
    ) -> int:
        """Store a document version, then remove older versions; return the stored count.

        Chunk IDs include the version, so the new chunks never overwrite the old ones.
        Older versions are deleted only after every new chunk is verified as persisted;
        if verification fails, the partial new version is rolled back and the previous
        version stays intact.
        """
        if not (len(ids) == len(texts) == len(metadatas)) or not ids:
            raise ValueError("ids, texts and metadatas must be non-empty and equal length")
        if len(set(ids)) != len(ids):
            raise ValueError("chunk ids must be unique")
        self._check_vectors(embeddings, len(ids))
        collection = await self._coll()
        vectors = embeddings.astype(np.float32)
        async with self._write_lock:
            batch = max(1, self._max_batch_size)
            try:
                for i in range(0, len(ids), batch):
                    await asyncio.to_thread(
                        collection.upsert,
                        ids=ids[i : i + batch],
                        documents=texts[i : i + batch],
                        embeddings=vectors[i : i + batch],
                        metadatas=metadatas[i : i + batch],
                    )
                stored = await self.count_document_chunks(document_id, version)
                if stored != len(ids):
                    raise PersistenceError(
                        f"Persistence check failed: {stored} of {len(ids)} chunks stored"
                    )
            except Exception:
                await asyncio.to_thread(collection.delete, ids=ids)
                raise
            await asyncio.to_thread(
                collection.delete,
                where={
                    "$and": [
                        {"document_id": document_id},
                        {"document_version": {"$ne": version}},
                    ]
                },
            )
            self.generation += 1
            return stored

    async def get_document_info(self, document_id: str) -> dict[str, Any] | None:
        """Metadata of one stored chunk of the document (document-level fields), if any."""
        collection = await self._coll()
        result = await asyncio.to_thread(
            collection.get, where={"document_id": document_id}, limit=1, include=["metadatas"]
        )
        metadatas = result.get("metadatas") or []
        return dict(metadatas[0]) if metadatas else None

    async def get_document_version(self, document_id: str) -> str | None:
        collection = await self._coll()
        result = await asyncio.to_thread(
            collection.get, where={"document_id": document_id}, limit=1, include=["metadatas"]
        )
        metadatas = result.get("metadatas") or []
        return metadatas[0].get("document_version") if metadatas else None

    async def count_document_chunks(self, document_id: str, version: str) -> int:
        collection = await self._coll()
        result = await asyncio.to_thread(
            collection.get,
            where={"$and": [{"document_id": document_id}, {"document_version": version}]},
            include=[],
        )
        return len(result.get("ids") or [])

    async def count(self) -> int:
        collection = await self._coll()
        return await asyncio.to_thread(collection.count)

    async def query(
        self, embedding: np.ndarray, n_results: int, *, department: str | None = None
    ) -> list[ChunkHit]:
        self._check_vectors(np.atleast_2d(embedding), 1)
        collection = await self._coll()
        kwargs: dict[str, Any] = {
            "query_embeddings": np.atleast_2d(embedding).astype(np.float32),
            "n_results": n_results,
            "include": ["documents", "metadatas", "distances"],
        }
        if department is not None:
            kwargs["where"] = {"department": department}
        result = await asyncio.to_thread(collection.query, **kwargs)
        ids = (result.get("ids") or [[]])[0]
        docs = (result.get("documents") or [[]])[0]
        metas = (result.get("metadatas") or [[]])[0]
        dists = (result.get("distances") or [[]])[0]
        return [
            ChunkHit(id=i, text=d or "", metadata=dict(m or {}), distance=float(dist))
            for i, d, m, dist in zip(ids, docs, metas, dists, strict=True)
        ]

    async def query_many(
        self,
        embeddings: np.ndarray,
        n_results: int,
        *,
        departments: Sequence[str] | None = None,
    ) -> list[list[ChunkHit]]:
        """One ranked hit list per query vector, in a single ChromaDB call.

        ``departments`` restricts results to those departments (``None`` = all).
        """
        vectors = np.atleast_2d(embeddings)
        self._check_vectors(vectors, vectors.shape[0])
        collection = await self._coll()
        kwargs: dict[str, Any] = {
            "query_embeddings": vectors.astype(np.float32),
            "n_results": n_results,
            "include": ["documents", "metadatas", "distances"],
        }
        if departments:
            names = list(dict.fromkeys(departments))
            kwargs["where"] = (
                {"department": names[0]} if len(names) == 1 else {"department": {"$in": names}}
            )
        result = await asyncio.to_thread(collection.query, **kwargs)
        lists = []
        for ids, docs, metas, dists in zip(
            result.get("ids") or [],
            result.get("documents") or [],
            result.get("metadatas") or [],
            result.get("distances") or [],
            strict=True,
        ):
            lists.append(
                [
                    ChunkHit(id=i, text=d or "", metadata=dict(m or {}), distance=float(dist))
                    for i, d, m, dist in zip(ids, docs, metas, dists, strict=True)
                ]
            )
        return lists

    async def get_embeddings(self, ids: Sequence[str]) -> dict[str, np.ndarray]:
        """Stored chunk vectors by id (missing ids are omitted)."""
        if not ids:
            return {}
        collection = await self._coll()
        result = await asyncio.to_thread(
            collection.get, ids=list(dict.fromkeys(ids)), include=["embeddings"]
        )
        vectors = result.get("embeddings")
        if vectors is None:
            return {}
        return {
            i: np.asarray(v, dtype=np.float32)
            for i, v in zip(result.get("ids") or [], vectors, strict=True)
        }

    async def all_chunks(self, page_size: int = 1000) -> list[tuple[str, str, dict[str, Any]]]:
        """Every stored chunk as ``(id, text, metadata)`` (used to build the BM25 index)."""
        collection = await self._coll()
        chunks: list[tuple[str, str, dict[str, Any]]] = []
        offset = 0
        while True:
            result = await asyncio.to_thread(
                collection.get,
                include=["documents", "metadatas"],
                limit=page_size,
                offset=offset,
            )
            ids = result.get("ids") or []
            docs = result.get("documents") or []
            metas = result.get("metadatas") or []
            chunks.extend(
                (i, d or "", dict(m or {})) for i, d, m in zip(ids, docs, metas, strict=True)
            )
            if len(ids) < page_size:
                return chunks
            offset += page_size
