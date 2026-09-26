"""Run the OnboardIQ evaluation.

    uv sync --group eval
    uv run --group eval python -m evals.run --limit 5            # quick smoke run
    uv run --group eval python -m evals.run --suite all --synthetic 30

Every question is sent through the real chat pipeline (``ChatService.stream``) against
the local Chroma index, with LLM tracing printed to the terminal. The answers, the
retrieved context and the trace diagnostics become deepeval test cases, which are
scored by deterministic pipeline metrics and LLM-judged deepeval metrics. A summary
report is printed and saved (JSON + Markdown) under ``evals/results/<timestamp>/``.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import tempfile
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from evals.dataset import DEFAULT_EXAMPLES, EvalCase, load_curated, load_synthetic

ROOT = Path(__file__).resolve().parent
EVAL_EMAIL = "eval.runner@acme.example"
CHATBOT_ROLE = (
    "ACME Corp's employee onboarding assistant. It answers only from internal ACME "
    "documents, cites them with markers like [S1], and says so when the documents do not "
    "cover a question."
)
SUITES = {
    "curated": {"department", "quick_start", "cross_department", "edge_case", "conversation"},
    "department": {"department"},
    "quick": {"quick_start"},
    "cross": {"cross_department"},
    "edge": {"edge_case"},
    "conversation": {"conversation"},
    "synthetic": {"synthetic"},
}


@dataclass
class TurnRun:
    question: str
    answer: str = ""
    error: str | None = None
    latency_ms: float = 0.0
    retrieval_context: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    spans: dict[str, float] = field(default_factory=dict)  # span name -> duration ms
    llm_calls: int = 0
    tokens_in: int = 0
    tokens_out: int = 0


@dataclass
class CaseRun:
    case: EvalCase
    turns: list[TurnRun] = field(default_factory=list)

    @property
    def failed(self) -> bool:
        return any(t.error for t in self.turns)


# ---------------------------------------------------------------------------
# Collect: run questions through the chat pipeline
# ---------------------------------------------------------------------------


class TraceCapture:
    """Trace listener keeping each chat turn's trace, keyed by assistant message id."""

    def __init__(self) -> None:
        self.traces: dict[str, dict[str, Any]] = {}

    def __call__(self, trace) -> None:
        meta = dict(trace.metadata or {})
        message_id = meta.get("assistant_message_id")
        if not message_id:
            return
        spans: dict[str, float] = {}
        calls = tin = tout = 0
        stack = list(trace.root_spans or [])
        while stack:
            span = stack.pop()
            if span.end_time and span.start_time:
                duration = (span.end_time - span.start_time) * 1000
                spans[span.name] = spans.get(span.name, 0.0) + duration
            if type(span).__name__ == "LlmSpan":
                calls += 1
                tin += int(span.input_token_count or 0)
                tout += int(span.output_token_count or 0)
            stack.extend(span.children or [])
        self.traces[message_id] = {
            "metadata": meta,
            "retrieval_context": list(trace.retrieval_context or []),
            "spans": spans,
            "llm_calls": calls,
            "tokens_in": tin,
            "tokens_out": tout,
        }


def _frames(chunk: str):
    for frame in chunk.split("\n\n"):
        event, data = None, None
        for line in frame.splitlines():
            if line.startswith("event: "):
                event = line[7:].strip()
            elif line.startswith("data: "):
                data = json.loads(line[6:])
        if event:
            yield event, data or {}


async def _run_turn(chat, question: str, conversation_id: str | None, capture: TraceCapture):
    from src.rag.chat.schemas import ChatStreamRequest

    turn = TurnRun(question=question)
    message_id = None
    started = time.perf_counter()
    request = ChatStreamRequest(
        conversation_id=conversation_id, employee_email=EVAL_EMAIL, message=question
    )
    try:
        async for chunk in chat.stream(request):
            for event, data in _frames(chunk):
                if event == "session":
                    conversation_id = data["conversation_id"]
                    message_id = data["assistant_message_id"]
                elif event == "completed":
                    turn.answer = data.get("content") or ""
                    turn.metadata["diagnostics"] = data.get("diagnostics") or {}
                elif event == "error":
                    turn.error = f"{data.get('code')}: {data.get('message')}"
    except Exception as exc:  # recorded, the run continues
        turn.error = f"{type(exc).__name__}: {exc}"
    turn.latency_ms = round((time.perf_counter() - started) * 1000, 1)
    trace = capture.traces.pop(message_id, None) if message_id else None
    if trace:
        turn.metadata = {**trace["metadata"], **turn.metadata}
        turn.retrieval_context = trace["retrieval_context"]
        turn.spans = trace["spans"]
        turn.llm_calls, turn.tokens_in, turn.tokens_out = (
            trace["llm_calls"],
            trace["tokens_in"],
            trace["tokens_out"],
        )
    return turn, conversation_id


