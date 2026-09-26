"""Department-balanced retrieval over the ChromaDB collection.

A single global similarity search tends to be dominated by whichever department has the
most (or most generic) documents. Instead, every department is queried separately with a
metadata filter, plus one unfiltered global query, and the results are merged. No
department is filtered out based on the XGBoost prediction.
"""

from __future__ import annotations

import asyncio
from collections.abc import Sequence

import numpy as np

from src.chroma.client import ChromaStore, ChunkHit
from src.rag.departments import DEPARTMENTS


class DepartmentBalancedRetriever:
    def __init__(self, store: ChromaStore, departments: Sequence[str] = DEPARTMENTS) -> None:
        self.store = store
        self.departments = tuple(departments)

    async def retrieve(
        self,
        query_embedding: np.ndarray,
        *,
        per_department_k: int = 3,
        global_k: int = 20,
        limit: int | None = None,
    ) -> list[ChunkHit]:
        """Return deduplicated hits, interleaved so every department is represented.

        Order: round-robin over departments by rank (each department's best hit first),
        followed by any additional global hits by similarity. ``limit`` truncates the
        result, which therefore keeps department balance before global extras.
        """
        per_department = await asyncio.gather(
            *(
                self.store.query(query_embedding, per_department_k, department=d)
                for d in self.departments
            )
        )
        global_hits = await self.store.query(query_embedding, global_k) if global_k > 0 else []

        merged: list[ChunkHit] = []
        seen: set[str] = set()
        for rank in range(per_department_k):
            for hits in per_department:
                if rank < len(hits) and hits[rank].id not in seen:
                    seen.add(hits[rank].id)
                    merged.append(hits[rank])
        for hit in global_hits:
            if hit.id not in seen:
                seen.add(hit.id)
                merged.append(hit)
        return merged[:limit] if limit is not None else merged

    async def retrieve_global(self, query_embedding: np.ndarray, k: int) -> list[ChunkHit]:
        return await self.store.query(query_embedding, k)
