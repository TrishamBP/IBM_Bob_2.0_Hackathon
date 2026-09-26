"""Application settings loaded from environment variables and .env."""

from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

MB = 1024 * 1024


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "IBM Bob Backend"
    environment: str = "development"
    cors_origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # Fireworks AI (server-side only; never expose through NEXT_PUBLIC_* variables)
    fireworks_api_key: SecretStr = SecretStr("")
    fireworks_base_url: str = "https://api.fireworks.ai/inference/v1"
    fireworks_timeout_seconds: float = 30.0
    fireworks_max_retries: int = 4
    fireworks_embedding_model: str = "fireworks/qwen3-embedding-8b"
    fireworks_embedding_dimensions: int = Field(default=356, ge=32, le=4096)
    fireworks_embedding_batch_size: int = Field(default=32, ge=1, le=2048)
    fireworks_embedding_max_concurrency: int = Field(default=4, ge=1)
    # Qwen3 embedding models expect an instruction prefix on queries (not on documents).
    fireworks_query_instruction: str = (
        "Given an ACME Corp employee onboarding question, retrieve relevant internal "
        "documentation passages that answer it"
    )
    fireworks_reranker_model: str = ""
    # Optional full URL override (e.g. a dedicated deployment); defaults to {base_url}/rerank.
    fireworks_reranker_url: str = ""
    fireworks_reranker_task: str = (
        "Given an ACME Corp employee onboarding question, judge whether the passage answers it"
    )
    fireworks_reranker_max_candidates: int = Field(default=40, ge=1)

    # DeepSeek V4.1 Flash via Fireworks — query expansion, HyDE and semantic ingestion
    fireworks_llm_model: str = "accounts/fireworks/models/deepseek-v4p1-flash"
    fireworks_llm_timeout_seconds: float = Field(default=45.0, ge=1.0)
    fireworks_llm_max_tokens: int = Field(default=1024, ge=64)
    fireworks_llm_temperature: float = Field(default=0.3, ge=0.0, le=2.0)

    # Query preprocessing pipeline
    query_expansion_count: int = Field(default=3, ge=1, le=10)
    hyde_enabled: bool = True
    # Fusion weights (must sum to 1.0 at runtime; validated in FusionConfig)
    fusion_xgboost_weight: float = Field(default=0.20, ge=0.0, le=1.0)
    fusion_reranker_weight: float = Field(default=0.80, ge=0.0, le=1.0)
    # How many cross-department candidate chunks to fetch for the reranker
    fusion_retrieval_candidates: int = Field(default=40, ge=1)
    # Maximum alternative departments retained in routing result
    fusion_max_alternatives: int = Field(default=2, ge=0)

    # Employee chat (POST /api/v1/chat/stream)
    # GLM 5.3 Flash writes the streamed Markdown answer.
    fireworks_answer_model: str = "accounts/fireworks/models/glm-5p3-flash"
    fireworks_answer_max_tokens: int = Field(default=12000, ge=128)  # includes reasoning
    # Answer length the prompt asks for; the rest of max_tokens is left for reasoning.
    fireworks_answer_target_tokens: int = Field(default=3000, ge=100)
    fireworks_answer_temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    fireworks_answer_timeout_seconds: float = Field(default=60.0, ge=1.0)  # per network read
    fireworks_answer_reasoning_effort: str = ""  # "" to omit the parameter
    # DeepSeek (FIREWORKS_LLM_MODEL) query expansion, HyDE and follow-up resolution
    chat_preprocess_max_tokens: int = Field(default=2048, ge=128)  # includes reasoning
    chat_preprocess_reasoning_effort: str = "low"
    chat_preprocess_timeout_seconds: float = Field(default=30.0, ge=1.0)
    chat_dir: str = "data/chats"
    chat_history_turns: int = Field(default=4, ge=0, le=20)
    chat_followup_mode: str = Field(default="auto", pattern="^(auto|always|never)$")
    chat_max_concurrent_streams: int = Field(default=8, ge=1)
    chat_context_token_budget: int = Field(default=6000, ge=500)
    # Department filters: "routed" (primary + alternatives when unsure) or "none"
    chat_department_filter: str = Field(default="routed", pattern="^(routed|none)$")
    chat_low_confidence_threshold: float = Field(default=0.55, ge=0.0, le=1.0)
    chat_max_filter_departments: int = Field(default=3, ge=1, le=13)
    # Hybrid retrieval: candidates per query vector / BM25, RRF and MMR
    retrieval_semantic_k: int = Field(default=30, ge=1, le=200)
    retrieval_bm25_k: int = Field(default=30, ge=1, le=200)
    retrieval_fusion_candidates: int = Field(default=60, ge=1, le=400)
    retrieval_top_k: int = Field(default=20, ge=1, le=20)
    rrf_k: int = Field(default=60, ge=0)
    rrf_weight_original: float = Field(default=1.0, ge=0.0)
    rrf_weight_expansions: float = Field(default=1.0, ge=0.0)  # total over all expansions
    rrf_weight_hyde: float = Field(default=0.7, ge=0.0)
    rrf_weight_bm25: float = Field(default=1.0, ge=0.0)
    rrf_weight_bm25_expansions: float = Field(default=0.3, ge=0.0)
    mmr_lambda: float = Field(default=0.7, ge=0.0, le=1.0)
    mmr_duplicate_threshold: float = Field(default=0.97, ge=0.0, le=1.0)
    mmr_max_chunks_per_document: int = Field(default=8, ge=1)
    # Evidence thresholds (cosine vs. original/expansion query vectors; raw BM25 scores)
    evidence_min_similarity: float = Field(default=0.35, ge=-1.0, le=1.0)
    evidence_min_bm25: float = Field(default=3.0, ge=0.0)
    evidence_sufficient_similarity: float = Field(default=0.45, ge=-1.0, le=1.0)
    evidence_sufficient_bm25: float = Field(default=6.0, ge=0.0)

    # LLM tracing via deepeval, a dev-only dependency (`uv sync --group eval`). Each chat
    # turn prints a span tree to the terminal; a no-op when deepeval is not installed.
    tracing_enabled: bool = True
    tracing_terminal: bool = True
    tracing_preview_chars: int = Field(default=160, ge=0, le=4000)

    documents_dir: str = "data/documents"
    chroma_persist_dir: str = "data/chroma"
    chroma_collection: str = "acme_onboarding_v2"

    # Upload limits (enforced server-side regardless of the frontend)
    upload_max_files: int = Field(default=10, ge=1)
    upload_max_file_bytes: int = Field(default=50 * MB, ge=1)
    upload_max_request_bytes: int = Field(default=200 * MB, ge=1)

    # Semantic ingestion: DeepSeek (FIREWORKS_LLM_MODEL) structures uploaded documents.
    # Disabled or failing LLM -> deterministic structural sections (recorded per chunk).
    ingestion_llm_enabled: bool = True
    ingestion_llm_max_tokens: int = Field(default=8192, ge=256)  # includes reasoning tokens
    ingestion_llm_temperature: float = Field(default=0.0, ge=0.0, le=2.0)
    ingestion_llm_reasoning_effort: str = "low"  # "" to omit the parameter
    ingestion_llm_timeout_seconds: float = Field(default=120.0, ge=1.0)
    ingestion_llm_max_attempts: int = Field(default=3, ge=1, le=10)
    ingestion_llm_max_concurrency: int = Field(default=2, ge=1)
    ingestion_metadata_max_chars: int = Field(default=20_000, ge=1000)
    # Block previews sent per segmentation request, and the per-document request cap.
    ingestion_segmentation_window_chars: int = Field(default=24_000, ge=2000)
    ingestion_segmentation_max_windows: int = Field(default=12, ge=1)
    ingestion_block_preview_chars: int = Field(default=240, ge=60)
    # Chunk limits in approximate tokens (words + punctuation, see semantic/tokens.py)
    semantic_chunk_max_tokens: int = Field(default=450, ge=50)
    semantic_chunk_overlap_tokens: int = Field(default=40, ge=0)


@lru_cache
def get_settings() -> Settings:
    return Settings()