async def collect(chat, cases: list[EvalCase], concurrency: int) -> list[CaseRun]:
    from src.observability import add_trace_listener, remove_trace_listener

    capture = TraceCapture()
    add_trace_listener(capture)
    semaphore = asyncio.Semaphore(concurrency)
    done = 0

    async def one(case: EvalCase) -> CaseRun:
        nonlocal done
        async with semaphore:
            run = CaseRun(case)
            conversation_id = None
            for question in case.turns:
                turn, conversation_id = await _run_turn(chat, question, conversation_id, capture)
                run.turns.append(turn)
                if turn.error:
                    break
            done += 1
            status = "FAILED " + (run.turns[-1].error or "") if run.failed else "ok"
            print(f"[{done}/{len(cases)}] {case.id}: {status}", file=sys.stderr, flush=True)
            return run

    try:
        return list(await asyncio.gather(*(one(c) for c in cases)))
    finally:
        remove_trace_listener(capture)


# ---------------------------------------------------------------------------
# Score: build deepeval test cases and evaluate them
# ---------------------------------------------------------------------------


def _metadata(run: CaseRun, turn: TurnRun) -> dict[str, Any]:
    case = run.case
    routing = (turn.metadata.get("diagnostics") or {}).get("routing") or {}
    meta = {k: v for k, v in turn.metadata.items() if k != "diagnostics"}
    meta.update(
        suite=case.suite,
        section=case.section,
        expected_department=case.expected_department,
        expected_departments=case.expected_departments,
        expected_behavior=case.expected_behavior,
        source_chunk_id=case.source_chunk_id,
        source_document_id=case.source_document_id,
        routing_top=routing.get("top") or [],
        error=turn.error,
        latency_ms=turn.latency_ms,
    )
    return meta


def _metric_sets(run: CaseRun, args, judge) -> list[str]:
    case = run.case
    names = ["health"]
    if run.failed:
        return names
    if case.multi_turn:
        return ["conversation"] if judge else []
    if case.expected_department:
        names.append("routing")
    if len(case.expected_departments) > 1:
        names.append("coverage")
    if case.source_chunk_id:
        names.append("retrieval_rank")
    if judge:
        names.append("rag" if case.expected_behavior == "answer" else "behavior")
        if case.expected_output and case.expected_behavior == "answer":
            names.append("reference")
        if case.suite == "edge_case" or args.safety:
            names.append("safety")
    return names


def _build_metrics(name: str, judge, secret: str) -> list:
    from evals import metrics as m

    if name == "health":
        return [
            m.GenerationHealthMetric(),
            m.LatencyMetric(),
            m.CitationIntegrityMetric(),
            m.SecretLeakMetric(secret=secret),
        ]
    return {
        "routing": lambda: [m.RoutingAccuracyMetric()],
        "coverage": lambda: [m.DepartmentCoverageMetric()],
        "retrieval_rank": lambda: [m.RetrievalRankMetric(threshold=0.2)],
        "rag": lambda: m.rag_metrics(judge),
        "reference": lambda: m.reference_metrics(judge),
        "behavior": lambda: m.behavior_metrics(judge),
        "safety": lambda: m.safety_metrics(judge),
        "conversation": lambda: m.conversation_metrics(judge),
    }[name]()


def _single_turn_case(run: CaseRun):
    from deepeval.test_case import LLMTestCase

    turn = run.turns[0]
    return LLMTestCase(
        name=run.case.id,
        input=turn.question,
        actual_output=turn.answer or "",
        expected_output=run.case.expected_output,
        context=run.case.context,
        retrieval_context=turn.retrieval_context or None,
        completion_time=turn.latency_ms / 1000,
        input_token_count=turn.tokens_in or None,
        output_token_count=turn.tokens_out or None,
        metadata=_metadata(run, turn),
        tags=[run.case.suite],
    )


