"""Streaming answer generation with GLM 5.3 Flash (Fireworks chat completions).

Only ``delta.content`` is yielded. ``delta.reasoning_content`` (the model's internal
reasoning) is discarded and never stored or sent to the client. Usage and the finish
reason are captured from the final chunk.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from typing import Any

from src.rag.fireworks.client import FireworksClient


@dataclass
class GenerationStats:
    finish_reason: str | None = None
    usage: dict[str, Any] = field(default_factory=dict)
    model: str | None = None


class AnswerLLM:
    def __init__(
        self,
        client: FireworksClient,
        model: str,
        *,
        max_tokens: int = 2048,
        temperature: float = 0.2,
        timeout: float | None = 60.0,
        reasoning_effort: str = "",
    ) -> None:
        if not model:
            raise ValueError("Answer model identifier must not be empty")
        self.client = client
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.timeout = timeout
        self.reasoning_effort = reasoning_effort

    async def stream(
        self, messages: list[dict[str, str]], stats: GenerationStats | None = None
    ) -> AsyncIterator[str]:
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }
        if self.reasoning_effort:
            payload["reasoning_effort"] = self.reasoning_effort
        async for event in self.client.stream_sse(
            "chat/completions", payload, timeout=self.timeout
        ):
            if stats is not None:
                stats.model = event.get("model") or stats.model
                if isinstance(event.get("usage"), dict):
                    stats.usage = event["usage"]
            for choice in event.get("choices") or []:
                delta = choice.get("delta") or {}
                content = delta.get("content")
                if isinstance(content, str) and content:
                    yield content
                if choice.get("finish_reason") and stats is not None:
                    stats.finish_reason = choice["finish_reason"]
