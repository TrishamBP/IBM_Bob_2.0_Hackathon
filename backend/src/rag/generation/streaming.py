"""Server-Sent Events framing for the chat stream."""

from __future__ import annotations

import json
from typing import Any

SSE_HEADERS = {
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "X-Accel-Buffering": "no",  # disable proxy buffering so tokens arrive immediately
}


def sse_event(event: str, data: Any) -> str:
    """One SSE frame. JSON is single-line, so one ``data:`` line is always enough."""
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    return f"event: {event}\ndata: {payload}\n\n"
