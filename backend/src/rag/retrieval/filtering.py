"""Department filters derived from routing, and evidence filtering of fused candidates.

Evidence similarity is the best cosine between a chunk's stored embedding and the
*query* vectors (original + expansions). The HyDE vector is deliberately excluded: a
hypothetical document is a retrieval aid, never evidence that a chunk answers anything.
"""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Any

_WS = re.compile(r"\s+")


def plan_departments(
    route: dict[str, Any] | None,
    *,
    mode: str = "routed",
    low_confidence_threshold: float = 0.55,
    max_departments: int = 3,
) -> list[str] | None:
    """Departments to filter retrieval by; ``None`` means search every department.

    The primary department is always included, together with the router's selected
    alternatives (within its score margin). When routing confidence is low, or the router
    fell back on weak evidence, the next best departments are added up to
    ``max_departments``.
    """
    if mode == "none" or not route or not route.get("primary_department"):
        return None
    departments = [route["primary_department"]]
    for d in route.get("selected_departments") or []:
        if d not in departments:
            departments.append(d)
    predictions = route.get("predictions") or []
    top = predictions[0]["final_score"] if predictions else 1.0
    diagnostics = route.get("diagnostics") or {}
    low_confidence = (
        top < low_confidence_threshold
        or diagnostics.get("fallback_used")
        or not diagnostics.get("evidence_used", True)
    )
    if low_confidence:
        for p in predictions:
            if len(departments) >= max_departments:
                break
            if p["department"] not in departments:
                departments.append(p["department"])
    return departments[: max(max_departments, 1)]


@dataclass
class Candidate:
    id: str
    text: str
    metadata: dict[str, Any]
    rrf_score: float = 0.0
    ranks: dict[str, int] = field(default_factory=dict)
    evidence_similarity: float = 0.0
    bm25_score: float = 0.0

    @property
    def document_id(self) -> str:
        return str(self.metadata.get("document_id") or self.id)


@dataclass(frozen=True)
class EvidenceConfig:
    min_chars: int = 20
    min_similarity: float = 0.35  # a chunk below this needs lexical support to be kept
    min_bm25_score: float = 3.0
    sufficient_similarity: float = 0.45  # best chunk must reach this (or strong BM25)
    sufficient_bm25_score: float = 6.0
    min_chunks: int = 1


def _fingerprint(text: str) -> str:
    return hashlib.sha1(_WS.sub(" ", text).strip().lower().encode()).hexdigest()


def filter_evidence(
    candidates: list[Candidate], config: EvidenceConfig
) -> tuple[list[Candidate], dict[str, int]]:
    """Drop empty, invalid, duplicate and unsupported chunks (order preserved)."""
    kept: list[Candidate] = []
    rejected: Counter[str] = Counter()
    seen: set[str] = set()
    for cand in candidates:
        text = (cand.text or "").strip()
        if len(text) < config.min_chars:
            rejected["empty"] += 1
            continue
        if not cand.metadata.get("department") or not cand.metadata.get("title"):
            rejected["invalid_metadata"] += 1
            continue
        fingerprint = _fingerprint(text)
        if fingerprint in seen:
            rejected["duplicate"] += 1
            continue
        if (
            cand.evidence_similarity < config.min_similarity
            and cand.bm25_score < config.min_bm25_score
        ):
            rejected["low_relevance"] += 1
            continue
        seen.add(fingerprint)
        kept.append(cand)
    return kept, dict(rejected)


def sufficiency(candidates: list[Candidate], config: EvidenceConfig) -> str | None:
    """``None`` when the evidence is sufficient, otherwise the reason it is not."""
    if len(candidates) < config.min_chunks:
        return "no_relevant_chunks"
    best_sim = max(c.evidence_similarity for c in candidates)
    best_bm25 = max(c.bm25_score for c in candidates)
    if best_sim < config.sufficient_similarity and best_bm25 < config.sufficient_bm25_score:
        return "weak_evidence"
    return None
