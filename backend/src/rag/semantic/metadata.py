"""Document-level metadata: source facts + DeepSeek enrichment, with grounding checks.

Resolution rules:

- The HR-selected department is authoritative. A department found in the file's own
  metadata or suggested by the LLM is recorded, never applied.
- Facts read from the file (front matter, document properties) win over LLM output.
  Disagreements are recorded in ``conflicts`` instead of being overwritten silently.
- Factual LLM fields (owner, version, dates) must quote verbatim evidence that exists
  in the document, and referenced systems/products/policies/identifiers must literally
  appear in it. Anything unsupported is dropped and listed in ``ungrounded_fields``.
- If DeepSeek is unavailable or keeps returning invalid output, the document keeps its
  source-only metadata (``llm_status="fallback"``) and ingestion continues.
"""

from __future__ import annotations

import logging
import re
from typing import Any

from src.rag.extraction import ExtractedDocument
from src.rag.fireworks import FireworksError, FireworksLLM
from src.rag.semantic.llm_json import StructuredOutputError, call_structured
from src.rag.semantic.prompts import METADATA_SYSTEM, metadata_prompt
from src.rag.semantic.schemas import (
    DocumentMetadata,
    LLMDocumentMetadata,
    MetadataConflict,
    SourceMetadata,
)

logger = logging.getLogger(__name__)

_SOURCE_ALIASES = {
    "title": ("title",),
    "owner": ("owner", "document_owner", "doc_owner", "policy_owner"),
    "version": ("version", "document_version", "doc_version"),
    "effective_date": ("effective_date", "effective", "effective_from", "valid_from"),
    "review_date": ("review_date", "next_review", "next_review_date", "review_by"),
    "department": ("department", "dept"),
    "document_identifiers": ("id", "document_id", "doc_id", "policy_id", "identifier", "ref"),
    "keywords": ("keywords", "tags"),
}
FACT_FIELDS = ("owner", "version", "effective_date", "review_date")
LITERAL_LIST_FIELDS = (
    "referenced_systems",
    "referenced_products",
    "referenced_policies",
    "document_identifiers",
)


def _norm(text: str) -> str:
    text = text.replace("’", "'").replace("“", '"').replace("”", '"')
    return " ".join(text.split()).casefold()


def _as_text(value: Any) -> str | None:
    if value is None or isinstance(value, dict):
        return None
    if isinstance(value, list):
        joined = ", ".join(str(v) for v in value if v not in (None, ""))
        return joined or None
    text = " ".join(str(value).split())
    return text or None


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    items = value if isinstance(value, list) else re.split(r"[,;]", str(value))
    return [" ".join(str(i).split()) for i in items if str(i).strip()]


def parse_source_metadata(raw: dict[str, Any]) -> SourceMetadata:
    """Map the file's own metadata keys onto canonical fields (values kept verbatim)."""
    by_key = {re.sub(r"[\s\-]+", "_", str(k).strip().casefold()): v for k, v in raw.items()}

    def lookup(field: str) -> Any:
        return next((by_key[a] for a in _SOURCE_ALIASES[field] if a in by_key), None)

    return SourceMetadata(
        raw=raw,
        title=_as_text(lookup("title")),
        owner=_as_text(lookup("owner")),
        version=_as_text(lookup("version")),
        effective_date=_as_text(lookup("effective_date")),
        review_date=_as_text(lookup("review_date")),
        department=_as_text(lookup("department")),
        document_identifiers=_as_list(lookup("document_identifiers")),
        keywords=_as_list(lookup("keywords")),
    )


def build_excerpt(doc: ExtractedDocument, max_chars: int) -> tuple[str, bool]:
    """The document text if it fits; otherwise its beginning plus the opening of each
    later section, so the model sees the whole structure within the budget."""
    if len(doc.text) <= max_chars:
        return doc.text, False
    head_budget = max_chars // 2
    parts = [doc.text[:head_budget]]
    used = head_budget
    for i, block in enumerate(doc.blocks):
        if block.start < head_budget or not block.is_heading:
            continue
        following = doc.blocks[i + 1] if i + 1 < len(doc.blocks) else None
        snippet = block.text
        if following is not None and not following.is_heading:
            snippet += "\n" + following.text[:300]
        if used + len(snippet) + 10 > max_chars:
            break
        parts.append(snippet)
        used += len(snippet) + 10
    return "\n[...]\n".join(parts), True


