"""Structured DeepSeek calls with validation feedback and bounded retries."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from pydantic import BaseModel

from src.rag.fireworks import FireworksLLM, FireworksResponseError, LLMError


class StructuredOutputError(RuntimeError):
    """The model did not produce valid structured output within the attempt limit."""

    def __init__(self, problems: list[str], attempts: int) -> None:
        super().__init__(f"Invalid structured output after {attempts} attempt(s): {problems}")
        self.problems = problems
        self.attempts = attempts


async def call_structured[M: BaseModel](
    llm: FireworksLLM,
    system: str,
    user: str,
    schema: type[M],
    *,
    max_attempts: int,
    validate: Callable[[M], list[str]] | None = None,
    extra: dict[str, Any] | None = None,
) -> tuple[M, int]:
    """Return ``(result, attempts)``.

    Invalid JSON, schema violations and failed semantic checks (``validate`` returns a
    list of problems) are retried with the problems appended to the prompt. Transport
    and API errors (``FireworksAPIError`` etc.) are not retried here; the HTTP client
    already retries transient failures, so they propagate to the caller.
    """
    problems: list[str] = []
    for attempt in range(1, max_attempts + 1):
        prompt = user
        if problems:
            listed = "\n".join(f"- {p}" for p in problems[:20])
            prompt = (
                f"{user}\n\nYour previous response was rejected for these reasons:\n{listed}\n"
                "Return a corrected JSON object that follows all rules."
            )
        try:
            result = await llm.complete_json(system, prompt, schema, extra=extra)
        except (LLMError, FireworksResponseError) as exc:
            problems = [str(exc)[:600]]
            continue
        problems = validate(result) if validate else []  # type: ignore[arg-type]
        if not problems:
            return result, attempt  # type: ignore[return-value]
    raise StructuredOutputError(problems, max_attempts)
