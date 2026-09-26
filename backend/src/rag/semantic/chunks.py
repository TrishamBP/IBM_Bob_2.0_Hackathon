"""Build hierarchical, contextualized chunks from semantic sections.

A chunk's ``content`` is assembled only from original extracted text (whole blocks, or
deterministic token-based slices of an oversized block). Oversized sections are split
at the most meaningful boundary available:

1. sub-heading boundaries inside the section,
2. block (paragraph / list / table) boundaries, keeping a lead-in paragraph that ends
   with ":" together with the list, table or code block it introduces,
3. token-based slicing of a single oversized block (preferring line and sentence ends).

``verify_coverage`` checks that the chunks cover every character of every block exactly
once (overlap prefixes excluded), so segmentation can never silently drop or duplicate
source content.
"""

from __future__ import annotations

from dataclasses import dataclass

from src.rag.extraction import Block, ExtractedDocument
from src.rag.semantic.segmentation import Section, SegmentationMethod
from src.rag.semantic.tokens import count_tokens, split_by_tokens


class CoverageError(RuntimeError):
    """Chunks do not reproduce the extracted document exactly once."""


@dataclass(frozen=True)
class Piece:
    block: int
    start: int  # text offsets within the block, including any overlap prefix
    core_start: int
    end: int
    tokens: int


@dataclass(frozen=True)
class SemanticChunk:
    index: int
    section_index: int
    part: int
    part_count: int
    content: str
    pieces: tuple[Piece, ...]
    heading_path: tuple[str, ...]
    page_start: int | None
    page_end: int | None
    block_kinds: tuple[str, ...]
    token_count: int
    char_start: int  # offsets of the covered range in ExtractedDocument.text
    char_end: int
    segmentation_method: SegmentationMethod
    llm_title: str | None = None
    summary: str | None = None
    keywords: tuple[str, ...] = ()
    roles: tuple[str, ...] = ()
    context: str | None = None

    @property
    def block_start(self) -> int:
        return self.pieces[0].block

    @property
    def block_end(self) -> int:
        return self.pieces[-1].block

    @property
    def section_title(self) -> str | None:
        return self.heading_path[-1] if self.heading_path else self.llm_title

    @property
    def section_title_source(self) -> str | None:
        if self.heading_path:
            return "source"
        return "llm" if self.llm_title else None

    @property
    def parent_section(self) -> str | None:
        return self.heading_path[-2] if len(self.heading_path) >= 2 else None


def build_chunks(
    doc: ExtractedDocument,
    sections: list[Section],
    *,
    max_tokens: int = 450,
    overlap_tokens: int = 40,
) -> list[SemanticChunk]:
    blocks = doc.blocks
    chunks: list[SemanticChunk] = []
    for section_index, section in enumerate(sections):
        parts = _split_section(blocks, section.start, section.end, max_tokens, overlap_tokens)
        for part_number, pieces in enumerate(parts, start=1):
            chunks.append(
                _make_chunk(
                    doc, len(chunks), section_index, section, part_number, len(parts), pieces
                )
            )
    verify_coverage(doc, chunks)
    return chunks


def _block_pieces(block: Block, index: int, max_tokens: int, overlap: int) -> list[Piece]:
    tokens = count_tokens(block.text)
    if tokens <= max_tokens:
        return [Piece(index, 0, 0, len(block.text), tokens)]
    return [
        Piece(index, s.start, s.core_start, s.end, count_tokens(block.text[s.start : s.end]))
        for s in split_by_tokens(block.text, max_tokens, overlap)
    ]


def _split_section(
    blocks: list[Block], first: int, last: int, max_tokens: int, overlap: int
) -> list[list[Piece]]:
    indices = list(range(first, last + 1))
    whole = [_block_pieces(blocks[i], i, max_tokens, overlap) for i in indices]
    if sum(p.tokens for pieces in whole for p in pieces) <= max_tokens:
        return [[p for pieces in whole for p in pieces]]

    # Level 1: sub-heading boundaries (a heading always starts its own group).
    groups: list[list[int]] = []
    for i in indices:
        if not groups or (blocks[i].is_heading and not _only_headings(blocks, groups[-1])):
            groups.append([])
        groups[-1].append(i)

    parts: list[list[Piece]] = []
    for group in groups:
        pieces = [p for i in group for p in _block_pieces(blocks[i], i, max_tokens, overlap)]
        if sum(p.tokens for p in pieces) <= max_tokens:
            parts.append(pieces)
        else:
            parts.extend(_pack(_units(blocks, group, max_tokens, overlap), max_tokens))
    return parts


def _only_headings(blocks: list[Block], group: list[int]) -> bool:
    return all(blocks[i].is_heading for i in group)


