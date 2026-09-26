"""Terminal rendering of a finished trace as a span tree (rich, stderr).

Shows timing, status, models, token counts, span metadata and short previews of span
inputs/outputs. Retrieved document text is never printed: retrieval spans show only
chunk counts and source references.
"""

from __future__ import annotations

import json
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

_console = Console(stderr=True, soft_wrap=False)

_TYPE_STYLE = {
    "AgentSpan": ("agent", "magenta"),
    "LlmSpan": ("llm", "cyan"),
    "RetrieverSpan": ("retriever", "green"),
    "ToolSpan": ("tool", "yellow"),
}


def render_trace(trace, *, preview_chars: int = 160, console: Console | None = None) -> None:
    console = console or _console
    roots = list(trace.root_spans or [])
    if not roots:
        return
    root = roots[0]
    stats = _collect(roots)
    meta = trace.metadata or {}
    duration = _duration_ms(root)
    status = _status(trace)

    title = Text.assemble(
        (f"{trace.name or root.name}", "bold"),
        "  ",
        status,
        f"  {_fmt_ms(duration)}",
    )
    tree = Tree(title, guide_style="grey42")
    for span in roots:
        _add_span(tree, span, preview_chars)

    console.print(
        Panel(
            _body(tree, trace, meta, stats, preview_chars),
            title="[bold]LLM trace[/]",
            subtitle=_subtitle(trace),
            border_style="red" if status.plain == "FAILED" else "blue",
            expand=True,
        )
    )


# ---------------------------------------------------------------------------


def _body(tree: Tree, trace, meta: dict[str, Any], stats: dict[str, Any], preview_chars: int):
    table = Table.grid(padding=(0, 2))
    table.add_column(style="grey62", no_wrap=True)
    table.add_column()

    if trace.input:
        table.add_row("question", Text(_preview(trace.input, preview_chars * 2)))
    for key, label in (
        ("resolved_query", "resolved"),
        ("primary_department", "department"),
        ("selected_departments", "routed to"),
        ("filter_departments", "filter"),
        ("retrieval_sufficient", "evidence ok"),
        ("retrieval_reason", "evidence"),
        ("retrieved_chunks", "chunks"),
        ("context_sources", "sources"),
        ("cited_sources", "cited"),
        ("invalid_citations", "invalid cites"),
        ("finish_reason", "finish"),
        ("outcome", "outcome"),
    ):
        if key in meta and meta[key] not in (None, "", []):
            table.add_row(label, Text(_preview(meta[key], preview_chars * 2)))
    table.add_row(
        "llm calls",
        f"{stats['llm_calls']}  |  tokens in {stats['tokens_in']:,}  out {stats['tokens_out']:,}"
        + (f"  (reasoning {stats['reasoning']:,})" if stats["reasoning"] else ""),
    )
    table.add_row("spans", f"{stats['spans']}  |  errors {stats['errors']}")
    timings = meta.get("timings")
    if isinstance(timings, dict) and timings:
        table.add_row(
            "timings", "  ".join(f"{k.removesuffix('_ms')}={v:.0f}ms" for k, v in timings.items())
        )
    if trace.output:
        table.add_row("answer", Text(_preview(trace.output, preview_chars * 2)))

    grid = Table.grid()
    grid.add_row(tree)
    grid.add_row(Text(""))
    grid.add_row(table)
    return grid


def _subtitle(trace) -> str:
    parts = []
    if trace.thread_id:
        parts.append(f"conversation {str(trace.thread_id)[:8]}")
    parts.append(f"trace {trace.uuid[:8]}")
    return "[grey50]" + " | ".join(parts) + "[/]"


def _add_span(parent: Tree, span, preview_chars: int) -> None:
    kind, color = _TYPE_STYLE.get(type(span).__name__, ("span", "white"))
    label = Text.assemble(
        (span.name or "?", f"bold {color}"),
        (f" [{kind}]", "grey50"),
        "  ",
        (_fmt_ms(_duration_ms(span)), _duration_style(_duration_ms(span))),
    )
    model = getattr(span, "model", None)
    if model:
        label.append(f"  {model.rsplit('/', 1)[-1]}", style="grey70")
    tin, tout = getattr(span, "input_token_count", None), getattr(span, "output_token_count", None)
    if tin is not None or tout is not None:
        label.append(f"  tok {int(tin or 0):,}->{int(tout or 0):,}", style="grey70")
    if getattr(span, "top_k", None):
        label.append(f"  top_k={span.top_k}", style="grey70")
    status = getattr(span.status, "value", str(span.status))
    if span.error or status == "ERRORED":
        label.append(f"  ERROR {span.error or 'error'}"[:200], style="bold red")

    node = parent.add(label)
    if span.metadata:
        node.add(Text(_kv(span.metadata, preview_chars), style="grey62"))
    if preview_chars:
        if _is_text(span.input):
            node.add(Text("in  " + _preview(span.input, preview_chars), style="grey50"))
        if _is_text(span.output):
            node.add(Text("out " + _preview(span.output, preview_chars), style="grey50"))
    for child in sorted(span.children or [], key=lambda s: s.start_time):
        _add_span(node, child, preview_chars)


def _collect(spans) -> dict[str, Any]:
    stats = {"llm_calls": 0, "tokens_in": 0, "tokens_out": 0, "reasoning": 0, "spans": 0}
    stats["errors"] = 0
    stack = list(spans)
    while stack:
        span = stack.pop()
        stats["spans"] += 1
        if span.error:
            stats["errors"] += 1
        if type(span).__name__ == "LlmSpan":
            stats["llm_calls"] += 1
            stats["tokens_in"] += int(span.input_token_count or 0)
            stats["tokens_out"] += int(span.output_token_count or 0)
            stats["reasoning"] += int((span.metadata or {}).get("reasoning_tokens") or 0)
        stack.extend(span.children or [])
    return stats


def _status(trace) -> Text:
    status = getattr(trace.status, "value", str(trace.status))
    outcome = (trace.metadata or {}).get("outcome")
    if status == "ERRORED" or outcome in ("failed", "error"):
        return Text("FAILED", style="bold red")
    if outcome == "cancelled":
        return Text("CANCELLED", style="bold yellow")
    return Text("OK", style="bold green")


def _duration_ms(span) -> float:
    if span.end_time is None or span.start_time is None:
        return 0.0
    return (span.end_time - span.start_time) * 1000


def _fmt_ms(ms: float) -> str:
    return f"{ms / 1000:.2f} s" if ms >= 1000 else f"{ms:.0f} ms"


def _duration_style(ms: float) -> str:
    if ms >= 10_000:
        return "bold red"
    if ms >= 3_000:
        return "yellow"
    return "green"


def _is_text(value: Any) -> bool:
    if isinstance(value, list):
        return bool(value) and all(isinstance(v, str) for v in value)
    return isinstance(value, str) and bool(value.strip())


def _preview(value: Any, limit: int) -> str:
    if isinstance(value, list) and all(isinstance(v, str) for v in value):
        value = "; ".join(value)
    elif not isinstance(value, str):
        try:
            value = json.dumps(value, ensure_ascii=False, default=str)
        except (TypeError, ValueError):
            value = str(value)
    value = " ".join(value.split())
    if limit and len(value) > limit:
        value = value[: limit - 3] + "..."
    return value


def _kv(metadata: dict[str, Any], limit: int) -> str:
    parts = []
    for key, value in metadata.items():
        if value is None or value == "" or value == []:
            continue
        if isinstance(value, float):
            value = f"{value:.3f}"
        parts.append(f"{key}={_preview(value, max(limit, 60))}")
    return "  ".join(parts)
