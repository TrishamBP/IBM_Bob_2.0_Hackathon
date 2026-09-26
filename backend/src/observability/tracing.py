"""LLM tracing for the RAG pipeline, backed by deepeval when it is installed.

deepeval is a development dependency (``uv sync --group eval``). Without it, or with
``TRACING_ENABLED=false``, every helper here is a no-op and ``observe`` returns the
original function's result unchanged, so production installs carry no tracing cost.

Only spans created through :func:`observe` are traced. Each finished trace whose root
span was declared with ``root=True`` (the chat turn) is printed to the terminal as a
span tree and handed to any registered listeners (the evaluation harness uses one to
collect retrieval context). Traces are uploaded to Confident AI only when
``CONFIDENT_API_KEY`` is set; otherwise nothing leaves the process.
"""

from __future__ import annotations

import functools
import inspect
import logging
import os
from collections.abc import Callable
from typing import Any

logger = logging.getLogger(__name__)

TraceListener = Callable[[Any], None]


class _State:
    enabled = False
    terminal = True
    preview_chars = 160
    root_names: set[str] = set()
    listeners: list[TraceListener] = []
    deepeval: Any = None  # the deepeval.tracing module once configured


_state = _State()


def configure_tracing(
    *, enabled: bool = True, terminal: bool = True, preview_chars: int = 160
) -> bool:
    """Enable tracing if deepeval is importable. Returns whether tracing is active."""
    _state.terminal = terminal
    _state.preview_chars = preview_chars
    if not enabled:
        _state.enabled = False
        return False
    if _state.deepeval is not None:
        _state.enabled = True
        return True
    # Must be set before deepeval is imported: its settings are read at import time.
    os.environ.setdefault("DEEPEVAL_TELEMETRY_OPT_OUT", "YES")
    os.environ.setdefault("CONFIDENT_TRACE_FLUSH", "NO")
    if not os.environ.get("CONFIDENT_API_KEY"):
        os.environ.setdefault("CONFIDENT_TRACE_VERBOSE", "NO")
    try:
        import deepeval.tracing as deepeval_tracing
    except ImportError:
        logger.info("deepeval is not installed; LLM tracing is disabled")
        return False
    _install_exporter(deepeval_tracing.trace_manager)
    _state.deepeval = deepeval_tracing
    _state.enabled = True
    logger.info("LLM tracing enabled (deepeval); terminal output=%s", terminal)
    return True


def tracing_active() -> bool:
    return _state.enabled


def add_trace_listener(listener: TraceListener) -> None:
    _state.listeners.append(listener)


def remove_trace_listener(listener: TraceListener) -> None:
    if listener in _state.listeners:
        _state.listeners.remove(listener)


# ---------------------------------------------------------------------------
# Decorator
# ---------------------------------------------------------------------------


def observe(span_type: str | None = None, *, name: str | None = None, root: bool = False):
    """Trace a coroutine function or async generator as a span.

    ``span_type`` is one of deepeval's ``agent`` / ``llm`` / ``retriever`` / ``tool``.
    ``root=True`` marks spans whose traces are printed and sent to listeners. The
    decision to trace is made per call, so decorating at import time is safe.
    """

    def decorate(func):
        span_name = name or func.__name__
        if root:
            _state.root_names.add(span_name)
        traced: list[Callable] = []

        def resolve() -> Callable:
            if not traced:
                traced.append(_state.deepeval.observe(type=span_type, name=span_name)(func))
            return traced[0]

        if inspect.isasyncgenfunction(func):

            @functools.wraps(func)
            def agen_wrapper(*args, **kwargs):
                if not _state.enabled:
                    return func(*args, **kwargs)
                return resolve()(*args, **kwargs)

            return agen_wrapper

        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                if not _state.enabled:
                    return await func(*args, **kwargs)
                return await resolve()(*args, **kwargs)

            return async_wrapper

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            if not _state.enabled:
                return func(*args, **kwargs)
            return resolve()(*args, **kwargs)

        return sync_wrapper

    return decorate


