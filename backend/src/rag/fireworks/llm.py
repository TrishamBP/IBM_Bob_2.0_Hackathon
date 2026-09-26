"""Async LLM client for DeepSeek V4.1 Flash via the Fireworks OpenAI-compatible API.

Uses the existing ``FireworksClient`` HTTP layer (retries, backoff, auth) and adds
structured JSON response parsing with Pydantic validation.

The client is stateless: every call to ``complete`` or ``complete_json`` is independent.
Instantiate once and reuse across requests (the underlying ``httpx.AsyncClient`` is
already thread-safe for concurrent async use).
"""

from __future__ import annotations

import json
import logging
from typing import Any

from pydantic import BaseModel, ValidationError

from src.observability import observe, update_llm
from src.rag.fireworks.client import FireworksClient, FireworksResponseError

logger = logging.getLogger(__name__)

# Sentinel: the model returned valid JSON but the schema validation failed.
_SCHEMA_MISMATCH = object()


class LLMError(RuntimeError):
    """Raised when the LLM returns an unusable response."""


class FireworksLLM:
    """Thin async wrapper around the Fireworks chat-completions endpoint.

    Parameters
    ----------
    client:
        Shared ``FireworksClient`` (handles auth + retries).
    model:
        Fireworks model identifier, e.g.
        ``"accounts/fireworks/models/deepseek-v4p1-flash"``.
    max_tokens:
        Upper bound on generated tokens.
    temperature:
        Sampling temperature (0 = deterministic, higher = more varied).
    timeout:
        Per-request timeout in seconds; overrides the client default when set.
    """

    def __init__(
        self,
        client: FireworksClient,
        model: str,
        *,
        max_tokens: int = 1024,
        temperature: float = 0.3,
        timeout: float | None = None,
    ) -> None:
        if not model:
            raise ValueError("LLM model identifier must not be empty")
        self.client = client
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.timeout = timeout

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def complete(
        self,
        system: str,
        user: str,
        *,
        extra: dict[str, Any] | None = None,
    ) -> str:
        """Send a two-turn prompt and return the raw text of the first choice.

        Parameters
        ----------
        system:
            System prompt.
        user:
            User message.
        extra:
            Any additional top-level fields to merge into the request payload
            (e.g. ``{"response_format": {"type": "json_object"}}``).
        """
        payload = self._build_payload(system, user, extra)
        return await self._chat(payload)

    async def complete_json(
        self,
        system: str,
        user: str,
        schema: type[BaseModel],
        *,
        extra: dict[str, Any] | None = None,
    ) -> BaseModel:
        """Like :meth:`complete` but parses the response as JSON and validates it.

        The model is requested to produce ``{"type": "json_object"}`` output.
        The returned text is parsed with ``json.loads`` and validated against
        ``schema``.  Raises :class:`LLMError` on parse or validation failure.
        """
        payload = self._build_payload(
            system,
            user,
            {**(extra or {}), "response_format": {"type": "json_object"}},
        )
        content = await self._chat(payload)
        return _parse_and_validate(content, schema)

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    @observe("llm", name="chat_completion")
    async def _chat(self, payload: dict[str, Any]) -> str:
        body = await self.client.post_json("chat/completions", payload, timeout=self.timeout)
        content = _extract_content(body)
        update_llm(
            model=self.model,
            usage=body.get("usage") if isinstance(body.get("usage"), dict) else None,
            input=payload["messages"][-1]["content"],
            output=content,
            json_mode="response_format" in payload,
            reasoning_effort=payload.get("reasoning_effort"),
            max_tokens=payload.get("max_tokens"),
            finish_reason=_finish_reason(body),
        )
        return content

    def _build_payload(
        self, system: str, user: str, extra: dict[str, Any] | None
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }
        if extra:
            payload.update(extra)
        return payload


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------


def _extract_content(body: dict[str, Any]) -> str:
    """Pull the assistant message text from a chat-completions response."""
    try:
        choices = body["choices"]
        content = choices[0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise FireworksResponseError(
            f"Unexpected chat-completions response structure: {exc}"
        ) from exc
    if not isinstance(content, str):
        raise FireworksResponseError(
            f"Expected string content in chat-completions response, got {type(content).__name__}"
        )
    return content.strip()


def _finish_reason(body: dict[str, Any]) -> str | None:
    try:
        return body["choices"][0].get("finish_reason")
    except (KeyError, IndexError, TypeError, AttributeError):
        return None


def _parse_and_validate(content: str, schema: type[BaseModel]) -> BaseModel:
    """Parse ``content`` as JSON and validate against ``schema``."""
    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise LLMError(
            f"LLM returned non-JSON content (first 200 chars): {content[:200]!r}"
        ) from exc
    try:
        return schema.model_validate(data)
    except ValidationError as exc:
        raise LLMError(f"LLM JSON response did not match expected schema: {exc}") from exc
