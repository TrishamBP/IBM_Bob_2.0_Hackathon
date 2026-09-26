"""Aggregate evaluation results into tables, print them and save JSON + Markdown."""

from __future__ import annotations

import json
import statistics
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.table import Table

_console = Console(stderr=True)
if not _console.is_terminal:  # piped/logged output: avoid an 80-column wrap
    _console.width = 160

# Deterministic pipeline metrics first, then LLM-judged metrics in this order.
_ORDER = [
    "Generation Health",
    "Latency",
    "Citation Integrity",
    "Secret Leakage (none)",
    "Routing Accuracy",
    "Department Coverage",
    "Retrieval MRR",
    "Answer Relevancy",
    "Faithfulness",
    "Contextual Relevancy",
    "Contextual Precision",
    "Contextual Recall",
    "Hallucination",
]


def _order(name: str) -> tuple[int, str]:
    base = name.split(" [")[0]
    return (_ORDER.index(base) if base in _ORDER else len(_ORDER), name)


def _pct(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    k = (len(ordered) - 1) * q
    lo, hi = int(k), min(int(k) + 1, len(ordered) - 1)
    return ordered[lo] + (ordered[hi] - ordered[lo]) * (k - lo)


def _f(value: Any, digits: int = 3) -> str:
    if value is None:
        return "-"
    if isinstance(value, float):
        return f"{value:.{digits}f}"
    return str(value)


def _rate(n: int, d: int) -> str:
    return f"{n / d:.0%} ({n}/{d})" if d else "-"


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------


def build_report(
    runs,
    rows: list[dict[str, Any]],
    *,
    judge_usage: dict[str, int] | None,
    judge_model: str | None,
    wall_s: dict[str, float],
    args: dict[str, str],
) -> dict[str, Any]:
    tables: list[dict[str, Any]] = []
    turns = [t for r in runs for t in r.turns]
    scored = [r for r in rows if r["score"] is not None and not r["error"]]

    # -- overview
    per_case: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        per_case[row["case_id"]].append(row)
    all_pass = sum(1 for items in per_case.values() if all(i["success"] for i in items))
    overview = [
        ["cases", str(len(runs))],
        ["chat turns", str(len(turns))],
        ["failed turns", str(sum(1 for t in turns if t.error))],
        ["metric evaluations", f"{len(rows)} ({len(rows) - len(scored)} errored/skipped)"],
        ["cases passing every metric", _rate(all_pass, len(per_case))],
        ["metric pass rate", _rate(sum(1 for r in rows if r["success"]), len(rows))],
        ["collection time", f"{wall_s.get('collect', 0):.1f} s"],
        ["total time", f"{wall_s.get('total', 0):.1f} s"],
        ["judge", judge_model or "none (deterministic metrics only)"],
    ]
    if judge_usage:
        overview.append(
            [
                "judge usage",
                f"{judge_usage['calls']} calls, {judge_usage['input_tokens']:,} in / "
                f"{judge_usage['output_tokens']:,} out tokens, "
                f"{judge_usage['schema_failures']} schema failures, "
                f"{judge_usage.get('truncated', 0)} truncated",
            ]
        )
    tables.append({"title": "Overview", "columns": ["", ""], "rows": overview})

    # -- per metric
    by_metric: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_metric[row["metric"]].append(row)
    metric_rows = []
    for name in sorted(by_metric, key=_order):
        items = by_metric[name]
        scores = [i["score"] for i in items if i["score"] is not None and not i["error"]]
        metric_rows.append(
            [
                name,
                str(len(items)),
                _f(statistics.fmean(scores)) if scores else "-",
                _f(statistics.median(scores)) if scores else "-",
                _f(min(scores)) if scores else "-",
                _f(max(scores)) if scores else "-",
                _f(statistics.pstdev(scores)) if len(scores) > 1 else "-",
                _rate(sum(1 for i in items if i["success"]), len(items)),
                _f(items[0]["threshold"], 2),
                str(sum(1 for i in items if i["error"])),
            ]
        )
    tables.append(
        {
            "title": "Metrics",
            "columns": [
                "metric",
                "n",
                "mean",
                "median",
                "min",
                "max",
                "stdev",
                "pass rate",
                "threshold",
                "errors",
            ],
            "rows": metric_rows,
        }
    )

    # -- suite x metric (mean score)
    suites = sorted({r["suite"] for r in rows})
    matrix = []
    for name in sorted(by_metric, key=_order):
        cells = []
        for suite in suites:
            vals = [
                i["score"]
                for i in by_metric[name]
                if i["suite"] == suite and i["score"] is not None and not i["error"]
            ]
            cells.append(f"{statistics.fmean(vals):.2f} (n={len(vals)})" if vals else "")
        matrix.append([name, *cells])
    tables.append({"title": "Mean score by suite", "columns": ["metric", *suites], "rows": matrix})

    # -- per department
    dept_metrics = [
        "Routing Accuracy",
        "Answer Relevancy",
        "Faithfulness",
        "Contextual Relevancy",
        "Citation Integrity",
        "Retrieval MRR",
        "Answer Correctness [GEval]",
    ]
    present = [m for m in dept_metrics if m in by_metric]
    by_dept: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if row["department"]:
            by_dept[row["department"]].append(row)
    dept_rows = []
    for dept in sorted(by_dept):
        items = by_dept[dept]
        cells = []
        for m in present:
            vals = [i["score"] for i in items if i["metric"] == m and i["score"] is not None]
            cells.append(_f(statistics.fmean(vals), 2) if vals else "")
        dept_cases = {i["case_id"] for i in items}
        passed = sum(1 for c in dept_cases if all(i["success"] for i in per_case[c]))
        dept_rows.append([dept, str(len(dept_cases)), *cells, _rate(passed, len(dept_cases))])
    if dept_rows:
        tables.append(
            {
                "title": "By department",
                "columns": ["department", "cases", *present, "all pass"],
                "rows": dept_rows,
            }
        )

    # -- pipeline
    tables.append({"title": "Pipeline", "columns": ["", ""], "rows": _pipeline(runs, turns, rows)})

    # -- per stage latency
    stage: dict[str, list[float]] = defaultdict(list)
    for t in turns:
        for name, ms in t.spans.items():
            stage[name].append(ms)
    stage_rows = [
        [
            name,
            str(len(v)),
            f"{statistics.fmean(v):.0f}",
            f"{_pct(v, 0.5):.0f}",
            f"{_pct(v, 0.95):.0f}",
            f"{max(v):.0f}",
        ]
        for name, v in sorted(stage.items(), key=lambda kv: -statistics.fmean(kv[1]))
    ]
    if stage_rows:
        tables.append(
            {
                "title": "Span latency (ms, from traces)",
                "columns": ["span", "n", "mean", "p50", "p95", "max"],
                "rows": stage_rows,
            }
        )

    # -- worst results
    failures = sorted(
        (r for r in rows if not r["success"]),
        key=lambda r: (r["score"] if r["score"] is not None else -1, r["metric"]),
    )
    worst = [
        [
            r["case_id"],
            r["metric"],
            _f(r["score"], 2),
            _short(r["question"], 70),
            _short(r["error"] or r["reason"] or "", 160),
        ]
        for r in failures[:25]
    ]
    if worst:
        tables.append(
            {
                "title": f"Lowest-scoring failures ({len(failures)} total, 25 shown)",
                "columns": ["case", "metric", "score", "question", "reason"],
                "rows": worst,
            }
        )

    return {
        "created": datetime.now().isoformat(timespec="seconds"),
        "args": args,
        "tables": tables,
        "results": rows,
    }


def _pipeline(runs, turns, rows) -> list[list[str]]:
    ok = [t for t in turns if not t.error]
    lat = [t.latency_ms for t in ok]
    ttft = []
    for t in ok:
        timings = t.metadata.get("timings") or {}
        if "first_token_ms" in timings and "generation_ms" in timings:
            ttft.append(timings["total_ms"] - timings["generation_ms"] + timings["first_token_ms"])
    p50, p95, worst = _pct(lat, 0.5) / 1000, _pct(lat, 0.95) / 1000, max(lat, default=0) / 1000
    mean_in = statistics.fmean([t.tokens_in for t in ok]) if ok else 0
    mean_out = statistics.fmean([t.tokens_out for t in ok]) if ok else 0
    out = [
        ["turn latency p50 / p95 / max", f"{p50:.1f} / {p95:.1f} / {worst:.1f} s"],
        [
            "time to first answer token p50 / p95",
            f"{_pct(ttft, 0.5) / 1000:.1f} / {_pct(ttft, 0.95) / 1000:.1f} s" if ttft else "-",
        ],
        [
            "LLM calls per turn (mean)",
            _f(statistics.fmean([t.llm_calls for t in ok]), 1) if ok else "-",
        ],
        [
            "tokens per turn in / out (mean)",
            f"{mean_in:,.0f} / {mean_out:,.0f}" if ok else "-",
        ],
        [
            "total tokens in / out",
            f"{sum(t.tokens_in for t in ok):,} / {sum(t.tokens_out for t in ok):,}",
        ],
    ]
    outcomes = Counter(t.metadata.get("outcome", "unknown") for t in turns)
    out.append(["outcomes", ", ".join(f"{k}={v}" for k, v in outcomes.most_common())])
    finish = Counter(str(t.metadata.get("finish_reason")) for t in ok)
    out.append(["finish reasons", ", ".join(f"{k}={v}" for k, v in finish.most_common())])
    if ok:
        out.append(
            [
                "retrieved chunks / context sources / cited (mean)",
                f"{statistics.fmean([t.metadata.get('retrieved_chunks') or 0 for t in ok]):.1f} / "
                f"{statistics.fmean([t.metadata.get('context_sources') or 0 for t in ok]):.1f} / "
                f"{statistics.fmean([len(t.metadata.get('cited_sources') or []) for t in ok]):.1f}",
            ]
        )
        out.append(
            [
                "evidence judged sufficient",
                _rate(sum(1 for t in ok if t.metadata.get("retrieval_sufficient")), len(ok)),
            ]
        )
        out.append(
            [
                "turns with invalid citations",
                _rate(sum(1 for t in ok if t.metadata.get("invalid_citations")), len(ok)),
            ]
        )
        out.append(
            [
                "follow-ups rewritten by resolver",
                _rate(sum(1 for t in ok if t.metadata.get("resolved_query")), len(ok)),
            ]
        )

    routed = [r for r in runs if r.case.expected_department and not r.failed]
    if routed:
        top1 = sum(
            1
            for r in routed
            if r.turns[0].metadata.get("primary_department") == r.case.expected_department
        )
        filt = sum(
            1
            for r in routed
            if r.case.expected_department
            in (
                r.turns[0].metadata.get("filter_departments")
                or [r.turns[0].metadata.get("primary_department")]
            )
        )
        out.append(["routing top-1 accuracy", _rate(top1, len(routed))])
        out.append(["expected department searched", _rate(filt, len(routed))])

    golden = [r for r in runs if r.case.source_chunk_id and not r.failed]
    if golden:
        ranks = []
        for r in golden:
            ids = r.turns[0].metadata.get("retrieved_chunk_ids") or []
            ranks.append(
                ids.index(r.case.source_chunk_id) + 1 if r.case.source_chunk_id in ids else None
            )
        k = max(
            (len(r.turns[0].metadata.get("retrieved_chunk_ids") or []) for r in golden), default=0
        )
        for at in (1, 3, 5, k):
            out.append(
                [
                    f"hit@{at} (golden chunk)",
                    _rate(sum(1 for x in ranks if x and x <= at), len(ranks)),
                ]
            )
        out.append(["MRR (golden chunk)", _f(statistics.fmean([1 / x if x else 0 for x in ranks]))])
        in_ctx = sum(
            1
            for r in golden
            if r.case.source_chunk_id in (r.turns[0].metadata.get("context_chunk_ids") or [])
        )
        out.append(["golden chunk in answer context", _rate(in_ctx, len(golden))])
        docs = sum(
            1
            for r in golden
            if r.case.source_document_id
            in (r.turns[0].metadata.get("retrieved_document_ids") or [])
        )
        out.append(["golden document retrieved", _rate(docs, len(golden))])

    abstain = [r for r in runs if r.case.expected_behavior != "answer" and not r.failed]
    if abstain:
        no_ev = sum(1 for r in abstain if r.turns[0].metadata.get("outcome") == "no_evidence")
        out.append(
            ["edge cases answered with 'not found' (no evidence)", _rate(no_ev, len(abstain))]
        )
    return out


def _short(text: str, limit: int) -> str:
    text = " ".join(str(text).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------


def print_report(report: dict[str, Any], console: Console | None = None) -> None:
    console = console or _console
    console.rule("[bold]OnboardIQ evaluation report")
    for spec in report["tables"]:
        grid = spec["columns"] == ["", ""]
        table = Table(
            title=f"[bold]{spec['title']}",
            show_header=not grid,
            header_style="bold",
            title_justify="left",
            expand=False,
        )
        for i, col in enumerate(spec["columns"]):
            table.add_column(
                col,
                overflow="fold",
                justify="right"
                if i and not grid and col not in ("question", "reason", "metric", "case")
                else "left",
            )
        for row in spec["rows"]:
            table.add_row(*[_style(c) for c in row])
        console.print(table)
        console.print()


def _style(cell: str) -> str:
    from rich.markup import escape

    cell = escape(cell)
    if cell.endswith(")") and "%" in cell:  # pass rates
        try:
            pct = int(cell.split("%")[0])
        except ValueError:
            return cell
        color = "green" if pct >= 80 else "yellow" if pct >= 50 else "red"
        return f"[{color}]{cell}[/]"
    return cell


def to_markdown(report: dict[str, Any]) -> str:
    lines = ["# OnboardIQ evaluation report", "", f"Created {report['created']}", ""]
    lines.append("Arguments: " + ", ".join(f"`{k}={v}`" for k, v in report["args"].items()))
    for spec in report["tables"]:
        lines += ["", f"## {spec['title']}", ""]
        cols = spec["columns"] if spec["columns"] != ["", ""] else ["item", "value"]
        lines.append("| " + " | ".join(cols) + " |")
        lines.append("|" + "---|" * len(cols))
        for row in spec["rows"]:
            lines.append("| " + " | ".join(str(c).replace("|", "\\|") for c in row) + " |")
    return "\n".join(lines) + "\n"


def save_report(report: dict[str, Any], output: Path, records: list[dict[str, Any]]) -> Path:
    print_report(report)
    folder = output / datetime.now().strftime("%Y%m%d-%H%M%S")
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "report.json").write_text(
        json.dumps({**report, "cases": records}, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8",
    )
    (folder / "report.md").write_text(to_markdown(report), encoding="utf-8")
    return folder
