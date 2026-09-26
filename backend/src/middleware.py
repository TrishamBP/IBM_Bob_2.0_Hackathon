"""ASGI middleware enforcing a maximum request body size on selected paths.

Requests with a ``Content-Length`` above the limit are rejected before any body is
read. Chunked or mislabelled bodies are counted while streaming; exceeding the limit
raises an ``HTTPException(413)`` from ``receive``, which FastAPI re-raises during form
parsing so the client gets a 413 with a string ``detail``.
"""

from __future__ import annotations

from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send


class BodySizeLimitMiddleware:
    def __init__(self, app: ASGIApp, *, max_bytes: int, path_prefixes: tuple[str, ...]) -> None:
        self.app = app
        self.max_bytes = max_bytes
        self.path_prefixes = path_prefixes

    def _detail(self) -> str:
        return f"Request body exceeds the {self.max_bytes // (1024 * 1024)} MB limit"

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http" or not scope["path"].startswith(self.path_prefixes):
            await self.app(scope, receive, send)
            return

        headers = dict(scope.get("headers") or [])
        content_length = headers.get(b"content-length")
        if content_length is not None:
            try:
                too_large = int(content_length) > self.max_bytes
            except ValueError:
                too_large = False
            if too_large:
                response = JSONResponse({"detail": self._detail()}, status_code=413)
                await response(scope, receive, send)
                return

        received = 0

        async def limited_receive() -> Message:
            nonlocal received
            message = await receive()
            if message["type"] == "http.request":
                received += len(message.get("body", b""))
                if received > self.max_bytes:
                    raise HTTPException(status_code=413, detail=self._detail())
            return message

        await self.app(scope, limited_receive, send)
