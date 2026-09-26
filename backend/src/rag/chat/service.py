"""Chat orchestration: one employee message -> streamed, cited Markdown answer.

Stages (each reported to the client as a ``status`` SSE event):

1. Load the conversation and its history window; persist the user message and an
   assistant placeholder (``status="streaming"``).
2. Resolve a context-dependent follow-up into a standalone query (DeepSeek).
3. Embed the resolved query once; XGBoost + Qwen3 reranker fusion routing reuses it.
4. Query expansion and HyDE run concurrently (DeepSeek).
5. Expansions and the HyDE document are embedded in one batched request; the routing
   embedding of the original query is reused, never recomputed.
6. Hybrid retrieval (ChromaDB + BM25) -> RRF -> evidence filter -> MMR (<= 20 chunks).
7. GLM 5.3 Flash streams the answer; citations are validated against the sources.
8. The assistant message is persisted as ``completed``, ``failed`` or ``cancelled``.
   Partial output is never saved as completed.
"""

from __future__ import annotations

import asyncio
import logging
import re
import time
from collections.abc import AsyncIterator, Awaitable, Callable
from dataclasses import dataclass
from typing import Any

import numpy as np

from src.rag.chat.context import FollowUpResolver, format_history, history_window, make_title
from src.rag.chat.schemas import (
    ChatMessage,
    ChatStreamRequest,
    Conversation,
    SourceRef,
    now_iso,
)
from src.rag.chat.storage import ChatStorage, ConversationNotFound
from src.rag.fireworks import FireworksAPIError, FireworksEmbeddings, FireworksError, FireworksLLM
from src.rag.generation import (
    AnswerLLM,
    GenerationStats,
    Source,
    build_sources,
    format_documents,
    sse_event,
    validate_citations,
)
from src.rag.generation.prompts import (
    ANSWER_SYSTEM,
    ANSWER_USER,
    RESOLVED_NOTE,
    WEAK_EVIDENCE_NOTE,
)
from src.rag.preprocessing.hyde import generate_hyde
from src.rag.preprocessing.query_expansion import expand_query
from src.rag.preprocessing.schemas import HyDEResult, QueryExpansionResult, StageStatus
from src.rag.retrieval import HybridRetriever, QueryVectors, RetrievalResult, plan_departments
from src.rag.router.fusion import FusionRouter
from src.rag.router.router import DepartmentRouter

logger = logging.getLogger(__name__)

_MARKERS = re.compile(r"\s?\[S\d+(?:\s*[,;]\s*S\d+)*\]")

NO_DOCUMENTS_ANSWER = (
    "There are no onboarding documents in the ACME knowledge base yet, so I can't answer "
    "this from ACME documentation. Please ask HR to upload the relevant documents."
)
NOT_FOUND_ANSWER = (
    "I couldn't find information about this in the ACME onboarding documents, so I can't "
    "give you an ACME-specific answer. Try rephrasing with specific terms (the tool, team "
    "or policy name), or ask your manager or HR contact."
)


class ConversationAccessError(LookupError):
    """Unknown conversation, or it belongs to another employee (reported as 404)."""


class GenerationError(RuntimeError):
    pass


@dataclass(frozen=True)
class ChatConfig:
    history_turns: int = 4
    expansion_count: int = 3
    hyde_enabled: bool = True
    context_token_budget: int = 6000
    department_filter_mode: str = "routed"
    low_confidence_threshold: float = 0.55
    max_filter_departments: int = 3
    max_concurrent_streams: int = 8
    disconnect_check_every: int = 8  # tokens


def user_safe_error(exc: BaseException) -> str:
    if isinstance(exc, FireworksAPIError) and exc.status_code == 429:
        return "The AI service is rate-limited right now. Please try again in a moment."
    if isinstance(exc, FireworksError | GenerationError):
        return "The assistant could not generate a response. Please try again."
    return "Something went wrong while answering. Please try again."


