"""Deterministic token counting and splitting.

Tokens are approximated as words and individual punctuation marks (``\\w+|[^\\w\\s]``).
This is tokenizer-independent and reproducible, and runs offline; real Qwen3/BPE token
counts are typically 1.1-1.4x higher for English prose, so size limits are configured in
these approximate units.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_TOKEN = re.compile(r"\w+|[^\w\s]", re.UNICODE)
_SENTENCE_END = frozenset(".!?")


def count_tokens(text: str) -> int:
    return sum(1 for _ in _TOKEN.finditer(text))


@dataclass(frozen=True)
class TextSlice:
    """A piece of a text. ``[core_start, end)`` pieces tile the text exactly; the optional
    ``[start, core_start)`` prefix repeats the tail of the previous piece as overlap."""

    start: int
    core_start: int
    end: int


def split_by_tokens(text: str, max_tokens: int, overlap_tokens: int = 0) -> list[TextSlice]:
    """Split ``text`` into pieces of at most ``max_tokens`` tokens (plus overlap).

    Cuts prefer, in order, a line break and a sentence end found in the second half of
    the window; otherwise the cut is made at the token limit. Deterministic for a given
    input and configuration.
    """
    if max_tokens < 1:
        raise ValueError("max_tokens must be >= 1")
    if not 0 <= overlap_tokens < max_tokens:
        raise ValueError("overlap_tokens must be >= 0 and < max_tokens")
    spans = [m.span() for m in _TOKEN.finditer(text)]
    if len(spans) <= max_tokens:
        return [TextSlice(0, 0, len(text))]

    slices: list[TextSlice] = []
    i = 0
    while i < len(spans):
        j = min(i + max_tokens, len(spans))
        if j < len(spans):
            j = _best_cut(text, spans, i + max(1, max_tokens // 2), j)
        core_start = 0 if i == 0 else spans[i][0]
        start = spans[max(i - overlap_tokens, 0)][0] if i > 0 and overlap_tokens else core_start
        end = spans[j][0] if j < len(spans) else len(text)
        slices.append(TextSlice(start, core_start, end))
        i = j
    return slices


def _best_cut(text: str, spans: list[tuple[int, int]], low: int, high: int) -> int:
    """Token index to cut before, searching ``[low, high]`` backwards."""
    for k in range(high, low - 1, -1):
        if "\n" in text[spans[k - 1][1] : spans[k][0]]:
            return k
    for k in range(high, low - 1, -1):
        if text[spans[k - 1][0] : spans[k - 1][1]] in _SENTENCE_END:
            return k
    return high
