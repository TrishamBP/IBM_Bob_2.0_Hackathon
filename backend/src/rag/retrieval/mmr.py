"""Maximal Marginal Relevance selection over stored chunk embeddings.

``mmr(d) = lambda * relevance(d) - (1 - lambda) * max_{s in selected} cos(d, s)``

Relevance is the RRF score normalized to [0, 1]. Candidates that are near-duplicates of
an already selected chunk (cosine >= ``duplicate_threshold``) are dropped, and an
optional per-document cap keeps several documents in the final set. The result is at
most ``k`` chunks and is never padded.
"""

from __future__ import annotations

from collections import Counter

import numpy as np


def mmr_select(
    ids: list[str],
    relevance: dict[str, float],
    embeddings: dict[str, np.ndarray],
    *,
    k: int = 20,
    lambda_: float = 0.7,
    duplicate_threshold: float = 0.97,
    document_of: dict[str, str] | None = None,
    max_per_document: int | None = None,
) -> list[str]:
    if not 0.0 <= lambda_ <= 1.0:
        raise ValueError("MMR lambda must be between 0 and 1")
    if k < 1 or not ids:
        return []
    top = max(relevance.get(i, 0.0) for i in ids) or 1.0
    rel = {i: relevance.get(i, 0.0) / top for i in ids}
    unit = {i: _unit(embeddings[i]) for i in ids if i in embeddings}

    selected: list[str] = []
    per_document: Counter[str] = Counter()
    remaining = list(ids)
    max_sim = dict.fromkeys(ids, 0.0)
    while remaining and len(selected) < k:
        best, best_score = None, -np.inf
        for cand in remaining:
            score = lambda_ * rel[cand] - (1.0 - lambda_) * max_sim[cand]
            if score > best_score:
                best, best_score = cand, score
        assert best is not None
        remaining.remove(best)
        if max_sim[best] >= duplicate_threshold:
            continue
        doc = (document_of or {}).get(best)
        if doc is not None and max_per_document and per_document[doc] >= max_per_document:
            continue
        selected.append(best)
        if doc is not None:
            per_document[doc] += 1
        if best in unit:
            vec = unit[best]
            for cand in remaining:
                if cand in unit:
                    max_sim[cand] = max(max_sim[cand], float(unit[cand] @ vec))
    return selected


def _unit(vector: np.ndarray) -> np.ndarray:
    vector = np.asarray(vector, dtype=np.float32)
    norm = float(np.linalg.norm(vector))
    return vector / norm if norm > 0 else vector
