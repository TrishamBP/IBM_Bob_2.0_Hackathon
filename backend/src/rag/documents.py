"""Rebuild a stored document from its chunks for the citation viewer.

Original files are not kept after ingestion, but the chunks cover the extracted text
exactly once (see ``semantic.chunks.verify_coverage``), so the chunks in ``chunk_index``
order reproduce the document. Two artefacts of chunking are undone here:

- Token-sliced oversized blocks repeat an overlap prefix at the start of the next
  chunk; it is removed so the text reads once.
- Extraction strips heading markup (``#``, DOCX styles, PDF font sizes). Headings are
  restored as Markdown from the chunks' heading paths, whose position gives the depth.

Only original chunk text is returned: no embeddings, LLM summaries or contextual
headers.
"""

from __future__ import annotations

from typing import Any

from src.rag.generation.context_builder import section_label
from src.rag.schemas import DocumentChunkView, DocumentView
from src.rag.semantic.serialization import unflatten_metadata

_MIN_OVERLAP_CHARS = 10
_MAX_OVERLAP_CHARS = 4000


def _int(value: Any) -> int | None:
    return value if isinstance(value, int) and not isinstance(value, bool) else None


def _strip_overlap(previous: str, text: str) -> str:
    """Drop the longest prefix of ``text`` that ``previous`` already ends with."""
    limit = min(len(previous), len(text), _MAX_OVERLAP_CHARS)
    for size in range(limit, _MIN_OVERLAP_CHARS - 1, -1):
        if previous.endswith(text[:size]):
            return text[size:].lstrip()
    return text


def _heading_depths(metas: list[dict[str, Any]]) -> dict[str, int]:
    """Heading text -> depth (0 = outermost), from every chunk's heading path."""
    depths: dict[str, int] = {}
    for meta in metas:
        for depth, heading in enumerate(meta.get("heading_path") or []):
            depths.setdefault(str(heading).strip(), depth)
    # Outline headings with no content of their own appear in no path; render them
    # one level below the title.
    for heading in metas[0].get("src_outline") or []:
        depths.setdefault(str(heading).strip(), 1)
    return depths


def _to_markdown(text: str, depths: dict[str, int], title: str) -> str:
    blocks = []
    for block in text.split("\n\n"):
        stripped = block.strip()
        depth = depths.get(stripped) if "\n" not in stripped else None
        if depth is None:
            blocks.append(block)
        elif stripped.casefold() != title.casefold():  # the title is shown separately
            blocks.append(f"{'#' * min(depth + 1, 6)} {stripped}")
    return "\n\n".join(blocks)


def build_document_view(
    document_id: str, chunks: list[tuple[str, str, dict[str, Any]]]
) -> DocumentView:
    """``chunks`` are ``(id, text, flat metadata)`` in ``chunk_index`` order."""
    # While a re-upload is being stored, two versions coexist; show the newest.
    latest = max(chunks, key=lambda c: str(c[2].get("ingested_at") or ""))[2]
    chunks = [c for c in chunks if c[2].get("document_version") == latest.get("document_version")]
    metas = [unflatten_metadata(meta) for _, _, meta in chunks]
    first = metas[0]
    title = str(first.get("title") or first.get("source_filename") or "Untitled")
    depths = _heading_depths(metas)

    views: list[DocumentChunkView] = []
    previous_text = ""
    previous_block_end: int | None = None
    for (chunk_id, text, _), meta in zip(chunks, metas, strict=True):
        text = text.strip()
        # Overlap only exists where one block was split across consecutive chunks.
        if previous_block_end is not None and meta.get("block_start") == previous_block_end:
            text = _strip_overlap(previous_text, text)
        previous_text, previous_block_end = text, _int(meta.get("block_end"))
        views.append(
            DocumentChunkView(
                chunk_id=chunk_id,
                index=len(views),
                section=section_label(meta),
                page_start=_int(meta.get("page_start")),
                page_end=_int(meta.get("page_end")),
                markdown=_to_markdown(text, depths, title),
            )
        )

    version = first.get("doc_version")
    return DocumentView(
        document_id=document_id,
        title=title,
        department=str(first.get("department") or ""),
        version=str(version) if version else None,
        effective_date=first.get("doc_effective_date"),
        source_filename=first.get("source_filename"),
        file_type=first.get("file_type"),
        page_count=_int(first.get("page_count")),
        ingested_at=first.get("ingested_at"),
        chunks=views,
    )
