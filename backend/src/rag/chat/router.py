"""Chat HTTP endpoints (demo identity: ``employee_email`` is supplied, not verified).

- ``POST   /api/v1/chat``            create an empty conversation
- ``GET    /api/v1/chat``            list the employee's conversations
- ``GET    /api/v1/chat/{id}``       conversation with messages
- ``PATCH  /api/v1/chat/{id}``       rename
- ``DELETE /api/v1/chat/{id}``       delete
- ``POST   /api/v1/chat/stream``     send a message; Server-Sent Events response

A conversation owned by another email is reported as 404, like a missing one.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Request, Response, status
from fastapi.responses import StreamingResponse
from pydantic import ValidationError

from src.rag.chat.schemas import (
    ChatStreamRequest,
    Conversation,
    ConversationSummary,
    CreateConversationRequest,
    RenameConversationRequest,
    normalize_email,
)
from src.rag.chat.service import ChatService, ConversationAccessError
from src.rag.chat.storage import ChatStorage, InvalidConversationId
from src.rag.generation import SSE_HEADERS

router = APIRouter(prefix="/chat", tags=["chat"])

EmailQuery = Annotated[str, Query(min_length=3, max_length=254)]


def _storage(request: Request) -> ChatStorage:
    storage: ChatStorage | None = getattr(request.app.state, "chat_storage", None)
    if storage is None:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Chat storage is unavailable")
    return storage


def _service(request: Request) -> ChatService:
    service: ChatService | None = getattr(request.app.state, "chat", None)
    if service is None:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            "The assistant is unavailable: the AI service is not configured",
        )
    return service


def _email(value: str) -> str:
    try:
        return normalize_email(value)
    except ValueError as exc:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)) from exc


async def _owned(storage: ChatStorage, conversation_id: str, email: str) -> Conversation:
    try:
        conversation = await storage.get(conversation_id)
    except InvalidConversationId as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid conversation id") from exc
    except LookupError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Conversation not found") from exc
    if conversation.employee_email != email:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Conversation not found")
    return conversation


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_conversation(request: Request, body: CreateConversationRequest) -> Conversation:
    conversation = Conversation(employee_email=body.employee_email)
    if body.title and body.title.strip():
        conversation.title = " ".join(body.title.split())
    return await _storage(request).create(conversation)


@router.get("")
async def list_conversations(
    request: Request, employee_email: EmailQuery
) -> list[ConversationSummary]:
    return await _storage(request).list_for(_email(employee_email))


@router.get("/{conversation_id}")
async def get_conversation(
    request: Request, conversation_id: str, employee_email: EmailQuery
) -> Conversation:
    return await _owned(_storage(request), conversation_id, _email(employee_email))


@router.patch("/{conversation_id}")
async def rename_conversation(
    request: Request, conversation_id: str, body: RenameConversationRequest
) -> Conversation:
    storage = _storage(request)
    await _owned(storage, conversation_id, body.employee_email)

    def rename(conversation: Conversation) -> None:
        conversation.title = body.title

    try:
        return await storage.update(conversation_id, rename)
    except LookupError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Conversation not found") from exc


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    request: Request, conversation_id: str, employee_email: EmailQuery
) -> Response:
    storage = _storage(request)
    await _owned(storage, conversation_id, _email(employee_email))
    try:
        await storage.delete(conversation_id)
    except LookupError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Conversation not found") from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/stream")
async def stream_chat(request: Request) -> StreamingResponse:
    try:
        body = ChatStreamRequest.model_validate(await request.json())
    except (ValidationError, ValueError) as exc:
        detail = (
            "; ".join(e["msg"] for e in exc.errors())
            if isinstance(exc, ValidationError)
            else "Request body must be JSON"
        )
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail) from exc
    service = _service(request)
    if body.conversation_id is not None:
        try:
            await service.get_owned(body.conversation_id, body.employee_email)
        except InvalidConversationId as exc:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid conversation id") from exc
        except ConversationAccessError as exc:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Conversation not found") from exc
        if service.is_busy(body.conversation_id):
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                "A response is already being generated in this conversation",
            )
    return StreamingResponse(
        service.stream(body, is_disconnected=request.is_disconnected),
        media_type="text/event-stream",
        headers=SSE_HEADERS,
    )
