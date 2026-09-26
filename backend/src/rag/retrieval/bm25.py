"""Lexical BM25 index over the same chunks (and chunk ids) stored in ChromaDB.

Dense retrieval misses exact identifiers, so BM25 catches repository names, tool names,
policy IDs, acronyms and document titles. The index covers ``title + heading path +
chunk text`` and is rebuilt lazily (in a worker thread) whenever the store's
``generation`` counter changes, i.e. after any ingest, update or removal.
"""

from __future__ import annotations

import asyncio
import math
import re
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

import numpy as np
from rank_bm25 import BM25Okapi

from src.chroma.client import ChromaStore

# Compound tokens keep "kube-prod", "sec-101", "v2.3" and "acme_api" intact; their parts
# are indexed too so "kube" alone still matches.
_TOKEN = re.compile(r"[a-z0-9]+(?:[._\-/][a-z0-9]+)*")
_SPLIT = re.compile(r"[._\-/]")
_STOPWORDS = frozenset(
    "a an and are as at be by can do does for from how i in is it my of on or should "
    "the this to what when where which who why will with you your".split()
)


def tokenize(text: str) -> list[str]:
    tokens: list[str] = []
    for match in _TOKEN.finditer(text.lower()):
        token = match.group()
        if token not in _STOPWORDS:
            tokens.append(token)
        parts = _SPLIT.split(token)
        if len(parts) > 1:
            tokens.extend(p for p in parts if p and p not in _STOPWORDS)
    return tokens


@dataclass(frozen=True)
class BM25Hit:
    id: str
    text: str
    metadata: dict[str, Any]
    score: float


class _BM25(BM25Okapi):
    """BM25Okapi with the non-negative Lucene IDF ``log(1 + (N - n + 0.5) / (n + 0.5))``.

    The classic Okapi IDF is negative for terms in more than half of the chunks, so a
    new knowledge base with one or two documents would never produce a lexical match.
    """

    def _calc_idf(self, nd: dict[str, int]) -> None:
        for word, freq in nd.items():
            self.idf[word] = math.log(1 + (self.corpus_size - freq + 0.5) / (freq + 0.5))


class _Snapshot:
    def __init__(self, chunks: list[tuple[str, str, dict[str, Any]]]) -> None:
        self.ids = [c[0] for c in chunks]
        self.texts = [c[1] for c in chunks]
        self.metadatas = [c[2] for c in chunks]
        self.departments = np.array([str(m.get("department", "")) for m in self.metadatas])
        corpus = [
            tokenize(
                " ".join(
                    (
                        str(meta.get("title", "")),
                        str(meta.get("heading_path_text", "")),
                        text,
                    )
                )
            )
            for _, text, meta in chunks
        ]
        # BM25Okapi cannot be built from an empty corpus.
        self.bm25 = _BM25(corpus) if corpus else None


class BM25Index:
    def __init__(self, store: ChromaStore, *, k1: float = 1.5, b: float = 0.75) -> None:
        self.store = store
        self.k1 = k1
        self.b = b
        self._snapshot: _Snapshot | None = None
        self._generation: int | None = None
        self._lock = asyncio.Lock()

    async def refresh(self, *, force: bool = False) -> None:
        if not force and self._generation == self.store.generation:
            return
        async with self._lock:
            generation = self.store.generation
            if not force and self._generation == generation:
                return
            chunks = await self.store.all_chunks()
            self._snapshot = await asyncio.to_thread(self._build, chunks)
            self._generation = generation

    def _build(self, chunks: list[tuple[str, str, dict[str, Any]]]) -> _Snapshot:
        snapshot = _Snapshot(chunks)
        if snapshot.bm25 is not None:
            snapshot.bm25.k1, snapshot.bm25.b = self.k1, self.b
        return snapshot

    @property
    def size(self) -> int:
        return len(self._snapshot.ids) if self._snapshot else 0

    async def search(
        self, query: str, k: int, *, departments: Sequence[str] | None = None
    ) -> list[BM25Hit]:
        """Top ``k`` chunks with a positive BM25 score, optionally department-filtered."""
        await self.refresh()
        snapshot = self._snapshot
        tokens = tokenize(query)
        if snapshot is None or snapshot.bm25 is None or not tokens or k < 1:
            return []
        return await asyncio.to_thread(self._search, snapshot, tokens, k, departments)

    @staticmethod
    def _search(
        snapshot: _Snapshot, tokens: list[str], k: int, departments: Sequence[str] | None
    ) -> list[BM25Hit]:
        assert snapshot.bm25 is not None
        scores = snapshot.bm25.get_scores(tokens)
        if departments:
            scores = np.where(np.isin(snapshot.departments, list(departments)), scores, 0.0)
        order = np.argsort(-scores, kind="stable")[:k]
        return [
            BM25Hit(snapshot.ids[i], snapshot.texts[i], snapshot.metadatas[i], float(scores[i]))
            for i in order
            if scores[i] > 0
        ]