def _conversation_case(run: CaseRun):
    from deepeval.test_case import ConversationalTestCase, Turn

    turns = []
    for t in run.turns:
        turns.append(Turn(role="user", content=t.question))
        turns.append(
            Turn(
                role="assistant",
                content=t.answer or "(no answer)",
                retrieval_context=t.retrieval_context or None,
                latency_ms=t.latency_ms,
            )
        )
    return ConversationalTestCase(
        name=run.case.id,
        turns=turns,
        scenario=f"A new ACME employee asks follow-up questions: {run.case.section}",
        expected_outcome="Each follow-up is resolved against earlier turns and answered from "
        "the ACME documents with citations.",
        chatbot_role=CHATBOT_ROLE,
        metadata={"suite": run.case.suite, "section": run.case.section},
        tags=[run.case.suite],
    )


def score(runs: list[CaseRun], args, judge, secret: str) -> list[dict[str, Any]]:
    from deepeval import evaluate
    from deepeval.evaluate.configs import AsyncConfig, CacheConfig, DisplayConfig, ErrorConfig

    groups: dict[tuple[str, ...], list[CaseRun]] = {}
    for run in runs:
        key = tuple(_metric_sets(run, args, judge))
        if key:
            groups.setdefault(key, []).append(run)

    by_id = {r.case.id: r for r in runs}
    rows: list[dict[str, Any]] = []
    for key, members in groups.items():
        conversational = key == ("conversation",)
        metrics = [metric for name in key for metric in _build_metrics(name, judge, secret)]
        test_cases = [
            _conversation_case(r) if conversational else _single_turn_case(r) for r in members
        ]
        print(
            f"\n== Scoring {len(test_cases)} case(s) with {len(metrics)} metrics "
            f"[{', '.join(key)}]",
            file=sys.stderr,
            flush=True,
        )
        result = evaluate(
            test_cases=test_cases,
            metrics=metrics,
            async_config=AsyncConfig(max_concurrent=args.judge_concurrency),
            display_config=DisplayConfig(
                show_indicator=not args.no_print_results,
                print_results=not args.no_print_results,
                truncate_passing_cases=False,
                inspect_after_run=False,
            ),
            cache_config=CacheConfig(write_cache=False, use_cache=False),
            error_config=ErrorConfig(ignore_errors=True, skip_on_missing_params=True),
        )
        for test in result.test_results:
            run = by_id.get(test.name)
            if run is None:
                continue
            for data in test.metrics_data or []:
                rows.append(
                    {
                        "case_id": run.case.id,
                        "suite": run.case.suite,
                        "section": run.case.section,
                        "department": run.case.expected_department,
                        "question": run.case.turns[0],
                        "metric": data.name,
                        "score": data.score,
                        "threshold": data.threshold,
                        "success": bool(data.success),
                        "reason": data.reason,
                        "error": data.error,
                        "evaluation_model": data.evaluation_model,
                    }
                )
    return rows


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="python -m evals.run", description=__doc__.split("\n")[0])
    p.add_argument("--suite", default="curated", choices=[*SUITES, "all"])
    p.add_argument("--limit", type=int, default=0, help="max cases per suite (0 = all)")
    p.add_argument("--synthetic", type=int, default=0, help="number of synthetic goldens")
    p.add_argument("--regenerate", action="store_true", help="regenerate synthetic goldens")
    p.add_argument("--concurrency", type=int, default=2, help="chat turns in parallel")
    p.add_argument("--judge-model", default=None, help="Fireworks model id for the judge")
    p.add_argument("--judge-concurrency", type=int, default=4)
    p.add_argument("--no-llm-metrics", action="store_true", help="deterministic metrics only")
    p.add_argument("--safety", action="store_true", help="bias/toxicity/PII on every case")
    p.add_argument("--quiet-traces", action="store_true", help="do not print trace trees")
    p.add_argument("--no-print-results", action="store_true", help="hide deepeval's per-case log")
    p.add_argument("--examples", type=Path, default=DEFAULT_EXAMPLES)
    p.add_argument("--output", type=Path, default=ROOT / "results")
    args = p.parse_args(argv)
    if args.suite == "synthetic" and not args.synthetic:
        args.synthetic = 20
    return args


