"""POST /api/v1/rag/upload against the real app with mocked Fireworks and temp ChromaDB."""

from __future__ import annotations

import httpx
import pymupdf
import pytest
from fastapi import FastAPI, File, UploadFile

from src.config import Settings
from src.main import app
from src.middleware import BodySizeLimitMiddleware
from src.rag import routes
from src.rag.service import create_services

URL = "/api/v1/rag/upload"


def text_pdf() -> bytes:
    pdf = pymupdf.open()
    pdf.new_page().insert_text((72, 72), "Expense reports are due on the fifth of each month.")
    data = pdf.tobytes()
    pdf.close()
    return data


def blank_pdf() -> bytes:
    pdf = pymupdf.open()
    pdf.new_page()
    data = pdf.tobytes()
    pdf.close()
    return data


@pytest.fixture
def settings(tmp_path) -> Settings:
    return Settings(
        _env_file=None,
        fireworks_api_key="test-key",
        fireworks_reranker_model="fireworks/qwen3-reranker-8b",
        chroma_persist_dir=str(tmp_path / "chroma"),
        chroma_collection="test_upload",
        upload_max_file_bytes=1024,
    )


@pytest.fixture
async def api(settings, fake_fireworks, monkeypatch):
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


async def test_partial_success_returns_200_with_per_file_errors(api):
    files = [
        ("files", ("expenses.pdf", text_pdf(), "application/pdf")),
        ("files", ("scan.pdf", blank_pdf(), "application/pdf")),
        ("files", ("notes.md", b"# Travel\n\nBook flights via the portal.", "text/markdown")),
        ("files", ("big.txt", b"x " * 2000, "text/plain")),
        ("files", ("photo.png", b"\x89PNG....", "image/png")),
    ]
    response = await api.post(URL, data={"department": "Finance"}, files=files)
    assert response.status_code == 200
    body = response.json()
    assert body["uploaded"] == 2
    errors = {e["filename"]: e["message"] for e in body["errors"]}
    assert set(errors) == {"scan.pdf", "big.txt", "photo.png"}
    assert "OCR" in errors["scan.pdf"]
    assert "size limit" in errors["big.txt"]
    assert body["department"] == "Finance"
    statuses = {r["filename"]: r["status"] for r in body["results"]}
    assert statuses["expenses.pdf"] == "ingested" and statuses["notes.md"] == "ingested"
    results = {r["filename"]: r for r in body["results"]}
    notes = results["notes.md"]
    assert notes["department"] == "Finance" and notes["segmentation_method"] == "llm"
    assert {k: v["status"] for k, v in notes["stages"].items()} == {
        "validation": "succeeded",
        "extraction": "succeeded",
        "metadata": "succeeded",
        "chunking": "succeeded",
        "embedding": "succeeded",
        "persistence": "succeeded",
    }
    assert results["scan.pdf"]["stages"]["extraction"]["status"] == "failed"
    assert results["scan.pdf"]["stages"]["embedding"]["status"] == "not_run"
    assert results["big.txt"]["stages"]["validation"]["status"] == "failed"
    assert app.state.rag and await app.state.rag.store.count() == 2


async def test_reupload_reports_unchanged_as_uploaded(api):
    files = [("files", ("notes.txt", b"Payroll runs monthly.", "text/plain"))]
    await api.post(URL, data={"department": "Finance"}, files=files)
    body = (await api.post(URL, data={"department": "Finance"}, files=files)).json()
    assert body["uploaded"] == 1 and body["results"][0]["status"] == "unchanged"


@pytest.mark.parametrize("department", [None, "", "Marketing"])
async def test_invalid_department_is_400_with_string_detail(api, department):
    data = {"department": department} if department is not None else {}
    files = [("files", ("a.txt", b"hello", "text/plain"))]
    response = await api.post(URL, data=data, files=files)
    assert response.status_code == 400
    assert isinstance(response.json()["detail"], str)


async def test_no_files_is_400(api):
    response = await api.post(URL, data={"department": "Finance"})
    assert response.status_code == 400 and isinstance(response.json()["detail"], str)


async def test_too_many_files_is_400(api):
    files = [("files", (f"{i}.txt", b"hi", "text/plain")) for i in range(11)]
    response = await api.post(URL, data={"department": "Finance"}, files=files)
    assert response.status_code == 400 and "Too many files" in response.json()["detail"]


async def test_missing_api_key_is_503(monkeypatch):
    app.state.rag = None
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        files = [("files", ("a.txt", b"hello", "text/plain"))]
        response = await client.post(URL, data={"department": "Finance"}, files=files)
    assert response.status_code == 503 and isinstance(response.json()["detail"], str)


async def test_create_services_without_key_returns_none(tmp_path):
    settings = Settings(_env_file=None, fireworks_api_key="", chroma_persist_dir=str(tmp_path))
    assert await create_services(settings) is None


def small_app(limit: int) -> FastAPI:
    test_app = FastAPI()
    test_app.add_middleware(BodySizeLimitMiddleware, max_bytes=limit, path_prefixes=("/up",))

    @test_app.post("/up")
    async def up(files: list[UploadFile] = File(...)) -> dict:  # noqa: B008
        return {"n": len(files)}

    return test_app


async def test_request_body_limit_by_content_length():
    transport = httpx.ASGITransport(app=small_app(500))
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        ok = await client.post("/up", files=[("files", ("a.txt", b"x" * 10, "text/plain"))])
        big = await client.post("/up", files=[("files", ("a.txt", b"x" * 1000, "text/plain"))])
    assert ok.status_code == 200
    assert big.status_code == 413 and isinstance(big.json()["detail"], str)


async def test_request_body_limit_when_streamed_without_content_length():
    async def body():  # valid multipart; the file part is larger than the limit
        yield (
            b'--b\r\nContent-Disposition: form-data; name="files"; filename="a.txt"\r\n'
            b"Content-Type: text/plain\r\n\r\n"
        )
        for _ in range(10):
            yield b"x" * 100
        yield b"\r\n--b--\r\n"

    transport = httpx.ASGITransport(app=small_app(500))
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/up", content=body(), headers={"content-type": "multipart/form-data; boundary=b"}
        )
    assert response.status_code == 413


async def test_route_endpoint_uses_fusion(api, monkeypatch):
    async def fake_route(query):
        return {
            "query": query,
            "primary_department": "Finance",
            "selected_departments": ["Finance"],
            "predictions": [],
            "retrieved_chunks": [],
            "diagnostics": {},
        }

    monkeypatch.setattr(app.state.rag.fusion, "route", fake_route)
    response = await api.post("/api/v1/rag/route", json={"query": "expenses?"})
    assert response.status_code == 200 and response.json()["primary_department"] == "Finance"