# ---------------------------------------------------------------------------
# Span / trace updates (all safe no-ops when tracing is off)
# ---------------------------------------------------------------------------


def _current_span():
    if not _state.enabled:
        return None
    return _state.deepeval.current_span_context.get()


def _current_trace():
    if not _state.enabled:
        return None
    return _state.deepeval.current_trace_context.get()


def update_span(
    *,
    input: Any = None,
    output: Any = None,
    retrieval_context: list[str] | None = None,
    **metadata: Any,
) -> None:
    """Set the current span's input/output and merge ``metadata`` into it."""
    span = _current_span()
    if span is None:
        return
    if input is not None:
        span.input = input
    if output is not None:
        span.output = output
    if retrieval_context is not None:
        span.retrieval_context = retrieval_context
    if metadata:
        span.metadata = {**(span.metadata or {}), **metadata}


def update_llm(
    *,
    model: str | None = None,
    usage: dict[str, Any] | None = None,
    input: Any = None,
    output: Any = None,
    **metadata: Any,
) -> None:
    """Record model and token usage (OpenAI-style ``usage`` dict) on an LLM span."""
    span = _current_span()
    if span is None:
        return
    if model and hasattr(span, "model"):
        span.model = model
    if usage and hasattr(span, "input_token_count"):
        span.input_token_count = usage.get("prompt_tokens")
        span.output_token_count = usage.get("completion_tokens")
        details = usage.get("completion_tokens_details") or {}
        if isinstance(details, dict) and details.get("reasoning_tokens"):
            metadata.setdefault("reasoning_tokens", details["reasoning_tokens"])
    update_span(input=input, output=output, **metadata)


def update_retriever(
    *, embedder: str | None = None, top_k: int | None = None, chunk_size: int | None = None
) -> None:
    span = _current_span()
    if span is None or not hasattr(span, "embedder"):
        return
    if embedder:
        span.embedder = embedder
    if top_k:
        span.top_k = top_k
    if chunk_size:
        span.chunk_size = chunk_size


def update_trace(
    *,
    name: str | None = None,
    thread_id: str | None = None,
    input: Any = None,
    output: Any = None,
    retrieval_context: list[str] | None = None,
    tags: list[str] | None = None,
    **metadata: Any,
) -> None:
    """Set trace-level fields and merge ``metadata`` into the trace."""
    trace = _current_trace()
    if trace is None:
        return
    if name:
        trace.name = name
    if thread_id:
        trace.thread_id = thread_id
    if input is not None:
        trace.input = input
    if output is not None:
        trace.output = output
    if retrieval_context is not None:
        trace.retrieval_context = retrieval_context
    if tags:
        trace.tags = sorted({*(trace.tags or []), *tags})
    if metadata:
        trace.metadata = {**(trace.metadata or {}), **metadata}


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------


def _install_exporter(trace_manager) -> None:
    if getattr(trace_manager.end_trace, "_onboardiq_exporter", False):
        return
    original = trace_manager.end_trace

    def end_trace(trace_uuid: str):
        trace = trace_manager.active_traces.get(trace_uuid)
        root = trace.root_spans[0] if trace is not None and trace.root_spans else None
        ours = root is not None and root.name in _state.root_names
        if trace is not None and not ours:
            trace.drop = True  # internal or ingestion traces: never uploaded or printed
        if ours:
            # Before the original: during deepeval evaluation it rewrites root_spans.
            _export(trace)
        return original(trace_uuid)

    end_trace._onboardiq_exporter = True  # type: ignore[attr-defined]
    trace_manager.end_trace = end_trace


def _export(trace) -> None:
    if _state.terminal:
        try:
            from src.observability.console import render_trace

            render_trace(trace, preview_chars=_state.preview_chars)
        except Exception:  # tracing must never break a chat turn
            logger.exception("Could not render trace")
    for listener in list(_state.listeners):
        try:
            listener(trace)
        except Exception:
            logger.exception("Trace listener failed")
