"""JSON file storage for chat conversations: ``<chat_dir>/<conversation_id>.json``.

- Conversation ids must be canonical UUIDs, so a path can never escape the directory.
- Writes go to a temporary file in the same directory and are moved into place with
  ``os.replace`` (atomic on POSIX and Windows), so readers never see a partial file.
- Updates to one conversation are serialized with a per-conversation ``asyncio.Lock``.
- File I/O runs in worker threads and never blocks the event loop.
"""

from __future__ import annotations

import asyncio
import contextlib
import os
import tempfile
import uuid
import weakref
from collections.abc import AsyncIterator, Callable
from pathlib import Path

from src.rag.chat.schemas import Conversation, ConversationSummary, now_iso


class InvalidConversationId(ValueError):
    pass


class ConversationNotFound(LookupError):
    pass


def validate_conversation_id(value: str) -> str:
    try:
        parsed = uuid.UUID(value)
    except (ValueError, AttributeError, TypeError) as exc:
        raise InvalidConversationId("Invalid conversation id") from exc
    if str(parsed) != value.lower():
        raise InvalidConversationId("Invalid conversation id")
    return str(parsed)


class ChatStorage:
    def __init__(self, directory: str | Path) -> None:
        self.directory = Path(directory)
        self._locks: weakref.WeakValueDictionary[str, asyncio.Lock] = weakref.WeakValueDictionary()

    def _path(self, conversation_id: str) -> Path:
        return self.directory / f"{validate_conversation_id(conversation_id)}.json"

    def _lock(self, conversation_id: str) -> asyncio.Lock:
        lock = self._locks.get(conversation_id)
        if lock is None:
            lock = asyncio.Lock()
            self._locks[conversation_id] = lock
        return lock

    @contextlib.asynccontextmanager
    async def locked(self, conversation_id: str) -> AsyncIterator[None]:
        conversation_id = validate_conversation_id(conversation_id)
        lock = self._lock(conversation_id)  # strong reference held for the block
        async with lock:
            yield

    # ------------------------------------------------------------------ sync helpers

    def _read_sync(self, path: Path) -> Conversation:
        try:
            data = path.read_text(encoding="utf-8")
        except FileNotFoundError as exc:
            raise ConversationNotFound(path.stem) from exc
        return Conversation.model_validate_json(data)

    def _write_sync(self, conversation: Conversation) -> None:
        self.directory.mkdir(parents=True, exist_ok=True)
        path = self._path(conversation.id)
        data = conversation.model_dump_json(indent=2)
        fd, tmp = tempfile.mkstemp(dir=self.directory, prefix=f".{conversation.id}.", suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp, path)
        except BaseException:
            with contextlib.suppress(FileNotFoundError):
                os.unlink(tmp)
            raise

    def _list_sync(self) -> list[Conversation]:
        if not self.directory.exists():
            return []
        conversations = []
        for path in self.directory.glob("*.json"):
            try:
                validate_conversation_id(path.stem)
                conversations.append(self._read_sync(path))
            except (InvalidConversationId, ConversationNotFound, ValueError):
                continue  # foreign, removed or corrupt file: skip, never crash the listing
        return conversations

    # ------------------------------------------------------------------ public API

    async def get(self, conversation_id: str) -> Conversation:
        return await asyncio.to_thread(self._read_sync, self._path(conversation_id))

    async def save(self, conversation: Conversation) -> None:
        async with self.locked(conversation.id):
            await asyncio.to_thread(self._write_sync, conversation)

    async def create(self, conversation: Conversation) -> Conversation:
        await self.save(conversation)
        return conversation

    async def update(
        self, conversation_id: str, mutate: Callable[[Conversation], None]
    ) -> Conversation:
        """Read-modify-write under the conversation's lock."""
        async with self.locked(conversation_id):
            conversation = await asyncio.to_thread(self._read_sync, self._path(conversation_id))
            mutate(conversation)
            conversation.updated_at = now_iso()
            await asyncio.to_thread(self._write_sync, conversation)
            return conversation

    async def delete(self, conversation_id: str) -> None:
        path = self._path(conversation_id)
        async with self.locked(conversation_id):
            try:
                await asyncio.to_thread(path.unlink)
            except FileNotFoundError as exc:
                raise ConversationNotFound(conversation_id) from exc

    async def list_for(self, employee_email: str) -> list[ConversationSummary]:
        conversations = await asyncio.to_thread(self._list_sync)
        summaries = []
        for c in conversations:
            if c.employee_email != employee_email:
                continue
            last = next((m for m in reversed(c.messages) if m.content), None)
            summaries.append(
                ConversationSummary(
                    id=c.id,
                    title=c.title,
                    created_at=c.created_at,
                    updated_at=c.updated_at,
                    message_count=len(c.messages),
                    last_message_preview=last.content[:120] if last else None,
                )
            )
        summaries.sort(key=lambda s: s.updated_at, reverse=True)
        return summaries
