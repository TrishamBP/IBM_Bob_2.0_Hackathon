"""Optional LLM tracing (deepeval). See :mod:`src.observability.tracing`."""

from src.observability.tracing import (
    add_trace_listener,
    configure_tracing,
    observe,
    remove_trace_listener,
    tracing_active,
    update_llm,
    update_retriever,
    update_span,
    update_trace,
)

__all__ = [
    "add_trace_listener",
    "configure_tracing",
    "observe",
    "remove_trace_listener",
    "tracing_active",
    "update_llm",
    "update_retriever",
    "update_span",
    "update_trace",
]
