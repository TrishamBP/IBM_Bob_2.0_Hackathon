"""Conversational context: history window and follow-up resolution.

A follow-up such as "What if it doesn't connect?" (after a VPN question) is rewritten
by DeepSeek into a standalone query ("What should I do if the VPN doesn't connect?")
that is used for routing and retrieval. The employee's original message is always what
is stored and shown; the resolved query is only a retrieval input.

Resolution modes: ``"auto"`` (only when the message looks context-dependent),
``"always"`` (whenever history exists) and ``"never"``.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass

from pydantic import BaseModel, Field

from src.rag.chat.prompts import RESOLVE_SYSTEM, RESOLVE_USER
from src.rag.chat.schemas import ChatMessage
from src.rag.fireworks import FireworksError, FireworksLLM, LLMError

logger = logging.getLogger(__name__)

_REFERENCE = re.compile(
    r"\b(it|its|it's|that|this|those|these|they|them|their|there|he|she|one|ones|"
    r"same|above|previous|earlier|former|latter|also|too|else|instead|another|more)\b",
    re.IGNORECASE,
)
_FOLLOW_UP_START = re.compile(
    r"^\s*(what if|what about|how about|and|but|also|then|so|why|ok|okay|and if|"
    r"what else|any other|which one|how long|where|when)\b",
    re.IGNORECASE,
)


def history_window(messages: list[ChatMessage], turns: int) -> list[ChatMessage]:
    """The last ``turns`` user/assistant exchanges; only completed, non-empty messages."""
    usable = [m for m in messages if m.status == "completed" and m.content.strip()]
    return usable[-2 * turns :] if turns > 0 else []


def format_history(messages: list[ChatMessage], max_chars: int = 600) -> str:
    lines = []
    for m in messages:
        text = " ".join(m.content.split())
        if len(text) > max_chars:
            text = text[:max_chars].rstrip() + " …"
        lines.append(f"{'Employee' if m.role == 'user' else 'Assistant'}: {text}")
    return "\n".join(lines)


def looks_context_dependent(message: str) -> bool:
    words = re.findall(r"\w+", message)
    return len(words) <= 6 or bool(_REFERENCE.search(message) or _FOLLOW_UP_START.match(message))


class _Resolved(BaseModel):
    query: str = Field(min_length=1, max_length=600)


@dataclass(frozen=True)
class ResolvedQuery:
    query: str
    method: str  # "original" | "llm" | "fallback"
    error: str | None = None


class FollowUpResolver:
    def __init__(
        self,
        llm: FireworksLLM | None,
        *,
        mode: str = "auto",
        llm_extra: dict | None = None,
    ) -> None:
        if mode not in ("auto", "always", "never"):
            raise ValueError(f"Unknown resolver mode {mode!r}")
        self.llm = llm
        self.mode = mode
        self.llm_extra = llm_extra

    async def resolve(self, message: str, history: list[ChatMessage]) -> ResolvedQuery:
        if (
            not history
            or self.llm is None
            or self.mode == "never"
            or (self.mode == "auto" and not looks_context_dependent(message))
        ):
            return ResolvedQuery(message, "original")
        user = RESOLVE_USER.format(history=format_history(history), message=message)
        try:
            parsed = await self.llm.complete_json(
                RESOLVE_SYSTEM, user, _Resolved, extra=self.llm_extra
            )
        except (LLMError, FireworksError) as exc:
            logger.warning("Follow-up resolution failed; using the original message: %s", exc)
            return ResolvedQuery(message, "fallback", str(exc)[:300])
        query = " ".join(parsed.query.split())
        return ResolvedQuery(query or message, "llm" if query != message else "original")


def make_title(message: str, max_chars: int = 60) -> str:
    """Conversation title from the first user message (deterministic, no LLM call)."""
    text = " ".join(message.split()).strip(" ?!.")
    if len(text) <= max_chars:
        return text or "New conversation"
    cut = text[:max_chars].rsplit(" ", 1)[0]
    return (cut or text[:max_chars]) + "…"
