"""HyDE — Hypothetical Document Embeddings.

Generates a fictional but plausible internal knowledge-base article that could
answer the employee's question, then embeds it using the Fireworks embedding
model.

The hypothetical document is a retrieval aid: its embedding is used for
similarity search, not presented to employees as authoritative policy.

Any failure (LLM or embedding) is captured as a ``HyDEResult`` with
``status=FAILED`` rather than propagating an exception.
"""

from __future__ import annotations

import logging

from pydantic import BaseModel, Field

from src.rag.fireworks.embeddings import FireworksEmbeddings
from src.rag.fireworks.llm import FireworksLLM, LLMError
from src.rag.preprocessing.prompts import HYDE_CONVERSATION_CONTEXT, HYDE_SYSTEM, HYDE_USER
from src.rag.preprocessing.schemas import HyDEResult, StageStatus

logger = logging.getLogger(__name__)

_MIN_DOC_WORDS = 10
_MAX_DOC_CHARS = 4000


# ---------------------------------------------------------------------------
# LLM response schema (internal)
# ---------------------------------------------------------------------------


class _HyDEResponse(BaseModel):
    document: str = Field(default="")


# ---------------------------------------------------------------------------
# HyDE generation
# ---------------------------------------------------------------------------


async def generate_hyde(
    llm: FireworksLLM,
    embeddings: FireworksEmbeddings | None,
    query: str,
    department: str,
    *,
    conversation_context: str | None = None,
    extra: dict | None = None,
) -> HyDEResult:
    """Generate a hypothetical document and embed it.

    Parameters
    ----------
    llm:
        Configured :class:`FireworksLLM` instance.
    embeddings:
        Configured :class:`FireworksEmbeddings` instance, or ``None`` to return the
        document without embedding it (the caller batches the embedding request).
    query:
        The original employee question.
    department:
        Primary department determined by the fusion router.

    Returns
    -------
    :class:`HyDEResult` — always returns; failures are captured in the result.
    """
    if not query.strip():
        return HyDEResult(
            status=StageStatus.FAILED,
            error="Query must not be empty",
        )

    # ── Step 1: Generate hypothetical document ───────────────────────────
    system_prompt = HYDE_SYSTEM
    user_prompt = HYDE_USER.format(query=query, department=department)
    if conversation_context:
        user_prompt += HYDE_CONVERSATION_CONTEXT.format(context=conversation_context)

    try:
        parsed: _HyDEResponse = await llm.complete_json(
            system_prompt,
            user_prompt,
            _HyDEResponse,
            extra=extra,
        )
    except LLMError as exc:
        logger.warning("HyDE LLM generation failed: %s", exc)
        return HyDEResult(status=StageStatus.FAILED, error=str(exc))
    except Exception as exc:  # noqa: BLE001
        logger.exception("Unexpected error during HyDE generation: %s", exc)
        return HyDEResult(
            status=StageStatus.FAILED,
            error=f"Unexpected error during document generation: {exc}",
        )

    doc_text = parsed.document.strip()

    # Basic sanity checks — the model sometimes returns very short strings
    if not doc_text:
        return HyDEResult(
            status=StageStatus.FAILED,
            error="LLM returned an empty hypothetical document",
        )
    if len(doc_text.split()) < _MIN_DOC_WORDS:
        return HyDEResult(
            status=StageStatus.FAILED,
            error=f"Hypothetical document is too short ({len(doc_text.split())} words)",
        )

    # Truncate excessively long responses before embedding
    if len(doc_text) > _MAX_DOC_CHARS:
        logger.warning("HyDE document truncated from %d to %d chars", len(doc_text), _MAX_DOC_CHARS)
        doc_text = doc_text[:_MAX_DOC_CHARS]

    if embeddings is None:
        return HyDEResult(hypothetical_document=doc_text, status=StageStatus.COMPLETED)

    # ── Step 2: Embed the hypothetical document ──────────────────────────
    try:
        embedding_matrix = await embeddings.embed_documents([doc_text])
        embedding_vector = embedding_matrix[0].tolist()
    except Exception as exc:  # noqa: BLE001
        logger.warning("HyDE embedding failed: %s", exc)
        # Return the document text even if embedding failed
        return HyDEResult(
            hypothetical_document=doc_text,
            embedding=[],
            embedding_dimensions=0,
            status=StageStatus.FAILED,
            error=f"Embedding failed: {exc}",
        )

    return HyDEResult(
        hypothetical_document=doc_text,
        embedding=embedding_vector,
        embedding_dimensions=len(embedding_vector),
        status=StageStatus.COMPLETED,
    )
