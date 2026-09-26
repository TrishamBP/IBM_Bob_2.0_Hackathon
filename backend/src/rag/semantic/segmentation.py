"""Semantic segmentation: group extracted blocks into coherent sections.

Sections are contiguous, inclusive block ranges. DeepSeek sees block *previews* and
returns ranges plus descriptive fields; the section text is always rebuilt from the
original blocks, so the model cannot rewrite, drop or invent source content.

Every LLM answer is validated against the source structure:

- the ranges must cover the requested blocks exactly once, in order (gaps = missing
  content, overlaps = duplicated content);
- a section may contain deeper sub-headings of the heading it belongs to, but never a
  sibling or higher-level heading (that would merge unrelated sections).

Invalid answers are retried with the problems fed back to the model. If a window still
fails, or the LLM is unavailable, its blocks fall back to deterministic structural
sections (one per heading). Long documents are segmented in windows that break at
top-level headings, concurrently up to a bounded limit.
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from typing import Any, Literal

from src.rag.extraction import Block, ExtractedDocument
from src.rag.fireworks import FireworksError, FireworksLLM
from src.rag.semantic.llm_json import StructuredOutputError, call_structured
from src.rag.semantic.prompts import SEGMENTATION_SYSTEM, segmentation_prompt
from src.rag.semantic.schemas import LLMSection, LLMSegmentation
from src.rag.semantic.tokens import count_tokens

logger = logging.getLogger(__name__)

SegmentationMethod = Literal["llm", "structural"]
DocumentSegmentationMethod = Literal["llm", "structural", "mixed"]


@dataclass(frozen=True)
class Section:
    start: int  # inclusive block indices
    end: int
    method: SegmentationMethod
    title: str | None = None  # LLM-generated descriptive fields (None for structural)
    summary: str | None = None
    keywords: tuple[str, ...] = ()
    roles: tuple[str, ...] = ()
    context: str | None = None


@dataclass
class SegmentationResult:
    sections: list[Section]
    method: DocumentSegmentationMethod
    windows: int = 0
    llm_windows: int = 0
    fallback_reasons: list[str] = field(default_factory=list)
    llm_attempts: int = 0


def structural_sections(blocks: list[Block], first: int, last: int) -> list[Section]:
    """One section per heading; headings directly followed by another heading (or with
    no content yet) are kept together with the content that follows them."""
    sections: list[list[int]] = []
    for index in range(first, last + 1):
        block = blocks[index]
        current = sections[-1] if sections else None
        heading_only = current is not None and all(blocks[i].is_heading for i in current)
        if current is None or (block.is_heading and not heading_only):
            sections.append([index])
        else:
            current.append(index)
    return [Section(s[0], s[-1], "structural") for s in sections]


def validate_sections(
    sections: list[tuple[int, int]], blocks: list[Block], first: int, last: int
) -> list[str]:
    """Problems with a proposed segmentation of blocks ``first..last`` (empty if valid)."""
    if not sections:
        return ["No sections were returned"]
    problems: list[str] = []
    expected = first
    for start, end in sections:
        if start > end:
            problems.append(f"Section B{start}-B{end}: start_block is after end_block")
            continue
        if start < first or end > last:
            problems.append(f"Section B{start}-B{end} is outside the range B{first}-B{last}")
            continue
        if start > expected:
            problems.append(f"Blocks B{expected}-B{start - 1} are missing (not in any section)")
        elif start < expected:
            problems.append(f"Blocks B{start}-B{expected - 1} are duplicated in two sections")
        expected = max(expected, end + 1)
        base = blocks[start].context_level
        for i in range(start + 1, end + 1):
            if blocks[i].is_heading and blocks[i].level <= base:
                problems.append(
                    f"Section B{start}-B{end} merges B{i} (level {blocks[i].level} heading "
                    f"'{blocks[i].text[:60]}') into a section of level {base}; start a new "
                    f"section at B{i}"
                )
                break
    if expected <= last:
        problems.append(f"Blocks B{expected}-B{last} are missing (not in any section)")
    return problems


def merge_heading_only(sections: list[Section], blocks: list[Block]) -> list[Section]:
    """Attach sections that contain nothing but headings to the following section."""
    merged: list[Section] = []
    pending: int | None = None
    for section in sections:
        if all(b.is_heading for b in blocks[section.start : section.end + 1]):
            pending = section.start if pending is None else pending
            continue
        if pending is not None:
            section = Section(**{**section.__dict__, "start": pending})
            pending = None
        merged.append(section)
    if pending is not None:
        if merged:
            last = merged.pop()
            merged.append(Section(**{**last.__dict__, "end": sections[-1].end}))
        else:
            merged.append(Section(pending, sections[-1].end, sections[-1].method))
    return merged


def block_preview(index: int, block: Block, preview_chars: int) -> str:
    if block.is_heading:
        kind = f"heading L{block.level}"
    else:
        kind = block.kind
    page = f" p{block.page}" if block.page is not None else ""
    text = block.text
    if len(text) > preview_chars:
        head = text[: int(preview_chars * 0.7)].rstrip()
        tail = text[-int(preview_chars * 0.3) :].lstrip()
        text = f"{head} [...] {tail}"
    size = "" if block.is_heading else f" ({count_tokens(block.text)} tok)"
    text = text.replace("\n", " / ")
    return f"[B{index}] {kind}{page}{size}: {text}"


def make_windows(
    blocks: list[Block], budget_chars: int, preview_chars: int
) -> list[tuple[int, int]]:
    """Split block indices into windows whose previews fit ``budget_chars``.

    A window is cut at the shallowest heading in its second half when possible, so
    related subsections are segmented together.
    """
    sizes = [min(len(b.text), preview_chars) + 40 for b in blocks]
    windows: list[tuple[int, int]] = []
    start = 0
    while start < len(blocks):
        used, end = 0, start
        while end < len(blocks) and (end == start or used + sizes[end] <= budget_chars):
            used += sizes[end]
            end += 1
        if end < len(blocks):
            half = start + (end - start) // 2
            candidates = [i for i in range(max(half, start + 1), end) if blocks[i].is_heading]
            if candidates:
                end = min(candidates, key=lambda i: (blocks[i].level, -i))
        windows.append((start, end - 1))
        start = end
    return windows


class SemanticSegmenter:
    def __init__(
        self,
        llm: FireworksLLM | None,
        *,
        max_attempts: int = 3,
        window_chars: int = 24_000,
        preview_chars: int = 240,
        max_windows: int = 12,
        max_concurrency: int = 2,
        llm_extra: dict[str, Any] | None = None,
    ) -> None:
        self.llm = llm
        self.max_attempts = max_attempts
        self.window_chars = window_chars
        self.preview_chars = preview_chars
        self.max_windows = max_windows
        self.max_concurrency = max_concurrency
        self.llm_extra = llm_extra

    async def segment(
        self, doc: ExtractedDocument, *, title: str, department: str
    ) -> SegmentationResult:
        blocks = doc.blocks
        if self.llm is None:
            sections = structural_sections(blocks, 0, len(blocks) - 1)
            return SegmentationResult(sections, "structural", fallback_reasons=["LLM disabled"])

        windows = make_windows(blocks, self.window_chars, self.preview_chars)
        semaphore = asyncio.Semaphore(self.max_concurrency)

        async def run(index: int, window: tuple[int, int]):
            if index >= self.max_windows:
                return None, 0, f"window {index + 1} exceeds the {self.max_windows}-window limit"
            async with semaphore:
                try:
                    sections, attempts = await self._segment_window(doc, window, title, department)
                    return sections, attempts, None
                except StructuredOutputError as exc:
                    return None, exc.attempts, f"window {index + 1}: {exc.problems[:3]}"
                except FireworksError as exc:
                    return None, 0, f"window {index + 1}: DeepSeek request failed: {exc}"

        outcomes = await asyncio.gather(*(run(i, w) for i, w in enumerate(windows)))
        sections: list[Section] = []
        reasons: list[str] = []
        attempts = llm_windows = 0
        for (first, last), (llm_sections, used, reason) in zip(windows, outcomes, strict=True):
            attempts += used
            if llm_sections is None:
                reasons.append(reason)
                sections.extend(structural_sections(blocks, first, last))
            else:
                llm_windows += 1
                sections.extend(llm_sections)
        if reasons:
            logger.warning("Segmentation fell back to structure for %s: %s", title, reasons)
        method: DocumentSegmentationMethod = (
            "llm" if llm_windows == len(windows) else "structural" if not llm_windows else "mixed"
        )
        return SegmentationResult(sections, method, len(windows), llm_windows, reasons, attempts)

    async def _segment_window(
        self, doc: ExtractedDocument, window: tuple[int, int], title: str, department: str
    ) -> tuple[list[Section], int]:
        first, last = window
        blocks = doc.blocks
        previews = [block_preview(i, blocks[i], self.preview_chars) for i in range(first, last + 1)]
        prompt = segmentation_prompt(
            title=title, department=department, first=first, last=last, blocks=previews
        )

        def check(result: LLMSegmentation) -> list[str]:
            ranges = [(s.start_block, s.end_block) for s in result.sections]
            return validate_sections(ranges, blocks, first, last)

        result, attempts = await call_structured(
            self.llm,  # type: ignore[arg-type]
            SEGMENTATION_SYSTEM,
            prompt,
            LLMSegmentation,
            max_attempts=self.max_attempts,
            validate=check,
            extra=self.llm_extra,
        )
        sections = [_from_llm(s) for s in result.sections]
        return merge_heading_only(sections, blocks), attempts


def _from_llm(section: LLMSection) -> Section:
    return Section(
        start=section.start_block,
        end=section.end_block,
        method="llm",
        title=section.title,
        summary=section.summary,
        keywords=tuple(section.keywords),
        roles=tuple(section.roles),
        context=section.context,
    )