def _select(cases: list[EvalCase], args) -> list[EvalCase]:
    wanted = set().union(*SUITES.values()) if args.suite == "all" else SUITES[args.suite]
    selected: list[EvalCase] = []
    counts: dict[str, int] = {}
    for case in cases:
        if case.suite not in wanted:
            continue
        counts[case.suite] = counts.get(case.suite, 0) + 1
        if args.limit and counts[case.suite] > args.limit:
            continue
        selected.append(case)
    return selected


async def _prepare(args, settings, chat_dir: str):
    from evals.judge import FireworksJudge
    from src.observability import configure_tracing
    from src.rag.service import create_services

    configure_tracing(
        enabled=True, terminal=not args.quiet_traces, preview_chars=settings.tracing_preview_chars
    )
    services = await create_services(settings.model_copy(update={"chat_dir": chat_dir}))
    if services is None or services.chat is None:
        raise SystemExit("FIREWORKS_API_KEY is not configured; see backend/.env.example")
    judge = None
    if not args.no_llm_metrics or args.synthetic:
        judge = FireworksJudge(
            api_key=settings.fireworks_api_key.get_secret_value(),
            base_url=settings.fireworks_base_url,
            model=args.judge_model or settings.fireworks_llm_model,
        )
    cases = load_curated(args.examples) if args.suite != "synthetic" else []
    if args.suite in ("synthetic", "all") and args.synthetic:
        cases += await load_synthetic(
            services.store, judge, args.synthetic, regenerate=args.regenerate
        )
    return services, judge, _select(cases, args)


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):  # deepeval prints emoji; Windows consoles are cp1252
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    os.environ.setdefault("DEEPEVAL_TELEMETRY_OPT_OUT", "YES")
    os.environ.setdefault("ERROR_REPORTING", "NO")
    # Conversational metrics make many sequential judge calls per test case.
    os.environ.setdefault("DEEPEVAL_PER_TASK_TIMEOUT_SECONDS_OVERRIDE", "900")
    args = _parse_args(argv)
    sys.path.insert(0, str(ROOT.parent))

    from evals.report import build_report, save_report
    from src.config import get_settings

    settings = get_settings()
    # One event loop for the whole run: deepeval's evaluate() reuses the current loop,
    # so the judge's async HTTP client stays valid across collection and scoring.
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    with tempfile.TemporaryDirectory(prefix="onboardiq-eval-") as chat_dir:
        services, judge, cases = loop.run_until_complete(_prepare(args, settings, chat_dir))
        if not cases:
            print("No cases selected.", file=sys.stderr)
            return 1
        print(f"Running {len(cases)} case(s)...", file=sys.stderr, flush=True)
        started = time.perf_counter()
        try:
            runs = loop.run_until_complete(collect(services.chat, cases, args.concurrency))
            collect_s = time.perf_counter() - started
            secret = settings.fireworks_api_key.get_secret_value()
            rows = score(runs, args, None if args.no_llm_metrics else judge, secret)
        finally:
            loop.run_until_complete(services.aclose())
    report = build_report(
        runs,
        rows,
        judge_usage=judge.usage() if judge else None,
        judge_model=judge.get_model_name() if judge else None,
        wall_s={"collect": collect_s, "total": time.perf_counter() - started},
        args={k: str(v) for k, v in vars(args).items()},
    )
    out = save_report(report, args.output, [_run_record(r) for r in runs])
    print(f"\nReport saved to {out}", file=sys.stderr)
    return 0


def _run_record(run: CaseRun) -> dict[str, Any]:
    """Saved per-case record. Retrieved chunk text is not written to disk (count only)."""
    turns = []
    for t in run.turns:
        record = asdict(t)
        record["retrieval_context"] = len(t.retrieval_context)
        record["metadata"] = {k: v for k, v in t.metadata.items() if k != "diagnostics"}
        turns.append(record)
    case = asdict(run.case)
    case.pop("context", None)
    return {**case, "runs": turns}


if __name__ == "__main__":
    raise SystemExit(main())