def _units(blocks: list[Block], group: list[int], max_tokens: int, overlap: int):
    """Level 2/3 units: headings bind to what follows, lead-ins bind to their list/table."""
    units: list[list[Piece]] = []
    bind_next = False
    for i in group:
        pieces = _block_pieces(blocks[i], i, max_tokens, overlap)
        block = blocks[i]
        if bind_next and units:
            first, rest = pieces[0], pieces[1:]
            if sum(p.tokens for p in units[-1]) + first.tokens <= max_tokens:
                units[-1].append(first)
            else:
                units.append([first])
            units.extend([p] for p in rest)
        else:
            units.extend([p] for p in pieces)
        bind_next = block.is_heading or (
            block.kind == "paragraph" and block.text.rstrip().endswith(":")
        )
    return units


def _pack(units: list[list[Piece]], max_tokens: int) -> list[list[Piece]]:
    parts: list[list[Piece]] = []
    current: list[Piece] = []
    size = 0
    for unit in units:
        tokens = sum(p.tokens for p in unit)
        # A slice of a split block starts a new part so its overlap stays meaningful.
        continuation = unit[0].core_start > 0
        if current and (size + tokens > max_tokens or continuation):
            parts.append(current)
            current, size = [], 0
        current.extend(unit)
        size += tokens
    if current:
        parts.append(current)
    return parts


def _make_chunk(
    doc: ExtractedDocument,
    index: int,
    section_index: int,
    section: Section,
    part: int,
    part_count: int,
    pieces: list[Piece],
) -> SemanticChunk:
    blocks = doc.blocks
    texts = [blocks[p.block].text[p.start : p.end].strip() for p in pieces]
    content = "\n\n".join(t for t in texts if t)
    used = [blocks[i] for i in dict.fromkeys(p.block for p in pieces)]
    pages = [pg for b in used for pg in (b.page, b.last_page) if pg is not None]
    first, last = pieces[0], pieces[-1]
    return SemanticChunk(
        index=index,
        section_index=section_index,
        part=part,
        part_count=part_count,
        content=content,
        pieces=tuple(pieces),
        heading_path=_heading_path(used),
        page_start=min(pages) if pages else None,
        page_end=max(pages) if pages else None,
        block_kinds=tuple(dict.fromkeys(b.kind for b in used)),
        token_count=count_tokens(content),
        char_start=blocks[first.block].start + first.core_start,
        char_end=blocks[last.block].start + last.end,
        segmentation_method=section.method,
        llm_title=section.title,
        summary=section.summary,
        keywords=section.keywords,
        roles=section.roles,
        context=section.context,
    )


def _heading_path(used: list[Block]) -> tuple[str, ...]:
    """Deepest heading path shared by the chunk's content (its own headings count only
    when the chunk has no other content)."""
    content = [b for b in used if not b.is_heading] or used
    path = content[0].heading_path
    for block in content[1:]:
        common = 0
        for a, b in zip(path, block.heading_path, strict=False):
            if a != b:
                break
            common += 1
        path = path[:common]
    return path


def verify_coverage(doc: ExtractedDocument, chunks: list[SemanticChunk]) -> None:
    covered: dict[int, list[tuple[int, int]]] = {}
    for chunk in chunks:
        for piece in chunk.pieces:
            covered.setdefault(piece.block, []).append((piece.core_start, piece.end))
    problems: list[str] = []
    for index, block in enumerate(doc.blocks):
        spans = sorted(covered.pop(index, []))
        if not spans:
            problems.append(f"block {index} is missing")
            continue
        position = 0
        for start, end in spans:
            if start > position and block.text[position:start].strip():
                problems.append(f"block {index} chars {position}-{start} are missing")
            if start < position:
                problems.append(f"block {index} chars {start}-{position} are duplicated")
            position = max(position, end)
        if block.text[position:].strip():
            problems.append(f"block {index} chars {position}-{len(block.text)} are missing")
    if covered:
        problems.append(f"unknown blocks referenced: {sorted(covered)}")
    if problems:
        raise CoverageError("; ".join(problems[:10]))


def contextualize(chunk: SemanticChunk, *, title: str, department: str) -> str:
    """Embedding input: hierarchy header, optional generated context, original content."""
    lines = [f"Document: {title}", f"Department: {department}"]
    path = [h for h in chunk.heading_path if h.casefold() != title.casefold()]
    if path:
        lines.append(f"Section: {path[0]}")
        if len(path) > 1:
            lines.append(f"Subsection: {' > '.join(path[1:])}")
    elif chunk.llm_title:
        lines.append(f"Section: {chunk.llm_title}")
    if chunk.part_count > 1:
        lines.append(f"Part: {chunk.part} of {chunk.part_count}")
    header = "\n".join(lines)
    if chunk.context:
        header = f"{header}\n\n{chunk.context}"
    return f"{header}\n\n{chunk.content}"
