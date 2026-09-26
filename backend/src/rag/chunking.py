"""Passage formatting shared by retrieval-time components.

Document chunking itself is semantic and lives in :mod:`src.rag.semantic`.
"""

from __future__ import annotations


def format_passage(title: str, heading: str | None, text: str) -> str:
    """Text sent to the reranker, with title and section for context."""
    header = f"{title} — {heading}" if heading and heading != title else title
    return f"{header}\n\n{text}"
