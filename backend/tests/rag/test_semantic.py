"""DeepSeek metadata, semantic segmentation, hierarchical chunks and serialization.

DeepSeek is mocked (``FakeFireworks`` chat completions); no network access.
"""

import json
import math

import pytest

from src.rag.extraction import extract_document
from src.rag.semantic.chunks import CoverageError, build_chunks, contextualize
from src.rag.semantic.metadata import MetadataGenerator
from src.rag.semantic.segmentation import (
    Section,
    SemanticSegmenter,
    make_windows,
    structural_sections,
    validate_sections,
)
from src.rag.semantic.serialization import flatten_metadata, unflatten_metadata
from src.rag.semantic.tokens import count_tokens, split_by_tokens
from tests.conftest import default_metadata

GUIDE = (
    "# IT Employee Onboarding Guide\n\n"  # B0 L1
    "Welcome to ACME. This guide is owned by the IT Service Desk.\n\n"  # B1
    "## Development Environment\n\n"  # B2 L2
    "Every developer gets the standard toolchain.\n\n"  # B3
    "### GitHub Copilot Setup\n\n"  # B4 L3
    "Request a Copilot seat through ServiceNow, then sign in with SSO.\n\n"  # B5
    "## Corporate Network\n\n"  # B6 L2
    "Connect with GlobalProtect before accessing internal systems.\n"  # B7
)


@pytest.fixture
async def guide():
    return await extract_document("it-guide.md", GUIDE.encode())


# ------------------------------------------------------------------ metadata


async def test_metadata_generation_keeps_hr_department(guide, llm, fake_fireworks):
    answer = default_metadata(
        "Extracted title: IT Employee Onboarding Guide\nHR-selected department: IT Operations"
    )
    answer.update(
        suggested_primary_department="Software Engineering",
        secondary_departments=["software engineering", "Not A Department"],
        document_type="Guide",
        referenced_systems=["ServiceNow", "GlobalProtect", "Jira"],  # Jira is not in the text
    )
    fake_fireworks.chat_queue["metadata"] = [answer]
    meta = await MetadataGenerator(llm).generate(guide, "IT Operations", "it-guide.md")
    assert meta.llm_status == "succeeded" and meta.llm_error is None
    assert meta.department == "IT Operations"  # HR selection is authoritative
    assert meta.llm.suggested_primary_department == "Software Engineering"  # kept only as metadata
    assert meta.llm.secondary_departments == ["Software Engineering"]
    assert meta.llm.document_type == "guide"
    assert meta.llm.referenced_systems == ["ServiceNow", "GlobalProtect"]
    assert "referenced_systems: Jira" in meta.ungrounded_fields
    assert meta.title == "IT Employee Onboarding Guide" and meta.title_source == "heading"
    assert meta.source_outline[:2] == ["IT Employee Onboarding Guide", "Development Environment"]


async def test_missing_metadata_stays_null(guide, llm):
    meta = await MetadataGenerator(llm).generate(guide, "IT Operations", "it-guide.md")
    assert meta.llm_status == "succeeded"
    for field in ("owner", "version", "effective_date", "review_date"):
        assert getattr(meta, field) is None and getattr(meta, f"{field}_source") is None
    assert meta.conflicts == []


async def test_facts_need_verbatim_evidence_and_source_wins(llm, fake_fireworks):
    md = "---\nversion: 3.0\n---\n# Travel Policy\n\nOwned by the Finance Operations team.\n"
    doc = await extract_document("travel.md", md.encode())
    answer = default_metadata("Extracted title: Travel Policy\nHR-selected department: Finance")
    answer.update(
        owner={"value": "Finance Operations", "evidence": "Owned by the Finance Operations team"},
        version={"value": "4.0", "evidence": "version 3.0"},
        effective_date={"value": "2025-01-01", "evidence": "Effective 1 January 2025"},
    )
    fake_fireworks.chat_queue["metadata"] = [answer]
    meta = await MetadataGenerator(llm).generate(doc, "Finance", "travel.md")
    assert (meta.owner, meta.owner_source) == ("Finance Operations", "llm_grounded")
    assert (meta.version, meta.version_source) == ("3.0", "source")
    assert meta.effective_date is None  # evidence is not in the document -> dropped
    assert "effective_date: 2025-01-01" in meta.ungrounded_fields
    # "version 3.0" is not verbatim text either, so the LLM value is dropped, not conflicted
    assert "version: 4.0" in meta.ungrounded_fields


async def test_source_conflicts_are_recorded(llm, fake_fireworks):
    md = "---\nversion: 3.0\ndepartment: Legal\n---\n# Travel Policy\n\nVersion 4.0 applies.\n"
    doc = await extract_document("travel.md", md.encode())
    answer = default_metadata("Extracted title: Travel Policy\nHR-selected department: Finance")
    answer["version"] = {"value": "4.0", "evidence": "Version 4.0 applies."}
    fake_fireworks.chat_queue["metadata"] = [answer]
    meta = await MetadataGenerator(llm).generate(doc, "Finance", "travel.md")
    assert meta.department == "Finance" and meta.version == "3.0"
    conflicts = {c.field: c for c in meta.conflicts}
    assert conflicts["department"].other_value == "Legal"
    assert conflicts["department"].kept_from == "hr_selection"
    assert (conflicts["version"].kept_value, conflicts["version"].other_value) == ("3.0", "4.0")


