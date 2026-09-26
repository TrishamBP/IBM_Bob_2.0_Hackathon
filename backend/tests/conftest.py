"""Shared fixtures: a mocked Fireworks API (httpx.MockTransport) and temporary stores."""

from __future__ import annotations

import asyncio
import hashlib
import json
import re
from collections.abc import Callable
from dataclasses import dataclass, field

import httpx
import numpy as np
import pytest

from src.chroma.client import ChromaStore
from src.rag.fireworks import (
    FireworksClient,
    FireworksEmbeddings,
    FireworksLLM,
    FireworksReranker,
)

DIMS = 356
MODEL = "fireworks/qwen3-embedding-8b"


def fake_vector(text: str, dims: int) -> list[float]:
    """Deterministic, un-normalized pseudo-embedding (bag of hashed words)."""
    vec = np.zeros(dims)
    for word in re.findall(r"[a-z0-9]+", text.lower()):
        vec[int(hashlib.md5(word.encode()).hexdigest(), 16) % dims] += 1.0
    vec += 0.01  # never all-zero
    return (vec * 40.0).tolist()  # mimic Fireworks' non-unit norm


def overlap_score(query: str, document: str) -> float:
    q = set(re.findall(r"[a-z0-9]+", query.lower()))
    d = set(re.findall(r"[a-z0-9]+", document.lower()))
    return len(q & d) / max(len(q), 1)


_BLOCK_LINE = re.compile(r"^\[B(\d+)\] (heading L\d+|\w+)", re.MULTILINE)
_RANGE_LINE = re.compile(r"Segment blocks B(\d+) to B(\d+)")


def default_metadata(user: str) -> dict:
    """Plausible DeepSeek metadata: echoes the prompt's title and department."""
    title = re.search(r"Extracted title: (.*)", user).group(1)
    department = re.search(r"HR-selected department: (.*)", user).group(1)
    return {
        "title": title,
        "document_type": "guide",
        "suggested_primary_department": department,
        "secondary_departments": [],
        "relevant_roles": ["New employee"],
        "topics": [title],
        "keywords": title.lower().split()[:5],
        "summary": f"Describes {title}.",
        "intended_audience": "New employees",
        "purpose": f"Explain {title}.",
        "major_sections": [],
        "referenced_systems": [],
        "referenced_products": [],
        "referenced_policies": [],
        "document_identifiers": [],
        "owner": None,
        "version": None,
        "effective_date": None,
        "review_date": None,
    }


def default_segmentation(user: str) -> dict:
    """Valid DeepSeek-style segmentation: one section per heading of the window."""
    first, last = map(int, _RANGE_LINE.search(user).groups())
    starts = [first] + [
        int(i) for i, kind in _BLOCK_LINE.findall(user) if kind.startswith("heading")
    ]
    starts = sorted({s for s in starts if first <= s <= last})
    ends = [s - 1 for s in starts[1:]] + [last]
    return {
        "sections": [
            {
                "start_block": start,
                "end_block": end,
                "title": f"Section B{start}",
                "summary": f"Blocks {start} to {end}.",
                "keywords": ["onboarding"],
                "roles": [],
                "context": f"This section covers blocks {start} to {end}.",
            }
            for start, end in zip(starts, ends, strict=True)
        ]
    }


def chat_task(body: dict) -> str:
    system = body["messages"][0]["content"]
    if body.get("stream"):
        return "answer"
    if system.startswith("TASK: document_metadata"):
        return "metadata"
    if system.startswith("TASK: semantic_"):
        return "segmentation"
    if "search query specialist" in system:
        return "expansion"
    if "technical writer" in system:
        return "hyde"
    if "standalone search query" in system:
        return "resolve"
    raise AssertionError(f"unknown chat task: {system[:80]!r}")


def default_expansion(user: str) -> dict:
    query = re.search(r"Original employee question:\n(.*)", user).group(1)
    return {"queries": [f"{query} steps", f"{query} procedure", f"{query} requirements"]}


def default_hyde(user: str) -> dict:
    query = re.search(r"Employee question:\n(.*)", user).group(1)
    return {"document": f"This internal article explains {query}. " * 4}


def default_resolve(user: str) -> dict:
    message = user.rsplit("Latest employee message:\n", 1)[1].strip()
    return {"query": message}


def default_answer(user: str) -> str:
    return "Follow the documented steps [S1]."


DEFAULTS = {
    "metadata": default_metadata,
    "segmentation": default_segmentation,
    "expansion": default_expansion,
    "hyde": default_hyde,
    "resolve": default_resolve,
    "answer": default_answer,
}


def _tokens(text: str) -> list[str]:
    """Split into small pieces like a model stream (keeps whitespace)."""
    return re.findall(r"\S+\s*|\s+", text)


class _SSEStream(httpx.AsyncByteStream):
    def __init__(self, chunks: list[bytes], fail_after: int | None, delay: float) -> None:
        self.chunks, self.fail_after, self.delay = chunks, fail_after, delay

    async def __aiter__(self):
        for i, chunk in enumerate(self.chunks):
            if self.fail_after is not None and i >= self.fail_after:
                raise httpx.ReadError("connection reset")
            if self.delay:
                await asyncio.sleep(self.delay)
            yield chunk


