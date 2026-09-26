"""Factories that build the Fireworks clients from application settings."""

from __future__ import annotations

from src.config import Settings
from src.rag.fireworks import (
    FireworksClient,
    FireworksEmbeddings,
    FireworksLLM,
    FireworksReranker,
)
from src.rag.generation.llm import AnswerLLM


def build_fireworks_client(settings: Settings, **kwargs) -> FireworksClient:
    return FireworksClient(
        settings.fireworks_api_key.get_secret_value(),
        settings.fireworks_base_url,
        timeout=settings.fireworks_timeout_seconds,
        max_retries=settings.fireworks_max_retries,
        **kwargs,
    )


def build_embedder(settings: Settings, client: FireworksClient) -> FireworksEmbeddings:
    return FireworksEmbeddings(
        client,
        settings.fireworks_embedding_model,
        settings.fireworks_embedding_dimensions,
        batch_size=settings.fireworks_embedding_batch_size,
        max_concurrency=settings.fireworks_embedding_max_concurrency,
        query_instruction=settings.fireworks_query_instruction,
    )


def build_reranker(settings: Settings, client: FireworksClient) -> FireworksReranker | None:
    if not settings.fireworks_reranker_model:
        return None
    return FireworksReranker(
        client,
        settings.fireworks_reranker_model,
        url=settings.fireworks_reranker_url,
        max_candidates=settings.fireworks_reranker_max_candidates,
        task=settings.fireworks_reranker_task,
    )


def build_ingestion_llm(settings: Settings, client: FireworksClient) -> FireworksLLM | None:
    """DeepSeek client for semantic ingestion (deterministic, larger output budget)."""
    if not settings.ingestion_llm_enabled or not settings.fireworks_llm_model:
        return None
    return FireworksLLM(
        client,
        settings.fireworks_llm_model,
        max_tokens=settings.ingestion_llm_max_tokens,
        temperature=settings.ingestion_llm_temperature,
        timeout=settings.ingestion_llm_timeout_seconds,
    )


def build_preprocess_llm(settings: Settings, client: FireworksClient) -> FireworksLLM | None:
    """DeepSeek client for query expansion, HyDE and follow-up resolution."""
    if not settings.fireworks_llm_model:
        return None
    return FireworksLLM(
        client,
        settings.fireworks_llm_model,
        max_tokens=settings.chat_preprocess_max_tokens,
        temperature=settings.fireworks_llm_temperature,
        timeout=settings.chat_preprocess_timeout_seconds,
    )


def build_answer_llm(settings: Settings, client: FireworksClient) -> AnswerLLM:
    """GLM 5.3 Flash streaming client for chat answers."""
    return AnswerLLM(
        client,
        settings.fireworks_answer_model,
        max_tokens=settings.fireworks_answer_max_tokens,
        temperature=settings.fireworks_answer_temperature,
        timeout=settings.fireworks_answer_timeout_seconds,
        reasoning_effort=settings.fireworks_answer_reasoning_effort,
    )