class ChatService:
    def __init__(
        self,
        storage: ChatStorage,
        *,
        embedder: FireworksEmbeddings,
        router: DepartmentRouter | None,
        fusion: FusionRouter | None,
        retriever: HybridRetriever,
        answer_llm: AnswerLLM,
        preprocess_llm: FireworksLLM | None,
        resolver: FollowUpResolver,
        config: ChatConfig | None = None,
        preprocess_extra: dict | None = None,
    ) -> None:
        self.storage = storage
        self.embedder = embedder
        self.router = router
        self.fusion = fusion
        self.retriever = retriever
        self.answer_llm = answer_llm
        self.preprocess_llm = preprocess_llm
        self.resolver = resolver
        self.config = config or ChatConfig()
        self.preprocess_extra = preprocess_extra
        self._streams = asyncio.Semaphore(self.config.max_concurrent_streams)
        self._active: set[str] = set()

    # ------------------------------------------------------------------ access

    async def get_owned(self, conversation_id: str, employee_email: str) -> Conversation:
        try:
            conversation = await self.storage.get(conversation_id)
        except ConversationNotFound as exc:
            raise ConversationAccessError(conversation_id) from exc
        if conversation.employee_email != employee_email:
            raise ConversationAccessError(conversation_id)
        return conversation

    def is_busy(self, conversation_id: str) -> bool:
        return conversation_id in self._active

    # ------------------------------------------------------------------ streaming

    async def stream(
        self,
        request: ChatStreamRequest,
        *,
        is_disconnected: Callable[[], Awaitable[bool]] | None = None,
    ) -> AsyncIterator[str]:
        """Yield SSE frames for one turn. Validate access with :meth:`get_owned` first."""
        started = time.perf_counter()
        timings: dict[str, float] = {}
        conversation_id = request.conversation_id
        if conversation_id and conversation_id in self._active:
            yield sse_event(
                "error",
                {
                    "code": "conversation_busy",
                    "message": "A response is already being generated in this conversation.",
                },
            )
            return

        final_status = "cancelled"
        final_content = ""
        final_error: str | None = None
        final_sources: list[SourceRef] = []
        assistant: ChatMessage | None = None
        persisted = False

        if conversation_id:
            self._active.add(conversation_id)  # reserved before any await: no double streams
        acquired = False
        try:
            await self._streams.acquire()
            acquired = True
            # 1. session
            conversation, history = await self._open_turn(request)
            conversation_id = conversation.id
            self._active.add(conversation_id)
            user_msg, assistant = conversation.messages[-2], conversation.messages[-1]
            yield sse_event(
                "session",
                {
                    "conversation_id": conversation.id,
                    "title": conversation.title,
                    "user_message_id": user_msg.id,
                    "assistant_message_id": assistant.id,
                    "created": request.conversation_id is None,
                    "user_message": user_msg.model_dump(),
                },
            )
            timings["session_ms"] = _ms(started)

            # 2. conversational context
            if history:
                yield _status("resolving_context", "Understanding your follow-up question")
            t = time.perf_counter()
            resolved = await self.resolver.resolve(request.message, history)
            timings["resolve_ms"] = _ms(t)

            # 3. routing (the query embedding is computed once and reused)
            yield _status("routing", "Identifying the relevant department")
            t = time.perf_counter()
            query_vector = await self.embedder.embed_query(resolved.query)
            route, route_error = await self._route(resolved.query, query_vector)
            departments = plan_departments(
                route,
                mode=self.config.department_filter_mode,
                low_confidence_threshold=self.config.low_confidence_threshold,
                max_departments=self.config.max_filter_departments,
            )
            primary = route["primary_department"] if route else None
            alternatives = [d for d in (departments or []) if d != primary]
            timings["routing_ms"] = _ms(t)
            if await _gone(is_disconnected):
                return

            # 4. expansion + HyDE (concurrent)
            yield _status(
                "expanding",
                "Expanding your question",
                department=primary,
                departments=departments,
            )
            t = time.perf_counter()
            expansion, hyde = await self._expand(resolved.query, primary, alternatives, history)
            timings["expansion_hyde_ms"] = _ms(t)

            # 5. batched embedding of expansions + HyDE
            yield _status("retrieving", "Searching onboarding documents")
            t = time.perf_counter()
            vectors, embed_error = await self._embed_inputs(query_vector, expansion, hyde)
            timings["embedding_ms"] = _ms(t)

            # 6. hybrid retrieval
            t = time.perf_counter()
            expansions_used = expansion.queries if vectors.expansions.size else []
            retrieval = await self.retriever.retrieve(
                resolved.query, expansions_used, vectors, departments
            )
            timings["retrieval_ms"] = _ms(t)
            if await _gone(is_disconnected):
                return

            # 7. answer
            stats = GenerationStats()
            sources: list[Source] = []
            invalid: list[str] = []
            if not retrieval.chunks:
                final_content = (
                    NO_DOCUMENTS_ANSWER if retrieval.collection_empty else NOT_FOUND_ANSWER
                )
                yield sse_event("token", {"text": final_content})
            else:
                sources = build_sources(retrieval.chunks, self.config.context_token_budget)
                messages = self._messages(
                    history, sources, request.message, resolved.query, retrieval
                )
                yield _status("generating", "Writing the answer", sources=len(sources))
                t = time.perf_counter()
                parts: list[str] = []
                first_token_at: float | None = None
                async for token in self.answer_llm.stream(messages, stats):
                    if first_token_at is None:
                        first_token_at = time.perf_counter()
                        timings["first_token_ms"] = _ms(t)
                    parts.append(token)
                    final_content = "".join(parts)  # partial, for a cancelled save
                    yield sse_event("token", {"text": token})
                    if len(parts) % self.config.disconnect_check_every == 0 and await _gone(
                        is_disconnected
                    ):
                        return
                timings["generation_ms"] = _ms(t)
                check = validate_citations("".join(parts), sources)
                if not check.content:
                    raise GenerationError(f"empty answer (finish_reason={stats.finish_reason})")
                final_content, invalid = check.content, check.invalid
                by_id = {s.citation_id: s for s in sources}
                final_sources = [SourceRef(**by_id[c].public()) for c in check.cited]

            yield sse_event("sources", {"sources": [s.model_dump() for s in final_sources]})
            assistant_id = assistant.id
            await self._finish(
                conversation_id, assistant_id, "completed", final_content, final_sources, None
            )
            persisted = True
            final_status = "completed"
            timings["total_ms"] = _ms(started)
            yield sse_event(
                "completed",
                {
                    "conversation_id": conversation_id,
                    "message_id": assistant_id,
                    "content": final_content,
                    "sources": [s.model_dump() for s in final_sources],
                    "invalid_citations": invalid,
                    "diagnostics": self._diagnostics(
                        resolved,
                        route,
                        route_error,
                        departments,
                        expansion,
                        hyde,
                        embed_error,
                        retrieval,
                        sources,
                        stats,
                        timings,
                    ),
                },
            )
        except ConversationAccessError:
            final_status = "failed"
            yield sse_event("error", {"code": "not_found", "message": "Conversation not found."})
        except (asyncio.CancelledError, GeneratorExit):
            final_status = "cancelled"
            raise
        except Exception as exc:
            logger.exception("Chat turn failed")
            final_status = "failed"
            final_error = user_safe_error(exc)
            yield sse_event(
                "error",
                {
                    "code": "generation_failed",
                    "message": final_error,
                    "message_id": assistant.id if assistant else None,
                },
            )
        finally:
            if acquired:
                self._streams.release()
            if conversation_id:
                self._active.discard(conversation_id)
            if assistant is not None and conversation_id and not persisted:
                # Shielded: a client disconnect must not leave a "streaming" message.
                await asyncio.shield(
                    self._finish(
                        conversation_id,
                        assistant.id,
                        final_status,
                        final_content,
                        [],
                        final_error,
                    )
                )

    # ------------------------------------------------------------------ stages

    async def _open_turn(
        self, request: ChatStreamRequest
    ) -> tuple[Conversation, list[ChatMessage]]:
        user_msg = ChatMessage(role="user", content=request.message)
        assistant = ChatMessage(role="assistant", status="streaming")
        if request.conversation_id is None:
            conversation = Conversation(
                employee_email=request.employee_email,
                title=make_title(request.message),
                messages=[user_msg, assistant],
            )
            await self.storage.create(conversation)
            return conversation, []

        await self.get_owned(request.conversation_id, request.employee_email)
        history: list[ChatMessage] = []

        def add(conversation: Conversation) -> None:
            history.extend(history_window(conversation.messages, self.config.history_turns))
            if not any(m.role == "user" for m in conversation.messages):
                conversation.title = make_title(request.message)
            conversation.messages.extend([user_msg, assistant])

        conversation = await self.storage.update(request.conversation_id, add)
        return conversation, history

    async def _route(
        self, query: str, vector: np.ndarray
    ) -> tuple[dict[str, Any] | None, str | None]:
        try:
            if self.fusion is not None:
                return await self.fusion.route(query, embedding=vector), None
            if self.router is not None:
                probs = (await self.router.predict_proba_from_embeddings(vector))[0]
                order = np.argsort(-probs)
                predictions = [
                    {"department": self.router.departments[i], "final_score": float(probs[i])}
                    for i in order
                ]
                return {
                    "primary_department": predictions[0]["department"],
                    "selected_departments": [predictions[0]["department"]],
                    "predictions": predictions,
                    "diagnostics": {"evidence_used": False, "reranker_error": "disabled"},
                }, None
        except Exception as exc:  # routing degrades to an unfiltered search
            logger.warning("Routing failed; searching all departments: %s", exc)
            return None, type(exc).__name__
        return None, "router unavailable"

    async def _expand(
        self,
        query: str,
        department: str | None,
        alternatives: list[str],
        history: list[ChatMessage],
    ) -> tuple[QueryExpansionResult, HyDEResult]:
        if self.preprocess_llm is None:
            skipped = "DeepSeek preprocessing is disabled"
            return (
                QueryExpansionResult(status=StageStatus.SKIPPED, error=skipped),
                HyDEResult(status=StageStatus.SKIPPED, error=skipped),
            )
        context = format_history(history[-4:], max_chars=300) if history else None
        department = department or "General onboarding"
        tasks: list[Awaitable[Any]] = [
            expand_query(
                self.preprocess_llm,
                query,
                department,
                alternative_departments=alternatives or None,
                n=self.config.expansion_count,
                conversation_context=context,
                extra=self.preprocess_extra,
            )
        ]
        if self.config.hyde_enabled:
            tasks.append(
                generate_hyde(
                    self.preprocess_llm,
                    None,  # embedded below together with the expansions
                    query,
                    department,
                    conversation_context=context,
                    extra=self.preprocess_extra,
                )
            )
        results = await asyncio.gather(*tasks)
        hyde = results[1] if len(results) > 1 else HyDEResult(status=StageStatus.SKIPPED)
        return results[0], hyde

    async def _embed_inputs(
        self, query_vector: np.ndarray, expansion: QueryExpansionResult, hyde: HyDEResult
    ) -> tuple[QueryVectors, str | None]:
        dims = self.embedder.dimensions
        queries = expansion.queries if expansion.status == StageStatus.COMPLETED else []
        hyde_doc = hyde.hypothetical_document if hyde.status == StageStatus.COMPLETED else ""
        inputs = [self.embedder.format_query(q) for q in queries]
        if hyde_doc:
            inputs.append(hyde_doc)  # documents are embedded without the query instruction
        empty = np.empty((0, dims), dtype=np.float32)
        if not inputs:
            return QueryVectors(query_vector, empty), None
        try:
            matrix = await self.embedder.embed_documents(inputs)
        except (FireworksError, ValueError) as exc:
            logger.warning("Expansion/HyDE embedding failed; using the original query: %s", exc)
            return QueryVectors(query_vector, empty), type(exc).__name__
        if matrix.shape != (len(inputs), dims):
            return QueryVectors(query_vector, empty), f"unexpected shape {matrix.shape}"
        expansions = matrix[: len(queries)]
        hyde_vector = matrix[len(queries)] if hyde_doc else None
        return QueryVectors(query_vector, expansions, hyde_vector), None

    def _messages(
        self,
        history: list[ChatMessage],
        sources: list[Source],
        message: str,
        resolved: str,
        retrieval: RetrievalResult,
    ) -> list[dict[str, str]]:
        messages = [{"role": "system", "content": ANSWER_SYSTEM}]
        for m in history:
            # Old citation markers refer to old sources; drop them from the history.
            content = _MARKERS.sub("", m.content) if m.role == "assistant" else m.content
            messages.append({"role": m.role, "content": content})
        question = message
        if resolved != message:
            question = f"{message}\n{RESOLVED_NOTE.format(resolved=resolved)}"
        messages.append(
            {
                "role": "user",
                "content": ANSWER_USER.format(
                    documents=format_documents(sources),
                    evidence_note="" if retrieval.sufficient else WEAK_EVIDENCE_NOTE,
                    question=question,
                ),
            }
        )
        return messages

    async def _finish(
        self,
        conversation_id: str,
        message_id: str,
        status: str,
        content: str,
        sources: list[SourceRef],
        error: str | None,
    ) -> None:
        def mutate(conversation: Conversation) -> None:
            for m in conversation.messages:
                if m.id == message_id:
                    m.status = status  # type: ignore[assignment]
                    m.content = content
                    m.sources = sources
                    m.error = error
                    m.timestamp = now_iso()

        try:
            await self.storage.update(conversation_id, mutate)
        except ConversationNotFound:
            pass  # deleted while the answer was streaming

    @staticmethod
    def _diagnostics(
        resolved,
        route,
        route_error,
        departments,
        expansion: QueryExpansionResult,
        hyde: HyDEResult,
        embed_error,
        retrieval: RetrievalResult,
        sources: list[Source],
        stats: GenerationStats,
        timings: dict[str, float],
    ) -> dict[str, Any]:
        route_view = None
        if route:
            route_view = {
                "primary_department": route.get("primary_department"),
                "selected_departments": route.get("selected_departments"),
                "top": [
                    {k: p.get(k) for k in ("department", "final_score")}
                    for p in (route.get("predictions") or [])[:3]
                ],
                "fallback_used": (route.get("diagnostics") or {}).get("fallback_used"),
            }
        return {
            "resolved_query": resolved.query,
            "resolution": resolved.method,
            "routing": route_view,
            "routing_error": route_error,
            "filter_departments": departments,
            "expansion": {"status": expansion.status, "queries": expansion.queries},
            "hyde": {"status": hyde.status},
            "embedding_error": embed_error,
            "retrieval": {
                "sufficient": retrieval.sufficient,
                "reason": retrieval.reason,
                "departments": retrieval.departments,
                "chunks": len(retrieval.chunks),
                "attempts": retrieval.attempts,
            },
            "context_sources": len(sources),
            "finish_reason": stats.finish_reason,
            "usage": stats.usage,
            "timings": timings,
        }


def _status(stage: str, message: str, **extra: Any) -> str:
    return sse_event("status", {"stage": stage, "message": message, **extra})


def _ms(start: float) -> float:
    return round((time.perf_counter() - start) * 1000, 1)


async def _gone(is_disconnected: Callable[[], Awaitable[bool]] | None) -> bool:
    return bool(is_disconnected and await is_disconnected())