@dataclass
class FakeFireworks:
    """Mock Fireworks server. Override behaviour with ``fail_next`` or ``embedding_dims``.

    Chat completions answer per task (see :func:`chat_task`) with the ``DEFAULTS``.
    Queue overrides in ``chat_queue`` keyed by task: a dict/str is returned as the message
    content, an int as an HTTP error status. For the streamed "answer" task a str is split
    into tokens, or a dict ``{"tokens": [...], "reasoning": [...], "fail_after": n,
    "delay": s}`` controls the stream.
    """

    embedding_dims: int | None = None  # None -> honour the requested dimensions
    fail_next: list[int] = field(default_factory=list)  # status codes to return first
    fail_embeddings: list[int] = field(default_factory=list)  # embedding-only failures
    chat_queue: dict[str, list] = field(default_factory=dict)
    requests: list[dict] = field(default_factory=list)

    def handler(self, request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        self.requests.append({"path": request.url.path, "body": body})
        if self.fail_next:
            return httpx.Response(self.fail_next.pop(0), json={"error": {"message": "boom"}})
        if request.url.path.endswith("/chat/completions"):
            return self._chat(body)
        if request.url.path.endswith("/embeddings") and self.fail_embeddings:
            status = self.fail_embeddings.pop(0)
            return httpx.Response(status, json={"error": {"message": "boom"}})
        if request.url.path.endswith("/embeddings"):
            inputs = body["input"] if isinstance(body["input"], list) else [body["input"]]
            dims = self.embedding_dims or body.get("dimensions", 4096)
            data = [
                {"index": i, "object": "embedding", "embedding": fake_vector(t, dims)}
                for i, t in enumerate(inputs)
            ]
            data.reverse()  # the client must reorder by index
            return httpx.Response(200, json={"data": data, "model": body["model"]})
        if request.url.path.endswith("/rerank"):
            scores = [overlap_score(body["query"], d) for d in body["documents"]]
            order = sorted(range(len(scores)), key=lambda i: -scores[i])
            data = [{"index": i, "relevance_score": scores[i]} for i in order]
            return httpx.Response(200, json={"object": "list", "data": data})
        return httpx.Response(404, json={"error": "not found"})

    def _chat(self, body: dict) -> httpx.Response:
        user = body["messages"][-1]["content"]
        task = chat_task(body)
        queue = self.chat_queue.get(task)
        if queue:
            answer = queue.pop(0)
            if isinstance(answer, int):
                return httpx.Response(answer, json={"error": {"message": "boom"}})
        else:
            answer = DEFAULTS[task](user)
        if task == "answer":
            return self._stream_answer(body, answer)
        content = answer if isinstance(answer, str) else json.dumps(answer)
        return httpx.Response(
            200, json={"choices": [{"message": {"role": "assistant", "content": content}}]}
        )

    def _stream_answer(self, body: dict, answer) -> httpx.Response:
        """GLM-style SSE: reasoning deltas first, then content deltas, usage, [DONE]."""
        assert body.get("stream") is True
        spec = answer if isinstance(answer, dict) else {"tokens": _tokens(answer)}
        frames = [
            {"choices": [{"index": 0, "delta": {"reasoning_content": r}}]}
            for r in spec.get("reasoning", ["Thinking about the documents."])
        ]
        frames += [{"choices": [{"index": 0, "delta": {"content": t}}]} for t in spec["tokens"]]
        frames.append(
            {
                "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
                "usage": {"prompt_tokens": 100, "completion_tokens": len(spec["tokens"])},
            }
        )
        chunks = [f"data: {json.dumps(f)}\n\n".encode() for f in frames]
        chunks.append(b"data: [DONE]\n\n")
        return httpx.Response(
            200,
            headers={"content-type": "text/event-stream"},
            stream=_SSEStream(chunks, spec.get("fail_after"), spec.get("delay", 0.0)),
        )

    @property
    def embedding_calls(self) -> int:
        return sum(r["path"].endswith("/embeddings") for r in self.requests)

    def chat_calls(self, task: str | None = None) -> int:
        return sum(
            r["path"].endswith("/chat/completions")
            and (task is None or chat_task(r["body"]) == task)
            for r in self.requests
        )

    def chat_requests(self, task: str) -> list[dict]:
        return [
            r["body"]
            for r in self.requests
            if r["path"].endswith("/chat/completions") and chat_task(r["body"]) == task
        ]


@pytest.fixture
def fake_fireworks() -> FakeFireworks:
    return FakeFireworks()


@pytest.fixture
def make_client(fake_fireworks: FakeFireworks) -> Callable[..., FireworksClient]:
    def factory(**kwargs) -> FireworksClient:
        kwargs.setdefault("backoff_base", 0.0)
        return FireworksClient(
            "test-key", transport=httpx.MockTransport(fake_fireworks.handler), **kwargs
        )

    return factory


@pytest.fixture
async def client(make_client):
    async with make_client() as c:
        yield c


@pytest.fixture
def embedder(client: FireworksClient) -> FireworksEmbeddings:
    return FireworksEmbeddings(
        client, MODEL, DIMS, batch_size=4, max_concurrency=2, query_instruction="Find docs"
    )


@pytest.fixture
def reranker(client: FireworksClient) -> FireworksReranker:
    return FireworksReranker(client, "fireworks/qwen3-reranker-8b", max_candidates=40)


@pytest.fixture
def llm(client: FireworksClient) -> FireworksLLM:
    return FireworksLLM(client, "accounts/fireworks/models/deepseek-v4p1-flash", max_tokens=512)


@pytest.fixture
async def store(tmp_path) -> ChromaStore:
    s = ChromaStore(
        tmp_path / "chroma", "test_collection", embedding_model=MODEL, embedding_dimensions=DIMS
    )
    await s.open()
    return s
