"""Chat conversation schemas (the JSON file format and the HTTP contract).

``employee_email`` is a demo-only identifier supplied by the client; it is not verified
identity and must not be treated as authentication.
"""

from __future__ import annotations

import re
from datetime import UTC, datetime
from typing import Annotated, Literal
from uuid import uuid4

from pydantic import AfterValidator, BaseModel, Field, field_validator

MessageRole = Literal["user", "assistant"]
MessageStatus = Literal["streaming", "completed", "failed", "cancelled"]

_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def new_id() -> str:
    return str(uuid4())


def normalize_email(value: str) -> str:
    value = value.strip().lower()
    if len(value) > 254 or not _EMAIL.match(value):
        raise ValueError("employee_email must be a valid email address")
    return value


Email = Annotated[str, Field(min_length=3, max_length=254), AfterValidator(normalize_email)]


class SourceRef(BaseModel):
    id: str  # citation marker, e.g. "S1"
    chunk_id: str
    document_id: str
    title: str
    department: str
    section: str | None = None
    reference: str
    version: str | None = None
    source_filename: str | None = None
    page_start: int | None = None
    page_end: int | None = None
    url: str | None = None  # only when the document has a real link


class ChatMessage(BaseModel):
    id: str = Field(default_factory=new_id)
    role: MessageRole
    content: str = ""
    timestamp: str = Field(default_factory=now_iso)
    status: MessageStatus = "completed"
    sources: list[SourceRef] = Field(default_factory=list)
    error: str | None = None  # user-safe failure message


class Conversation(BaseModel):
    id: str = Field(default_factory=new_id)
    employee_email: str
    title: str = "New conversation"
    created_at: str = Field(default_factory=now_iso)
    updated_at: str = Field(default_factory=now_iso)
    messages: list[ChatMessage] = Field(default_factory=list)


class ConversationSummary(BaseModel):
    id: str
    title: str
    created_at: str
    updated_at: str
    message_count: int
    last_message_preview: str | None = None


class CreateConversationRequest(BaseModel):
    employee_email: Email
    title: Annotated[str, Field(max_length=120)] | None = None


class RenameConversationRequest(BaseModel):
    employee_email: Email
    title: Annotated[str, Field(min_length=1, max_length=120)]

    @field_validator("title")
    @classmethod
    def _title(cls, v: str) -> str:
        v = " ".join(v.split())
        if not v:
            raise ValueError("title must not be blank")
        return v


class ChatStreamRequest(BaseModel):
    conversation_id: str | None = None
    employee_email: Email
    message: Annotated[str, Field(min_length=1, max_length=4000)]

    @field_validator("message")
    @classmethod
    def _message(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("message must not be blank")
        return v
