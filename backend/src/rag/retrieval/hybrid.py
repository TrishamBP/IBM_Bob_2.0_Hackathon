"""Hybrid retrieval: ChromaDB semantic search + BM25 -> weighted RRF -> evidence filter -> MMR.

Every query vector (original, expansions, HyDE) is searched in one batched ChromaDB call
while BM25 runs concurrently in a worker thread. Results are fused by chunk id, filtered
for evidence and diversified with MMR into at most ``top_k`` chunks.

If the evidence is insufficient the search is broadened step by step: routed
departments -> all departments -> original query only. A collection with no documents
is reported as such so the caller can answer accordingly.
"""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field
from typing import Any

import numpy as np

from src.chroma.client import ChromaStore
from src.rag.retrieval.bm25 import BM25Index
from src.rag.retrieval.filtering import (
    Candidate,
    EvidenceConfig,
    filter_evidence,
    sufficiency,
)
from src.rag.retrieval.fusion import RankedList, reciprocal_rank_fusion, split_weight
from src.rag.retrieval.mmr import mmr_select


@dataclass(frozen=True)
class RetrievalConfig:
    semantic_k: int = 30  # hits per query vector
    bm25_k: int = 30
    rrf_k: int = 60
    weight_original: float = 1.0
    weight_expansions: float = 1.0  # total, split across the expansion queries
    weight_hyde: float = 0.7
    weight_bm25: float = 1.0
    weight_bm25_expansions: float = 0.3  # total, split across the expansion queries
    fusion_candidates: int = 60  # fused candidates considered for filtering and MMR
    top_k: int = 20
    mmr_lambda: float = 0.7
    mmr_duplicate_threshold: float = 0.97
    max_chunks_per_document: int = 8
    evidence: EvidenceConfig = field(default_factory=EvidenceConfig)

    def __post_init__(self) -> None:
        if self.top_k < 1 or self.top_k > 20:
            raise ValueError("top_k must be between 1 and 20")
        if not 0.0 <= self.mmr_lambda <= 1.0:
            raise ValueError("mmr_lambda must be between 0 and 1")
        for name in ("semantic_k", "bm25_k", "fusion_candidates"):
            if getattr(self, name) < 1:
                raise ValueError(f"{name} must be >= 1")


@dataclass
class QueryVectors:
    """Unit query vectors. ``hyde`` is used for retrieval only, never as evidence."""

    original: np.ndarray
    expansions: np.ndarray
    hyde: np.ndarray | None = None

    def validate(self, dimensions: int) -> None:
        shapes = [self.original.reshape(1, -1), self.expansions.reshape(-1, dimensions)]
        if self.hyde is not None:
            shapes.append(self.hyde.reshape(1, -1))
        for matrix in shapes:
            if matrix.size and matrix.shape[1] != dimensions:
                raise ValueError(f"Query vector has {matrix.shape[1]} dims, expected {dimensions}")


@dataclass
class RetrievalResult:
    chunks: list[Candidate]
    sufficient: bool
    reason: str | None
    departments: list[str] | None
    collection_empty: bool = False
    attempts: list[dict[str, Any]] = field(default_factory=list)


