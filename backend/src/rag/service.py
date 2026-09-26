"""Container for the long-lived RAG services, created once in the app lifespan."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from src.chroma.client import ChromaStore
from src.config import Settings
from src.rag.chat.context import FollowUpResolver
from src.rag.chat.service import ChatConfig, ChatService
from src.rag.chat.storage import ChatStorage
from src.rag.embeddings import (
    build_answer_llm,
    build_embedder,
    build_fireworks_client,
    build_ingestion_llm,
    build_preprocess_llm,
    build_reranker,
)
from src.rag.fireworks import FireworksClient, FireworksEmbeddings
from src.rag.ingestion import IngestionService
from src.rag.retrieval import BM25Index, EvidenceConfig, HybridRetriever, RetrievalConfig
from src.rag.retriever import DepartmentBalancedRetriever
from src.rag.router.fusion import FusionConfig, FusionRouter
from src.rag.router.router import DepartmentRouter
from src.rag.semantic import MetadataGenerator, SemanticSegmenter

logger = logging.getLogger(__name__)


@dataclass
class RagServices:
    client: FireworksClient
    embedder: FireworksEmbeddings
    store: ChromaStore
    ingestion: IngestionService
    router: DepartmentRouter
    fusion: FusionRouter | None
    chat: ChatService | None = None

    async def aclose(self) -> None:
        await self.client.aclose()


async def create_services(settings: Settings, **client_kwargs) -> RagServices | None:
    """Build services, or return ``None`` when Fireworks is not configured."""
    if not settings.fireworks_api_key.get_secret_value():
        logger.warning("FIREWORKS_API_KEY is not set; RAG endpoints will return 503")
        return None
    client = build_fireworks_client(settings, **client_kwargs)
    embedder = build_embedder(settings, client)
    store = ChromaStore(
        settings.chroma_persist_dir,
        settings.chroma_collection,
        embedding_model=embedder.model,
        embedding_dimensions=embedder.dimensions,
    )
    try:
        await store.open()
    except Exception:
        await client.aclose()
        raise
    router = DepartmentRouter(embedder)
    reranker = build_reranker(settings, client)
    fusion = (
        FusionRouter(
            router,
            DepartmentBalancedRetriever(store),
            reranker,
            FusionConfig(
                xgboost_weight=settings.fusion_xgboost_weight,
                reranker_weight=settings.fusion_reranker_weight,
                max_rerank_candidates=settings.fireworks_reranker_max_candidates,
            ),
        )
        if reranker is not None
        else None
    )
    if fusion is None:
        logger.warning("FIREWORKS_RERANKER_MODEL is not set; fusion routing is disabled")
    ingestion = build_ingestion(settings, client, embedder, store)
    chat = build_chat(settings, client, embedder, store, router, fusion)
    return RagServices(client, embedder, store, ingestion, router, fusion, chat)


def build_chat(
    settings: Settings,
    client: FireworksClient,
    embedder: FireworksEmbeddings,
    store: ChromaStore,
    router: DepartmentRouter,
    fusion: FusionRouter | None,
    storage: ChatStorage | None = None,
) -> ChatService:
    retriever = HybridRetriever(
        store,
        BM25Index(store),
        RetrievalConfig(
            semantic_k=settings.retrieval_semantic_k,
            bm25_k=settings.retrieval_bm25_k,
            rrf_k=settings.rrf_k,
            weight_original=settings.rrf_weight_original,
            weight_expansions=settings.rrf_weight_expansions,
            weight_hyde=settings.rrf_weight_hyde,
            weight_bm25=settings.rrf_weight_bm25,
            weight_bm25_expansions=settings.rrf_weight_bm25_expansions,
            fusion_candidates=settings.retrieval_fusion_candidates,
            top_k=settings.retrieval_top_k,
            mmr_lambda=settings.mmr_lambda,
            mmr_duplicate_threshold=settings.mmr_duplicate_threshold,
            max_chunks_per_document=settings.mmr_max_chunks_per_document,
            evidence=EvidenceConfig(
                min_similarity=settings.evidence_min_similarity,
                min_bm25_score=settings.evidence_min_bm25,
                sufficient_similarity=settings.evidence_sufficient_similarity,
                sufficient_bm25_score=settings.evidence_sufficient_bm25,
            ),
        ),
    )
    preprocess_llm = build_preprocess_llm(settings, client)
    extra = (
        {"reasoning_effort": settings.chat_preprocess_reasoning_effort}
        if settings.chat_preprocess_reasoning_effort
        else None
    )
    return ChatService(
        storage or ChatStorage(settings.chat_dir),
        embedder=embedder,
        router=router,
        fusion=fusion,
        retriever=retriever,
        answer_llm=build_answer_llm(settings, client),
        preprocess_llm=preprocess_llm,
        resolver=FollowUpResolver(
            preprocess_llm, mode=settings.chat_followup_mode, llm_extra=extra
        ),
        config=ChatConfig(
            history_turns=settings.chat_history_turns,
            expansion_count=settings.query_expansion_count,
            hyde_enabled=settings.hyde_enabled,
            context_token_budget=settings.chat_context_token_budget,
            department_filter_mode=settings.chat_department_filter,
            low_confidence_threshold=settings.chat_low_confidence_threshold,
            max_filter_departments=settings.chat_max_filter_departments,
            max_concurrent_streams=settings.chat_max_concurrent_streams,
        ),
        preprocess_extra=extra,
    )


def build_ingestion(
    settings: Settings,
    client: FireworksClient,
    embedder: FireworksEmbeddings,
    store: ChromaStore,
) -> IngestionService:
    llm = build_ingestion_llm(settings, client)
    if llm is None:
        logger.warning("Semantic ingestion LLM disabled; using structural segmentation only")
    extra = (
        {"reasoning_effort": settings.ingestion_llm_reasoning_effort}
        if settings.ingestion_llm_reasoning_effort
        else None
    )
    attempts = settings.ingestion_llm_max_attempts
    return IngestionService(
        store,
        embedder,
        metadata=MetadataGenerator(
            llm,
            max_attempts=attempts,
            max_input_chars=settings.ingestion_metadata_max_chars,
            llm_extra=extra,
        ),
        segmenter=SemanticSegmenter(
            llm,
            max_attempts=attempts,
            window_chars=settings.ingestion_segmentation_window_chars,
            preview_chars=settings.ingestion_block_preview_chars,
            max_windows=settings.ingestion_segmentation_max_windows,
            max_concurrency=settings.ingestion_llm_max_concurrency,
            llm_extra=extra,
        ),
        max_chunk_tokens=settings.semantic_chunk_max_tokens,
        overlap_tokens=settings.semantic_chunk_overlap_tokens,
        llm_model=settings.fireworks_llm_model,
    )
