"""The tracing façade must be a transparent no-op when tracing is off."""

from __future__ import annotations

from src.observability import observe, tracing, update_llm, update_span, update_trace


async def test_decorated_functions_work_without_tracing(monkeypatch):
    monkeypatch.setattr(tracing._state, "enabled", False)

    @observe("tool", name="add")
    async def add(a: int, b: int) -> int:
        update_span(input="x", output="y", extra=1)
        update_trace(outcome="ok")
        update_llm(model="m", usage={"prompt_tokens": 1})
        return a + b

    @observe("llm")
    async def tokens():
        for t in ("a", "b"):
            yield t

    @observe()
    def sync(x: int) -> int:
        return x * 2

    assert await add(1, 2) == 3
    assert [t async for t in tokens()] == ["a", "b"]
    assert sync(4) == 8
    assert add.__name__ == "add"
