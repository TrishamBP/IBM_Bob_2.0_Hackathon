"""Shared async HTTP client for the Fireworks AI inference API.

Handles authentication, timeouts and bounded retries with exponential backoff for
transient failures (429 rate limits, 5xx errors, timeouts and connection errors).
"""

from __future__ import annotations

import asyncio
import json
import logging
import random
from collections.abc import AsyncIterator
from typing import Any

import httpx

logger = logging.getLogger(__name__)

RETRYABLE_STATUS = frozenset({408, 409, 425, 429, 500, 502, 503, 504})


class FireworksError(RuntimeError):
    """Base error for Fireworks API failures."""


class FireworksAPIError(FireworksError):
    """The API returned a non-success HTTP status."""

    def __init__(self, status_code: int, message: str) -> None:
        super().__init__(f"Fireworks API error {status_code}: {message}")
        self.status_code = status_code


class FireworksResponseError(FireworksError):
    """The API returned a success status but the payload was malformed."""


class FireworksClient:
    """Thin async wrapper over ``httpx.AsyncClient`` with retry handling.

    Use as an async context manager or call :meth:`aclose` when done.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.fireworks.ai/inference/v1",
        *,
        timeout: float = 30.0,
        max_retries: int = 4,
        backoff_base: float = 0.5,
        backoff_max: float = 8.0,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        if not api_key:
            raise FireworksError("FIREWORKS_API_KEY is not configured")
        if max_retries < 0:
            raise ValueError("max_retries must be >= 0")
        self.base_url = base_url.rstrip("/")
        self.max_retries = max_retries
        self.backoff_base = backoff_base
        self.backoff_max = backoff_max
        self._http = httpx.AsyncClient(
            headers={"Authorization": f"Bearer {api_key}", "Accept": "application/json"},
            timeout=httpx.Timeout(timeout),
            transport=transport,
        )

    async def __aenter__(self) -> FireworksClient:
        return self

    async def __aexit__(self, *exc: object) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        await self._http.aclose()

    async def post_json(
        self, path_or_url: str, payload: dict[str, Any], *, timeout: float | None = None
    ) -> dict[str, Any]:
        """POST ``payload`` and return the decoded JSON object, retrying transient failures."""
        url = path_or_url if "://" in path_or_url else f"{self.base_url}/{path_or_url.lstrip('/')}"
        request_timeout = httpx.Timeout(timeout) if timeout is not None else None
        attempt = 0
        while True:
            try:
                kwargs: dict[str, Any] = {"json": payload}
                if request_timeout is not None:
                    kwargs["timeout"] = request_timeout
                response = await self._http.post(url, **kwargs)
            except (httpx.TimeoutException, httpx.TransportError) as exc:
                if attempt >= self.max_retries:
                    raise FireworksError(
                        f"Fireworks request to {url} failed after {attempt + 1} attempts: "
                        f"{type(exc).__name__}"
                    ) from exc
                await self._sleep_before_retry(attempt, None, type(exc).__name__)
                attempt += 1
                continue

            if response.status_code < 400:
                return self._decode(response)
            if response.status_code in RETRYABLE_STATUS and attempt < self.max_retries:
                await self._sleep_before_retry(attempt, response, str(response.status_code))
                attempt += 1
                continue
            raise FireworksAPIError(response.status_code, _error_message(response))

    async def stream_sse(
        self, path_or_url: str, payload: dict[str, Any], *, timeout: float | None = None
    ) -> AsyncIterator[dict[str, Any]]:
        """POST with ``stream: true`` and yield each decoded ``data:`` JSON event.

        Transient failures are retried only before the response stream starts; once
        events have been yielded a failure is raised, so no output is ever duplicated.
        ``timeout`` bounds each network read (and the connect), not the whole stream.
        """
        url = path_or_url if "://" in path_or_url else f"{self.base_url}/{path_or_url.lstrip('/')}"
        body = {**payload, "stream": True}
        headers = {"Accept": "text/event-stream"}
        request_timeout = httpx.Timeout(timeout) if timeout is not None else None
        attempt = 0
        while True:
            request = self._http.build_request(
                "POST",
                url,
                json=body,
                headers=headers,
                **({"timeout": request_timeout} if request_timeout is not None else {}),
            )
            try:
                response = await self._http.send(request, stream=True)
            except (httpx.TimeoutException, httpx.TransportError) as exc:
                if attempt >= self.max_retries:
                    raise FireworksError(
                        f"Fireworks stream to {url} failed after {attempt + 1} attempts: "
                        f"{type(exc).__name__}"
                    ) from exc
                await self._sleep_before_retry(attempt, None, type(exc).__name__)
                attempt += 1
                continue
            try:
                if response.status_code >= 400:
                    await response.aread()
                    if response.status_code in RETRYABLE_STATUS and attempt < self.max_retries:
                        await self._sleep_before_retry(attempt, response, str(response.status_code))
                        attempt += 1
                        continue
                    raise FireworksAPIError(response.status_code, _error_message(response))
                try:
                    async for line in response.aiter_lines():
                        if not line.startswith("data:"):
                            continue
                        data = line[5:].strip()
                        if data == "[DONE]":
                            return
                        try:
                            event = json.loads(data)
                        except ValueError as exc:
                            raise FireworksResponseError(
                                "Fireworks stream contained a non-JSON event"
                            ) from exc
                        if isinstance(event, dict):
                            if event.get("error"):
                                raise FireworksResponseError(
                                    f"Fireworks stream error: {str(event['error'])[:300]}"
                                )
                            yield event
                except (httpx.TimeoutException, httpx.TransportError) as exc:
                    raise FireworksError(
                        f"Fireworks stream interrupted: {type(exc).__name__}"
                    ) from exc
                return
            finally:
                await response.aclose()

    async def _sleep_before_retry(
        self, attempt: int, response: httpx.Response | None, reason: str
    ) -> None:
        delay = min(self.backoff_max, self.backoff_base * 2**attempt)
        retry_after = _retry_after_seconds(response)
        if retry_after is not None:
            delay = min(self.backoff_max, max(delay, retry_after))
        delay *= random.uniform(0.8, 1.2)  # jitter to avoid synchronized retries
        logger.warning(
            "Fireworks transient failure (%s); retry %d in %.2fs", reason, attempt + 1, delay
        )
        await asyncio.sleep(delay)

    @staticmethod
    def _decode(response: httpx.Response) -> dict[str, Any]:
        try:
            body = response.json()
        except ValueError as exc:
            raise FireworksResponseError("Fireworks returned a non-JSON response") from exc
        if not isinstance(body, dict):
            raise FireworksResponseError("Fireworks returned a non-object JSON response")
        return body


def _retry_after_seconds(response: httpx.Response | None) -> float | None:
    if response is None:
        return None
    value = response.headers.get("retry-after")
    try:
        return float(value) if value is not None else None
    except ValueError:
        return None


def _error_message(response: httpx.Response) -> str:
    try:
        body = response.json()
    except ValueError:
        return response.text[:300] or response.reason_phrase
    error = body.get("error") if isinstance(body, dict) else None
    if isinstance(error, dict):
        return str(error.get("message") or error)
    return str(error or body)[:300]
