"""Evidence context for the answer model, and citation validation of its output.

Citation markers ``[S1]..[Sn]`` are assigned to the selected chunks *before* prompting,
in retrieval order (MMR: relevance with diversity). Chunks are added until the token
budget is used; the first chunk is truncated rather than dropped if it alone exceeds
the budget. Only original chunk text is evidence: LLM summaries, section contexts and
HyDE documents are never included.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from src.rag.retrieval.filtering import Candidate
from src.rag.semantic.tokens import count_tokens, split_by_tokens

_MARKER_GROUP = re.compile(r"\[(\s*S\d+\s*(?:[,;]\s*S\d+\s*)*)\]")
_MARKER = re.compile(r"S(\d+)")


@dataclass(frozen=True)
class Source:
    citation_id: str
    chunk_id: str
    document_id: str
    title: str
    department: str
    section: str | None
    version: str | None
    source_filename: str | None
    page_start: int | None
    page_end: int | None
    url: str | None
    text: str

    @property
    def reference(self) -> str:
        return f"{self.title} — {self.section}" if self.section else self.title

    def public(self) -> dict[str, Any]:
        """What the client and chat JSON receive: no chunk text, no embeddings."""
        return {
            "id": self.citation_id,
            "chunk_id": self.chunk_id,
            "document_id": self.document_id,
            "title": self.title,
            "department": self.department,
            "section": self.section,
            "reference": self.reference,
            "version": self.version,
            "source_filename": self.source_filename,
            "page_start": self.page_start,
            "page_end": self.page_end,
            "url": self.url,
        }


def _real_url(meta: dict[str, Any]) -> str | None:
    for key in ("source_url", "url"):
        value = meta.get(key)
        if isinstance(value, str) and value.startswith(("https://", "http://")):
            return value
    return None


def _section(meta: dict[str, Any]) -> str | None:
    path = str(meta.get("heading_path_text") or "").strip()
    title = str(meta.get("title") or "")
    parts = [p.strip() for p in path.split(" > ") if p.strip()]
    if parts and parts[0] == title:
        parts = parts[1:]  # the document title is shown separately
    if parts:
        return " > ".join(parts)
    heading = meta.get("section_heading")
    return str(heading) if heading and heading != title else None


def _int(value: Any) -> int | None:
    return value if isinstance(value, int) and not isinstance(value, bool) else None


def build_sources(chunks: list[Candidate], token_budget: int) -> list[Source]:
    sources: list[Source] = []
    used = 0
    for cand in chunks:
        meta = cand.metadata
        text = cand.text.strip()
        tokens = count_tokens(text) + 30  # header overhead
        if used + tokens > token_budget:
            if sources:
                continue  # a smaller later chunk may still fit
            head = split_by_tokens(text, max(token_budget - 30, 50))[0]
            text = text[head.start : head.end].rstrip() + " …"
            tokens = token_budget
        used += tokens
        version = meta.get("doc_version") or meta.get("version")
        sources.append(
            Source(
                citation_id=f"S{len(sources) + 1}",
                chunk_id=cand.id,
                document_id=cand.document_id,
                title=str(meta.get("title") or meta.get("source_filename") or "Untitled"),
                department=str(meta.get("department") or ""),
                section=_section(meta),
                version=str(version) if version else None,
                source_filename=meta.get("source_filename"),
                page_start=_int(meta.get("page_start")),
                page_end=_int(meta.get("page_end")),
                url=_real_url(meta),
                text=text,
            )
        )
    return sources


def format_documents(sources: list[Source]) -> str:
    blocks = []
    for s in sources:
        lines = [f"[{s.citation_id}] {s.reference}", f"Department: {s.department}"]
        if s.version:
            lines.append(f"Version: {s.version}")
        if s.source_filename:
            pages = ""
            if s.page_start:
                pages = f", p. {s.page_start}" + (
                    f"-{s.page_end}" if s.page_end and s.page_end != s.page_start else ""
                )
            lines.append(f"Source: {s.source_filename}{pages}")
        lines.append("")
        lines.append(s.text)
        blocks.append("\n".join(lines))
    return "\n\n---\n\n".join(blocks)


@dataclass(frozen=True)
class CitationCheck:
    content: str  # answer with invalid markers removed
    cited: list[str]  # valid ids in order of first use
    invalid: list[str]


def validate_citations(answer: str, sources: list[Source]) -> CitationCheck:
    valid = {s.citation_id for s in sources}
    cited: list[str] = []
    invalid: list[str] = []

    def replace(match: re.Match[str]) -> str:
        ids = [f"S{n}" for n in _MARKER.findall(match.group(1))]
        keep = []
        for cid in ids:
            if cid in valid:
                keep.append(cid)
                if cid not in cited:
                    cited.append(cid)
            elif cid not in invalid:
                invalid.append(cid)
        return "".join(f"[{cid}]" for cid in dict.fromkeys(keep))

    content = _MARKER_GROUP.sub(replace, answer)
    content = re.sub(r"(\[S\d+\])(?:\s*\1)+", r"\1", content)  # "[S1][S1]" -> "[S1]"
    if invalid:
        content = re.sub(r"[ \t]+([.,;:!?])", r"\1", content)  # space left by a dropped marker
        content = re.sub(r"[ \t]{2,}", " ", content)
    return CitationCheck(content.strip(), cited, invalid)