async def test_invalid_json_is_retried_then_accepted(guide, llm, fake_fireworks):
    fake_fireworks.chat_queue["metadata"] = ["not json", {"document_type": 5, "topics": "x"}]
    meta = await MetadataGenerator(llm, max_attempts=3).generate(guide, "IT Operations", "a.md")
    assert meta.llm_status == "succeeded"
    assert fake_fireworks.chat_calls("metadata") == 3
    retry_prompt = fake_fireworks.requests[-1]["body"]["messages"][1]["content"]
    assert "previous response was rejected" in retry_prompt


async def test_invalid_output_falls_back_to_source_metadata(guide, llm, fake_fireworks):
    fake_fireworks.chat_queue["metadata"] = ["{", "{", "{"]
    meta = await MetadataGenerator(llm, max_attempts=3).generate(guide, "IT Operations", "a.md")
    assert meta.llm_status == "fallback" and meta.llm is None
    assert "invalid structured output after 3" in meta.llm_error
    assert meta.title == "IT Employee Onboarding Guide" and meta.department == "IT Operations"


async def test_api_failure_falls_back(guide, llm, fake_fireworks):
    fake_fireworks.chat_queue["metadata"] = [400]
    meta = await MetadataGenerator(llm).generate(guide, "IT Operations", "a.md")
    assert meta.llm_status == "fallback" and "request failed" in meta.llm_error


async def test_no_llm_skips_metadata(guide):
    meta = await MetadataGenerator(None).generate(guide, "IT Operations", "a.md")
    assert meta.llm_status == "skipped" and meta.llm is None


# -------------------------------------------------------------- segmentation


def test_boundary_validation(guide):
    blocks = guide.blocks
    assert len(blocks) == 8
    assert validate_sections([(0, 1), (2, 5), (6, 7)], blocks, 0, 7) == []
    assert any("B2-B2 are missing" in p for p in validate_sections([(0, 1), (3, 7)], blocks, 0, 7))
    overlap = validate_sections([(0, 2), (2, 5), (6, 7)], blocks, 0, 7)
    assert any("duplicated" in p for p in overlap)
    merged = validate_sections([(0, 1), (2, 7)], blocks, 0, 7)
    assert any("merges B6" in p for p in merged)  # sibling "Corporate Network" heading
    assert any("outside" in p for p in validate_sections([(0, 9)], blocks, 0, 7))
    assert any("missing" in p for p in validate_sections([(0, 5)], blocks, 0, 7))
    assert validate_sections([], blocks, 0, 7) == ["No sections were returned"]


async def test_llm_segmentation_is_used_and_heading_only_sections_merge(guide, llm, fake_fireworks):
    sections = [
        {"start_block": 0, "end_block": 1, "title": "Welcome", "context": "Intro."},
        {"start_block": 2, "end_block": 2, "title": "Dev"},  # heading only -> merged forward
        {"start_block": 3, "end_block": 5, "title": "Toolchain and Copilot"},
        {"start_block": 6, "end_block": 7, "title": "Network"},
    ]
    fake_fireworks.chat_queue["segmentation"] = [{"sections": sections}]
    result = await SemanticSegmenter(llm).segment(guide, title=guide.title, department="IT")
    assert result.method == "llm" and result.windows == 1 and result.llm_attempts == 1
    assert [(s.start, s.end) for s in result.sections] == [(0, 1), (2, 5), (6, 7)]
    assert result.sections[1].title == "Toolchain and Copilot"
    prompt = fake_fireworks.requests[-1]["body"]["messages"][1]["content"]
    assert "[B4] heading L3" in prompt and "Segment blocks B0 to B7" in prompt


async def test_invalid_boundaries_retry_then_structural_fallback(guide, llm, fake_fireworks):
    gap = {"sections": [{"start_block": 0, "end_block": 1}, {"start_block": 4, "end_block": 7}]}
    fake_fireworks.chat_queue["segmentation"] = [gap, gap, gap]
    result = await SemanticSegmenter(llm, max_attempts=3).segment(
        guide, title=guide.title, department="IT"
    )
    assert result.method == "structural" and result.llm_attempts == 3
    assert "missing" in result.fallback_reasons[0]
    assert result.sections == structural_sections(guide.blocks, 0, 7)
    assert all(s.method == "structural" for s in result.sections)


