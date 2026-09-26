"""Citation viewer: rebuilding a document from its chunks, and GET /rag/documents/{id}."""

from __future__ import annotations

import json

import httpx
import pytest

from src.config import Settings
from src.main import app
from src.rag import routes
from src.rag.documents import build_document_view
from src.rag.service import create_services


def chunk(index: int, text: str, path: list[str], **meta) -> tuple[str, str, dict]:
    return (
        f"c{index}",
        text,
        {
            "document_id": "doc",
            "document_version": "v1",
            "title": "AI Tool Acceptable Use",
            "department": "Information Security",
            "ingested_at": "2026-09-01T00:00:00+00:00",
            "chunk_index": index,
            "block_start": index * 10,
            "block_end": index * 10 + 1,
            "heading_path_json": json.dumps(path),
            "heading_path_text": " > ".join(path),
            **meta,
        },
    )


def test_headings_are_restored_by_depth_and_title_is_dropped():
    title = "AI Tool Acceptable Use"
    view = build_document_view(
        "doc",
        [
            chunk(0, f"{title}\n\nIntro paragraph.", [title]),
            chunk(
                1, "3. Approved AI Tools\n\n- Copilot\n- Sandbox", [title, "3. Approved AI Tools"]
            ),
            chunk(2, "3.1 Sandbox\n\nUse it.", [title, "3. Approved AI Tools", "3.1 Sandbox"]),
        ],
    )
    assert [c.markdown for c in view.chunks] == [
        "Intro paragraph.",
        "## 3. Approved AI Tools\n\n- Copilot\n- Sandbox",
        "### 3.1 Sandbox\n\nUse it.",
    ]
    assert view.chunks[1].section == "3. Approved AI Tools"
    assert view.title == title and view.department == "Information Security"


def test_overlap_of_a_split_block_is_removed():
    first = chunk(0, "Alpha beta gamma delta epsilon zeta eta theta.", ["T"])
    second = chunk(1, "zeta eta theta. Iota kappa lambda.", ["T"])
    second[2]["block_start"] = first[2]["block_end"]  # same block continues
    view = build_document_view("doc", [first, second])
    assert view.chunks[1].markdown == "Iota kappa lambda."


def test_text_is_kept_when_blocks_differ():
    first = chunk(0, "Ends with the same words.", ["T"])
    second = chunk(1, "the same words. Starts a new block.", ["T"])
    view = build_document_view("doc", [first, second])
    assert view.chunks[1].markdown == "the same words. Starts a new block."


def test_only_the_newest_version_is_shown_during_reupload():
    old = chunk(0, "Old text.", ["T"])
    new = chunk(0, "New text.", ["T"], document_version="v2", ingested_at="2026-09-02T00:00:00")
    view = build_document_view("doc", [old, new])
    assert [c.markdown for c in view.chunks] == ["New text."]


@pytest.fixture
async def api(tmp_path, fake_fireworks, monkeypatch):
    settings = Settings(
        _env_file=None,
        fireworks_api_key="test-key",
        chroma_persist_dir=str(tmp_path / "chroma"),
        chroma_collection="test_documents",
    )
    monkeypatch.setattr(routes, "get_settings", lambda: settings)
    services = await create_services(
        settings, transport=httpx.MockTransport(fake_fireworks.handler)
    )
    app.state.rag = services
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    await services.aclose()
    app.state.rag = None


async def test_get_document_returns_rebuilt_markdown(api):
    content = (
        b"# Travel Policy\n\n## Booking\n\nBook flights via the portal.\n\n"
        b"- Economy class\n- Receipts required"
    )
    upload = await api.post(
        "/api/v1/rag/upload",
        data={"department": "Finance"},
        files=[("files", ("travel.md", content, "text/markdown"))],
    )
    document_id = upload.json()["results"][0]["document_id"]

    response = await api.get(f"/api/v1/rag/documents/{document_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Travel Policy"
    assert body["department"] == "Finance"
    assert body["source_filename"] == "travel.md"
    markdown = "\n\n".join(c["markdown"] for c in body["chunks"])
    assert "## Booking" in markdown
    assert "Book flights via the portal." in markdown
    assert "- Economy class\n- Receipts required" in markdown
    assert "Document:" not in markdown  # no contextual embedding header


async def test_unknown_document_is_404_with_string_detail(api):
    response = await api.get("/api/v1/rag/documents/missing")
    assert response.status_code == 404
    assert isinstance(response.json()["detail"], str)