class MetadataGenerator:
    def __init__(
        self,
        llm: FireworksLLM | None,
        *,
        max_attempts: int = 3,
        max_input_chars: int = 20_000,
        llm_extra: dict[str, Any] | None = None,
    ) -> None:
        self.llm = llm
        self.max_attempts = max_attempts
        self.max_input_chars = max_input_chars
        self.llm_extra = llm_extra

    async def generate(
        self, doc: ExtractedDocument, department: str, filename: str
    ) -> DocumentMetadata:
        source = parse_source_metadata(doc.source_metadata)
        llm_result: LLMDocumentMetadata | None = None
        status, error = "skipped", None
        if self.llm is not None:
            try:
                llm_result, _ = await call_structured(
                    self.llm,
                    METADATA_SYSTEM,
                    self._prompt(doc, department, filename),
                    LLMDocumentMetadata,
                    max_attempts=self.max_attempts,
                    extra=self.llm_extra,
                )
                status = "succeeded"
            except (StructuredOutputError, FireworksError) as exc:
                logger.warning("Metadata generation failed for %s: %s", filename, exc)
                status, error = "fallback", _short_error(exc)
        return resolve_metadata(doc, department, source, llm_result, status, error)

    def _prompt(self, doc: ExtractedDocument, department: str, filename: str) -> str:
        excerpt, truncated = build_excerpt(doc, self.max_input_chars)
        outline = [f"{'  ' * max(level - 1, 0)}- {text}" for level, text, _ in doc.outline()]
        return metadata_prompt(
            department=department,
            filename=filename,
            file_type=doc.file_type,
            title=doc.title,
            source_metadata=doc.source_metadata,
            outline=outline[:200],
            excerpt=excerpt,
            truncated=truncated,
        )


def _short_error(exc: Exception) -> str:
    if isinstance(exc, StructuredOutputError):
        return f"DeepSeek returned invalid structured output after {exc.attempts} attempt(s)"
    return f"DeepSeek request failed: {str(exc)[:200]}"


def resolve_metadata(
    doc: ExtractedDocument,
    department: str,
    source: SourceMetadata,
    llm: LLMDocumentMetadata | None,
    llm_status: str,
    llm_error: str | None,
) -> DocumentMetadata:
    corpus = _norm(doc.text + "\n" + " ".join(str(v) for v in doc.source_metadata.values()))
    conflicts: list[MetadataConflict] = []
    ungrounded: list[str] = []

    if source.department and _norm(source.department) != _norm(department):
        conflicts.append(
            MetadataConflict(
                field="department",
                kept_value=department,
                kept_from="hr_selection",
                other_value=source.department,
                other_from="source",
            )
        )

    if llm is not None:
        llm = llm.model_copy(deep=True)
        for field in LITERAL_LIST_FIELDS:
            kept = [item for item in getattr(llm, field) if _norm(item) in corpus]
            ungrounded.extend(
                f"{field}: {item}" for item in getattr(llm, field) if item not in kept
            )
            setattr(llm, field, kept)
        for field in FACT_FIELDS:
            fact = getattr(llm, field)
            if fact is not None and not _is_grounded(fact.value, fact.evidence, corpus):
                ungrounded.append(f"{field}: {fact.value}")
                setattr(llm, field, None)

    facts: dict[str, Any] = {}
    for field in FACT_FIELDS:
        source_value = getattr(source, field)
        llm_fact = getattr(llm, field) if llm is not None else None
        if source_value:
            facts[field], facts[f"{field}_source"] = source_value, "source"
            if llm_fact is not None and _norm(llm_fact.value) != _norm(source_value):
                conflicts.append(
                    MetadataConflict(
                        field=field,
                        kept_value=source_value,
                        kept_from="source",
                        other_value=llm_fact.value,
                        other_from="llm",
                    )
                )
        elif llm_fact is not None:
            facts[field], facts[f"{field}_source"] = llm_fact.value, "llm_grounded"

    title, title_source = doc.title, doc.title_source
    if title_source == "filename" and llm is not None and llm.title:
        title, title_source = llm.title, "llm"
    elif title_source == "metadata" and llm is not None and llm.title:
        if _norm(llm.title) != _norm(title):
            conflicts.append(
                MetadataConflict(
                    field="title",
                    kept_value=title,
                    kept_from="source",
                    other_value=llm.title,
                    other_from="llm",
                )
            )

    outline = [text for level, text, _ in doc.outline() if level <= 2][:50]
    return DocumentMetadata(
        title=title,
        title_source=title_source,
        department=department,
        source=source,
        llm=llm,
        llm_status=llm_status,
        llm_error=llm_error,
        conflicts=conflicts,
        ungrounded_fields=ungrounded,
        source_outline=outline,
        **facts,
    )


def _is_grounded(value: str, evidence: str, corpus: str) -> bool:
    """Evidence must be a verbatim quote, and the value must be backed by it."""
    evidence_n = _norm(evidence).strip("\"' ")
    if len(evidence_n) < 3 or evidence_n not in corpus:
        return False
    value_n = _norm(value)
    if value_n in evidence_n:
        return True
    # Normalized dates ("2025-03-01" from "1 March 2025"): every number must be quoted.
    numbers = re.findall(r"\d+", value_n)
    return bool(numbers) and all(n.lstrip("0") in evidence_n for n in numbers)