class HybridRetriever:
    def __init__(
        self, store: ChromaStore, bm25: BM25Index, config: RetrievalConfig | None = None
    ) -> None:
        self.store = store
        self.bm25 = bm25
        self.config = config or RetrievalConfig()

    async def retrieve(
        self,
        query: str,
        expansion_queries: list[str],
        vectors: QueryVectors,
        departments: list[str] | None,
    ) -> RetrievalResult:
        vectors.validate(self.store.embedding_dimensions)
        if await self.store.count() == 0:
            return RetrievalResult([], False, "no_documents", departments, collection_empty=True)

        plan: list[tuple[list[str] | None, bool]] = [(departments, True)]
        if departments:
            plan.append((None, True))  # broaden to every department
        if len(expansion_queries) or vectors.hyde is not None:
            plan.append((None, False))  # original query only, globally
        attempts: list[dict[str, Any]] = []
        best: tuple[list[Candidate], list[str] | None, str | None] | None = None
        for scope, use_expansions in plan:
            started = time.perf_counter()
            chunks, diag = await self.search(
                query, expansion_queries, vectors, scope, use_expansions=use_expansions
            )
            reason = sufficiency(chunks, self.config.evidence)
            attempts.append(
                {
                    "departments": scope,
                    "use_expansions": use_expansions,
                    "selected": len(chunks),
                    "insufficient_reason": reason,
                    "ms": round((time.perf_counter() - started) * 1000, 1),
                    **diag,
                }
            )
            if reason is None:
                return RetrievalResult(chunks, True, None, scope, attempts=attempts)
            if chunks and (best is None or len(chunks) > len(best[0])):
                best = (chunks, scope, reason)
        if best is None:
            return RetrievalResult([], False, "no_relevant_chunks", None, attempts=attempts)
        return RetrievalResult(best[0], False, best[2], best[1], attempts=attempts)

    async def search(
        self,
        query: str,
        expansion_queries: list[str],
        vectors: QueryVectors,
        departments: list[str] | None,
        *,
        use_expansions: bool = True,
    ) -> tuple[list[Candidate], dict[str, Any]]:
        cfg = self.config
        expansions = vectors.expansions.reshape(-1, vectors.original.shape[-1])
        if not use_expansions:
            expansions = expansions[:0]
            expansion_queries = []
        stack = [vectors.original.reshape(1, -1), expansions]
        use_hyde = use_expansions and vectors.hyde is not None
        if use_hyde:
            stack.append(vectors.hyde.reshape(1, -1))  # type: ignore[union-attr]
        matrix = np.vstack(stack)

        semantic, bm25_original, *bm25_expanded = await asyncio.gather(
            self.store.query_many(matrix, cfg.semantic_k, departments=departments),
            self.bm25.search(query, cfg.bm25_k, departments=departments),
            *(self.bm25.search(q, cfg.bm25_k, departments=departments) for q in expansion_queries),
        )

        pool: dict[str, Candidate] = {}
        lists: list[RankedList] = []
        n_exp = len(expansions)
        for index, hits in enumerate(semantic):
            if index == 0:
                source, weight = "semantic_original", cfg.weight_original
            elif index <= n_exp:
                source, weight = "semantic_expansion", split_weight(cfg.weight_expansions, n_exp)
            else:
                source, weight = "semantic_hyde", cfg.weight_hyde
            for hit in hits:
                pool.setdefault(hit.id, Candidate(hit.id, hit.text, hit.metadata))
            lists.append(RankedList(source, [h.id for h in hits], weight))
        bm25_lists = [("bm25_original", cfg.weight_bm25, bm25_original)] + [
            ("bm25_expansion", split_weight(cfg.weight_bm25_expansions, len(bm25_expanded)), h)
            for h in bm25_expanded
        ]
        for source, weight, hits in bm25_lists:
            for hit in hits:
                cand = pool.setdefault(hit.id, Candidate(hit.id, hit.text, hit.metadata))
                cand.bm25_score = max(cand.bm25_score, hit.score)
            lists.append(RankedList(source, [h.id for h in hits], weight))

        fused = reciprocal_rank_fusion(lists, cfg.rrf_k)[: cfg.fusion_candidates]
        candidates = []
        for item in fused:
            cand = pool[item.id]
            cand.rrf_score, cand.ranks = item.score, item.ranks
            candidates.append(cand)

        stored = await self.store.get_embeddings([c.id for c in candidates])
        evidence_queries = np.vstack([vectors.original.reshape(1, -1), expansions])
        evidence_queries = _normalize_rows(evidence_queries)
        for cand in candidates:
            if cand.id in stored:
                vec = _normalize_rows(stored[cand.id].reshape(1, -1))[0]
                cand.evidence_similarity = float(np.max(evidence_queries @ vec))

        kept, rejected = filter_evidence(candidates, cfg.evidence)
        selected_ids = mmr_select(
            [c.id for c in kept],
            {c.id: c.rrf_score for c in kept},
            {i: v for i, v in stored.items()},
            k=cfg.top_k,
            lambda_=cfg.mmr_lambda,
            duplicate_threshold=cfg.mmr_duplicate_threshold,
            document_of={c.id: c.document_id for c in kept},
            max_per_document=cfg.max_chunks_per_document,
        )
        by_id = {c.id: c for c in kept}
        diagnostics = {
            "semantic_queries": int(matrix.shape[0]),
            "semantic_hits": sum(len(h) for h in semantic),
            "bm25_hits": len(bm25_original) + sum(len(h) for h in bm25_expanded),
            "fused_candidates": len(candidates),
            "rejected": rejected,
            "after_filter": len(kept),
            "documents": len({by_id[i].document_id for i in selected_ids}),
        }
        return [by_id[i] for i in selected_ids], diagnostics


def _normalize_rows(matrix: np.ndarray) -> np.ndarray:
    matrix = np.asarray(matrix, dtype=np.float32)
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    return matrix / np.where(norms > 0, norms, 1.0)
