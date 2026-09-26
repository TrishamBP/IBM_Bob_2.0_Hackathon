"""Prompts for DeepSeek document metadata generation and semantic segmentation.

Bump ``PROMPT_VERSION`` whenever a prompt changes meaningfully; it is part of the
document version hash, so re-uploads are reprocessed with the new prompts.
"""

from __future__ import annotations

import json
from typing import Any

from src.rag.departments import DEPARTMENTS
from src.rag.semantic.schemas import DOCUMENT_TYPES

PROMPT_VERSION = "1"

METADATA_SYSTEM = f"""TASK: document_metadata
You analyse internal ACME Corp documents for an employee onboarding knowledge base.
You receive an extracted document (source metadata, heading outline and a text excerpt)
and return ONE JSON object describing it.

Rules:
- Use only information present in the provided text or source metadata. Never invent
  facts, dates, owners, contacts, policy requirements or approval chains.
- The department was selected by HR and is authoritative. Only fill
  "suggested_primary_department" if the content clearly belongs to a different
  department; otherwise repeat the HR department. "secondary_departments" lists other
  departments the document is clearly relevant to. Allowed departments:
  {", ".join(DEPARTMENTS)}.
- "owner", "version", "effective_date", "review_date": fill ONLY when explicitly stated.
  Return {{"value": "...", "evidence": "<short verbatim quote copied from the text>"}},
  otherwise null.
- "referenced_systems", "referenced_products", "referenced_policies",
  "document_identifiers": only names literally written in the text, copied exactly.
- Use null or [] for anything unavailable. Keep lists short (at most 12 items).
- "document_type" is one of: {", ".join(DOCUMENT_TYPES)}.

JSON shape:
{{"title": str|null, "document_type": str, "suggested_primary_department": str|null,
 "secondary_departments": [str], "relevant_roles": [str], "topics": [str],
 "keywords": [str], "summary": str (2-4 sentences), "intended_audience": str|null,
 "purpose": str|null, "major_sections": [str], "referenced_systems": [str],
 "referenced_products": [str], "referenced_policies": [str],
 "document_identifiers": [str], "owner": fact|null, "version": fact|null,
 "effective_date": fact|null, "review_date": fact|null}}"""


SEGMENTATION_SYSTEM = """TASK: semantic_segmentation
You divide an extracted internal document into semantic sections for a retrieval
system. The document is given as numbered blocks [B<n>] in reading order. Each block
shows its kind (heading with level, paragraph, list, table, code), page, size and text.
Long blocks are abbreviated with "[...]"; you only see previews. Never reproduce block
text; refer to blocks by number.

Return {"sections": [{"start_block": int, "end_block": int, "title": str,
"summary": str, "keywords": [str], "roles": [str], "context": str}]}

Rules:
1. Cover every block of the requested range exactly once and in order: the first
   start_block is the first block of the range, each start_block equals the previous
   end_block + 1, and the last end_block is the last block of the range.
2. Follow the document's structure. Start a new section at each heading. A section may
   contain deeper sub-headings of the heading it starts with, but never a heading of
   the same or a higher level (same or smaller level number) than the heading it
   belongs to: do not merge sibling or unrelated sections. Prefer the most specific
   subsection as a section; merge a sub-heading into its parent only when it is too
   short to be useful alone.
3. Keep numbered procedures, related bullet points, tables and the paragraph that
   introduces or explains them in the same section.
4. Where headings are missing or one heading covers several distinct topics, split at
   the topic change (on block boundaries).
5. Do not split only because a section is long; oversized sections are split later.
6. title: the heading text when the section starts with a heading, else a short
   descriptive title. summary: 1-2 sentences. keywords: 3-8 terms from the section.
   roles: job roles the section is relevant to when evident, else [].
   context: 1-2 sentences situating the section within the document, e.g. "This
   section of the IT Employee Onboarding Guide explains how new employees install the
   approved VS Code editor." Describe only what the section contains; do not add
   instructions, policies or facts that are not in the text."""


def metadata_prompt(
    *,
    department: str,
    filename: str,
    file_type: str,
    title: str,
    source_metadata: dict[str, Any],
    outline: list[str],
    excerpt: str,
    truncated: bool,
) -> str:
    source = json.dumps(source_metadata, ensure_ascii=False, default=str)[:4000]
    outline_text = "\n".join(outline) if outline else "(no headings detected)"
    note = " (excerpt; the document continues)" if truncated else ""
    return (
        f"HR-selected department: {department}\n"
        f"Filename: {filename}\nFile type: {file_type}\nExtracted title: {title}\n"
        f"Source metadata (from the file itself): {source}\n\n"
        f"Heading outline:\n{outline_text}\n\n"
        f"Document text{note}:\n<<<\n{excerpt}\n>>>"
    )


def segmentation_prompt(
    *, title: str, department: str, first: int, last: int, blocks: list[str]
) -> str:
    listing = "\n".join(blocks)
    return (
        f"Document: {title}\nDepartment: {department}\n"
        f"Segment blocks B{first} to B{last} (inclusive).\n\n{listing}"
    )
