"""Weighted Reciprocal Rank Fusion.

``score(d) = sum_s weight_s / (k + rank_s(d))`` over every ranked list ``s`` that
contains ``d`` (ranks start at 1). Several expansion queries each produce a semantic list;
callers split one weight across them so the semantic signal is not over-counted.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field


@dataclass(frozen=True)
class RankedList:
    source: str
    ids: list[str]
    weight: float = 1.0


@dataclass
class FusedItem:
    id: str
    score: float
    ranks: dict[str, int] = field(default_factory=dict)


def reciprocal_rank_fusion(lists: list[RankedList], k: int = 60) -> list[FusedItem]:
    if k < 0:
        raise ValueError("RRF k must be >= 0")
    fused: dict[str, FusedItem] = {}
    for ranked in lists:
        if ranked.weight <= 0:
            continue
        seen: set[str] = set()
        for rank, item_id in enumerate(ranked.ids, start=1):
            if item_id in seen:  # duplicates within one list count once, at the best rank
                continue
            seen.add(item_id)
            item = fused.setdefault(item_id, FusedItem(item_id, 0.0))
            item.score += ranked.weight / (k + rank)
            # Several lists may share a source name (one per expansion): keep the best rank.
            item.ranks[ranked.source] = min(rank, item.ranks.get(ranked.source, rank))
    return sorted(fused.values(), key=lambda i: (-i.score, min(i.ranks.values()), i.id))


def split_weight(total: float, parts: int) -> float:
    return total / parts if parts else 0.0


def group_ranks(items: list[FusedItem]) -> dict[str, dict[str, int]]:
    """``{chunk_id: {source: rank}}`` for diagnostics."""
    out: dict[str, dict[str, int]] = defaultdict(dict)
    for item in items:
        out[item.id].update(item.ranks)
    return dict(out)
