"""deepeval judge model backed by the Fireworks OpenAI-compatible API.

The judge reuses ``FIREWORKS_API_KEY`` / ``FIREWORKS_BASE_URL``; the model defaults to
``FIREWORKS_LLM_MODEL`` and can be changed with ``--judge-model``. Responses are
requested as JSON objects and validated against the metric's schema; one repair retry
is made when the JSON does not match.
"""

from __future__ import annotations

import json
import re
import threading
from typing import Any

from deepeval.models import DeepEvalBaseLLM
from openai import AsyncOpenAI, OpenAI
from pydantic import BaseModel, ValidationError

_FENCE = re.compile(r"^```(?:json)?\s*|\s*```$", re.MULTILINE)
_SYSTEM = (
    "You are a strict, impartial evaluator of an enterprise RAG assistant. "
    "Follow the instructions exactly and reply with a single valid JSON object only."
)


class FireworksJudge(DeepEvalBaseLLM):
    def __init__(
        self,
        *,
        api_key: str,
        base_url: str,
        model: str,
        reasoning_effort: str = "low",
        max_tokens: int = 16384,
        timeout: float = 120.0,
        max_retries: int = 6,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url
        self.model_id = model
        self.reasoning_effort = reasoning_effort
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.max_retries = max_retries
        self.calls = 0
        self.input_tokens = 0
        self.output_tokens = 0
        self.failures = 0
        self.truncated = 0
        self._lock = threading.Lock()
        super().__init__(model)

    # ------------------------------------------------------------------ deepeval API

    def load_model(self):
        kwargs = {
            "api_key": self.api_key,
            "base_url": self.base_url,
            "timeout": self.timeout,
            "max_retries": self.max_retries,
        }
        self._sync = OpenAI(**kwargs)
        self._async = AsyncOpenAI(**kwargs)
        return self._async

    def get_model_name(self) -> str:
        return f"fireworks:{self.model_id.rsplit('/', 1)[-1]}"

    def supports_json_mode(self) -> bool:
        return True

    def generate(self, prompt: str, schema: type[BaseModel] | None = None, **_: Any):
        content = self._record(self._sync.chat.completions.create(**self._payload(prompt)))
        parsed = _parse(content, schema)
        if schema is not None and parsed is None:
            retry = self._payload(_repair_prompt(prompt, content, schema))
            content = self._record(self._sync.chat.completions.create(**retry))
            parsed = _parse(content, schema)
        return self._result(parsed, content, schema)

    async def a_generate(self, prompt: str, schema: type[BaseModel] | None = None, **_: Any):
        response = await self._async.chat.completions.create(**self._payload(prompt))
        content = self._record(response)
        parsed = _parse(content, schema)
        if schema is not None and parsed is None:
            retry = self._payload(_repair_prompt(prompt, content, schema))
            content = self._record(await self._async.chat.completions.create(**retry))
            parsed = _parse(content, schema)
        return self._result(parsed, content, schema)

    # ------------------------------------------------------------------ helpers

    def _payload(self, prompt: str) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": self.model_id,
            "messages": [
                {"role": "system", "content": _SYSTEM},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.0,
            "max_tokens": self.max_tokens,
            "response_format": {"type": "json_object"},
        }
        if self.reasoning_effort:
            payload["extra_body"] = {"reasoning_effort": self.reasoning_effort}
        return payload

    def _record(self, response) -> str:
        usage = getattr(response, "usage", None)
        with self._lock:
            self.calls += 1
            if usage is not None:
                self.input_tokens += usage.prompt_tokens or 0
                self.output_tokens += usage.completion_tokens or 0
            if response.choices[0].finish_reason == "length":
                self.truncated += 1
        return (response.choices[0].message.content or "").strip()

    def _result(self, parsed, content: str, schema):
        if schema is None:
            return content
        if parsed is None:
            with self._lock:
                self.failures += 1
            return content  # deepeval falls back to lenient JSON extraction
        return parsed

    def usage(self) -> dict[str, int]:
        return {
            "calls": self.calls,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "schema_failures": self.failures,
            "truncated": self.truncated,
        }


def _parse(content: str, schema: type[BaseModel] | None):
    if schema is None:
        return None
    text = _FENCE.sub("", content).strip()
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end < start:
        return None
    try:
        return schema.model_validate(json.loads(text[start : end + 1]))
    except (json.JSONDecodeError, ValidationError):
        return None


def _repair_prompt(prompt: str, content: str, schema: type[BaseModel]) -> str:
    return (
        f"{prompt}\n\n---\nYour previous reply was not valid for the required JSON schema:\n"
        f"{content[:2000]}\n\nReply again with one JSON object that matches this JSON "
        f"schema exactly:\n{json.dumps(schema.model_json_schema())}"
    )
