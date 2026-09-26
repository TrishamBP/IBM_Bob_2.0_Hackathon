"""GLM streaming, Fireworks SSE client, evidence context and citation validation."""

import httpx
import pytest

from src.rag.fireworks import FireworksAPIError, FireworksClient, FireworksError
from src.rag.generation import (
    AnswerLLM,
    GenerationStats,
    build_sources,
    format_documents,
    sse_event,
    validate_citations,
)
from src.rag.retrieval.filtering import Candidate

GLM = "accounts/fireworks/models/glm-5p3-flash"


def candidate(i: int, text: str = "Install GlobalProtect.", **meta) -> Candidate:
    base = {
        "title": "VPN Guide",
        "department": "IT Operations",
        "heading_path_text": "VPN Guide > Connecting",
        "section_heading": "Connecting",
        "source_filename": "vpn.pdf",
        "page_start": 2,
        "page_end": 3,
        "document_id": f"doc{i}",
        "doc_version": "1.2",
        "llm_summary": "SUMMARY MUST NOT APPEAR",
        "contextualized_text": "CONTEXT MUST NOT APPEAR",
    }
    return Candidate(f"c{i}", text, {**base, **meta})


# ------------------------------------------------------------------ streaming


async def test_glm_stream_yields_content_only_and_captures_usage(client, fake_fireworks):
    fake_fireworks.chat_queue["answer"] = [
        {"tokens": ["Use ", "GlobalProtect ", "[S1]."], "reasoning": ["secret plan"]}
    ]
    llm = AnswerLLM(client, GLM)
    stats = GenerationStats()
    tokens = [t async for t in llm.stream([{"role": "user", "content": "q"}], stats)]
    assert tokens == ["Use ", "GlobalProtect ", "[S1]."]
    assert "secret" not in "".join(tokens)
    assert stats.finish_reason == "stop" and stats.usage["completion_tokens"] == 3
    body = fake_fireworks.chat_requests("answer")[0]
    assert body["model"] == GLM and body["stream"] is True


async def test_stream_retries_429_before_first_byte(make_client, fake_fireworks):
    fake_fireworks.fail_next = [429, 503]
    async with make_client(max_retries=3) as client:
        tokens = [
            t async for t in AnswerLLM(client, GLM).stream([{"role": "user", "content": "q"}])
        ]
    assert "".join(tokens) == "Follow the documented steps [S1]."
    assert len(fake_fireworks.requests) == 3


async def test_stream_gives_up_after_bounded_retries(make_client, fake_fireworks):
    fake_fireworks.fail_next = [429, 429, 429]
    async with make_client(max_retries=1) as client:
        with pytest.raises(FireworksAPIError) as info:
            async for _ in AnswerLLM(client, GLM).stream([{"role": "user", "content": "q"}]):
                pass
    assert info.value.status_code == 429 and len(fake_fireworks.requests) == 2


async def test_stream_failure_after_output_is_not_retried(client, fake_fireworks):
    fake_fireworks.chat_queue["answer"] = [{"tokens": ["a ", "b ", "c"], "fail_after": 3}]
    received = []
    with pytest.raises(FireworksError, match="interrupted"):
        async for token in AnswerLLM(client, GLM).stream([{"role": "user", "content": "q"}]):
            received.append(token)
    assert received == ["a ", "b "] and len(fake_fireworks.requests) == 1


async def test_stream_non_retryable_error():
    def handler(request):
        return httpx.Response(400, json={"error": {"message": "bad model"}})

    async with FireworksClient("k", transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(FireworksAPIError, match="bad model"):
            async for _ in client.stream_sse("chat/completions", {"model": "x"}):
                pass


# -------------------------------------------------------------------- context


def test_sources_have_markers_sections_and_no_summaries():
    sources = build_sources([candidate(1), candidate(2, "Restart the client.")], 4000)
    assert [s.citation_id for s in sources] == ["S1", "S2"]
    s1 = sources[0]
    assert s1.reference == "VPN Guide — Connecting" and s1.version == "1.2"
    assert s1.url is None  # no real link in the metadata -> none invented
    docs = format_documents(sources)
    assert docs.startswith("[S1] VPN Guide — Connecting\nDepartment: IT Operations")
    assert "vpn.pdf, p. 2-3" in docs
    assert "MUST NOT APPEAR" not in docs
    public = s1.public()
    assert "text" not in public and public["id"] == "S1"


def test_real_urls_only():
    linked = candidate(1, source_url="https://wiki.acme.example/vpn")
    fake = candidate(2, source_url="upload://IT/vpn.pdf")
    sources = build_sources([linked, fake], 4000)
    assert sources[0].url == "https://wiki.acme.example/vpn" and sources[1].url is None


def test_token_budget_truncates_first_and_skips_what_does_not_fit():
    long = candidate(1, "word " * 3000)
    sources = build_sources([long, candidate(2)], 500)
    assert len(sources) == 1  # an oversized first chunk is truncated, not dropped
    assert sources[0].text.endswith("…") and len(sources[0].text.split()) < 600
    tight = build_sources([candidate(1), candidate(2, "word " * 3000)], 200)
    assert [s.chunk_id for s in tight] == ["c1"]


# ------------------------------------------------------------------ citations


def test_citation_validation_removes_invalid_markers():
    sources = build_sources([candidate(1), candidate(2)], 4000)
    answer = "Install it [S1]. Then restart [S2, S7]. Ask IT [S9].\n\nDone [S1][S1]."
    check = validate_citations(answer, sources)
    assert check.cited == ["S1", "S2"] and check.invalid == ["S7", "S9"]
    assert check.content == "Install it [S1]. Then restart [S2]. Ask IT.\n\nDone [S1]."


def test_answer_without_citations_is_kept():
    check = validate_citations("General tip: restart your laptop.", [])
    assert check.cited == [] and check.content == "General tip: restart your laptop."


def test_sse_event_framing():
    frame = sse_event("token", {"text": "line1\nline2"})
    assert frame == 'event: token\ndata: {"text":"line1\\nline2"}\n\n'