async def test_long_documents_are_windowed_and_capped(llm, fake_fireworks):
    body = "Paragraph text about onboarding. " * 5
    md = "".join(f"# Part {i}\n\n{body}\n\n## Detail {i}\n\n{body}\n\n" for i in range(6))
    doc = await extract_document("long.md", md.encode())
    windows = make_windows(doc.blocks, budget_chars=700, preview_chars=240)
    assert len(windows) > 2
    assert windows[0][0] == 0 and windows[-1][1] == len(doc.blocks) - 1
    for (_, end), (start, _) in zip(windows, windows[1:], strict=False):
        assert start == end + 1 and doc.blocks[start].is_heading
    segmenter = SemanticSegmenter(llm, window_chars=700, max_windows=2)
    result = await segmenter.segment(doc, title=doc.title, department="IT")
    assert result.method == "mixed" and result.llm_windows == 2
    assert fake_fireworks.chat_calls("segmentation") == 2  # capped: no calls beyond the limit
    assert any("2-window limit" in r for r in result.fallback_reasons)
    ranges = [(s.start, s.end) for s in result.sections]
    assert validate_sections(ranges, doc.blocks, 0, len(doc.blocks) - 1) == []


# -------------------------------------------------------------------- chunks


async def test_hierarchical_chunks_and_contextualized_text(guide):
    sections = [
        Section(0, 1, "llm", title="Welcome"),
        Section(2, 3, "llm", title="Dev environment"),
        Section(
            4,
            5,
            "llm",
            title="Copilot",
            summary="How to get Copilot.",
            context="This section explains how new employees get GitHub Copilot.",
        ),
        Section(6, 7, "llm", title="Network"),
    ]
    chunks = build_chunks(guide, sections, max_tokens=450, overlap_tokens=40)
    assert len(chunks) == 4
    copilot = chunks[2]
    assert copilot.heading_path == (
        "IT Employee Onboarding Guide",
        "Development Environment",
        "GitHub Copilot Setup",
    )
    assert copilot.section_title == "GitHub Copilot Setup"
    assert copilot.section_title_source == "source"
    assert copilot.parent_section == "Development Environment"
    assert copilot.content == (
        "### GitHub Copilot Setup".removeprefix("### ")
        + "\n\nRequest a Copilot seat through ServiceNow, then sign in with SSO."
    )
    assert copilot.content in guide.text  # original text, not rewritten
    text = contextualize(copilot, title=guide.title, department="IT Operations")
    assert text == (
        "Document: IT Employee Onboarding Guide\n"
        "Department: IT Operations\n"
        "Section: Development Environment\n"
        "Subsection: GitHub Copilot Setup\n\n"
        "This section explains how new employees get GitHub Copilot.\n\n"
        f"{copilot.content}"
    )
    assert "\n".join(c.content for c in chunks).count("Request a Copilot seat") == 1


async def test_oversized_section_splits_on_structure_then_tokens():
    sentence = "Employees must complete the security training module before access is granted. "
    md = (
        "# Security\n\n"
        "Follow these steps:\n\n- Enable MFA\n- Register your laptop\n\n"
        f"{sentence * 60}\n\n"
        "## Passwords\n\nUse a password manager.\n"
    )
    doc = await extract_document("security.md", md.encode())
    one_section = [Section(0, len(doc.blocks) - 1, "structural")]
    chunks = build_chunks(doc, one_section, max_tokens=120, overlap_tokens=20)
    assert len(chunks) > 4
    assert all(c.token_count <= 120 + 20 for c in chunks)
    assert {c.part_count for c in chunks} == {len(chunks)}
    lead_in = next(c for c in chunks if "Follow these steps:" in c.content)
    assert "- Enable MFA" in lead_in.content  # a lead-in stays with its list
    passwords = chunks[-1]
    assert passwords.heading_path[-1] == "Passwords"
    assert "Use a password manager." in passwords.content
    long_parts = [c for c in chunks if "security training" in c.content]
    assert len(long_parts) >= 3 and all(c.content in doc.text for c in long_parts)


async def test_coverage_error_on_missing_blocks(guide):
    with pytest.raises(CoverageError, match="block 2 is missing"):
        build_chunks(guide, [Section(0, 1, "llm"), Section(3, 7, "llm")])


def test_token_slices_cover_text_with_overlap():
    text = " ".join(f"word{i}." for i in range(500))
    slices = split_by_tokens(text, max_tokens=100, overlap_tokens=10)
    assert slices[0].start == 0 and slices[-1].end == len(text)
    for prev, nxt in zip(slices, slices[1:], strict=False):
        assert nxt.core_start == prev.end and nxt.start < nxt.core_start
    assert all(count_tokens(text[s.start : s.end]) <= 110 for s in slices)


# ------------------------------------------------------------- serialization


def test_chroma_metadata_is_scalar_only():
    values = {
        "title": "Guide",
        "chunk_index": 3,
        "score": 0.5,
        "is_part": True,
        "heading_path": ("A", "B"),
        "src_raw": {"owner": "IT", "tags": ["x"]},
        "owner": None,
    }
    flat = flatten_metadata(values)
    assert all(isinstance(v, str | int | float | bool) for v in flat.values())
    assert "owner" not in flat and "heading_path" not in flat
    assert json.loads(flat["heading_path_json"]) == ["A", "B"]
    restored = unflatten_metadata(flat)
    assert restored["heading_path"] == ["A", "B"] and restored["src_raw"]["tags"] == ["x"]
    with pytest.raises(ValueError):
        flatten_metadata({"x": math.nan})
    with pytest.raises(TypeError):
        flatten_metadata({"x": object()})
