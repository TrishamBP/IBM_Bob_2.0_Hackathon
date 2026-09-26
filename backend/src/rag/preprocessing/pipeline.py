"""Query preprocessing pipeline orchestrator.

Wires together the fusion router, query-expansion and HyDE modules into a
single reusable class.  All expensive components (XGBoost, embedder, reranker,
LLM) are injected at construction time and never re-initialised per request.

Usage example
-------------
::

    from src.rag.preprocessing.pipeline import QueryPreprocessingPipeline

    pipeline = QueryPreprocessingPipeline.from_settings()
    result = await pipeline.process("How do I get access to our K8s cluster?")
    print(result.to_api_dict())

"""

from __future__ import annotations

import asyncio
import logging

import chromadb

from src.config import Settings, get_settings
from src.rag.fireworks.client import FireworksClient
from src.rag.fireworks.embeddings import FireworksEmbeddings
from src.rag.fireworks.llm import FireworksLLM
from src.rag.fireworks.reranker import FireworksReranker
from src.rag.preprocessing.fusion import CandidateChunk, FusionConfig, FusionRouter
from src.rag.preprocessing.hyde import generate_hyde
from src.rag.preprocessing.query_expansion import expand_query
from src.rag.preprocessing.schemas import (
    HyDEResult,
    PreprocessingResult,
    QueryExpansionResult,
    RoutingResult,
    StageStatus,
)
from src.rag.router.router import DepartmentRouter

logger = logging.getLogger(__name__)


class QueryPreprocessingPipeline:
    """End-to-end query preprocessing: routing → expansion + HyDE.

    Inject all dependencies via the constructor.  Use :meth:`from_settings`
    as a convenient factory that reads from ``Settings``.

    Parameters
    ----------
    fusion_router:
        Loaded :class:`FusionRouter` instance.
    llm:
        Fireworks LLM client for text generation.
    embeddings:
        Fireworks embedding client (used by HyDE).
    chroma_collection:
        ChromaDB collection to query for reranker candidates.
        Pass ``None`` to disable cross-department retrieval; the pipeline
        will fall back to XGBoost-only routing gracefully.
    expansion_count:
        Number of alternative queries to generate.
    hyde_enabled:
        Whether to run HyDE.  Can be disabled for latency-sensitive paths.
    retrieval_candidates:
        How many cross-department chunks to fetch from ChromaDB.
    """

    def __init__(
        self,
        fusion_router: FusionRouter,
        llm: FireworksLLM,
        embeddings: FireworksEmbeddings,
        chroma_collection: chromadb.Collection | None = None,
        *,
        expansion_count: int = 3,
        hyde_enabled: bool = True,
        retrieval_candidates: int = 40,
    ) -> None:
        self.fusion_router = fusion_router
        self.llm = llm
        self.embeddings = embeddings
        self.chroma_collection = chroma_collection
        self.expansion_count = expansion_count
        self.hyde_enabled = hyde_enabled
        self.retrieval_candidates = retrieval_candidates

    # ------------------------------------------------------------------
    # Factory
    # ------------------------------------------------------------------

    @classmethod
    def from_settings(
        cls,
        settings: Settings | None = None,
        chroma_collection: chromadb.Collection | None = None,
    ) -> QueryPreprocessingPipeline:
        """Build a pipeline from application settings.

        Parameters
        ----------
        settings:
            Loaded :class:`Settings`; defaults to ``get_settings()``.
        chroma_collection:
            Pre-constructed ChromaDB collection.  Pass ``None`` to disable
            cross-department candidate retrieval.
        """
        s = settings or get_settings()
        api_key = s.fireworks_api_key.get_secret_value()

        http_client = FireworksClient(
            api_key=api_key,
            base_url=s.fireworks_base_url,
            timeout=s.fireworks_timeout_seconds,
            max_retries=s.fireworks_max_retries,
        )
        embeddings = FireworksEmbeddings(
            client=http_client,
            model=s.fireworks_embedding_model,
            dimensions=s.fireworks_embedding_dimensions,
            batch_size=s.fireworks_embedding_batch_size,
            max_concurrency=s.fireworks_embedding_max_concurrency,
            query_instruction=s.fireworks_query_instruction,
        )
        reranker = FireworksReranker(
            client=http_client,
            model=s.fireworks_reranker_model,
            url=s.fireworks_reranker_url,
            max_candidates=s.fireworks_reranker_max_candidates,
            task=s.fireworks_reranker_task,
        )
        llm = FireworksLLM(
            client=http_client,
            model=s.fireworks_llm_model,
            max_tokens=s.fireworks_llm_max_tokens,
            temperature=s.fireworks_llm_temperature,
            timeout=s.fireworks_llm_timeout_seconds,
        )
        xgb_router = DepartmentRouter()
        fusion_config = FusionConfig(
            xgboost_weight=s.fusion_xgboost_weight,
            reranker_weight=s.fusion_reranker_weight,
            max_alternatives=s.fusion_max_alternatives,
        )
        fusion_router = FusionRouter(
            xgb_router=xgb_router,
            reranker=reranker,
            config=fusion_config,
        )
        return cls(
            fusion_router=fusion_router,
            llm=llm,
            embeddings=embeddings,
            chroma_collection=chroma_collection,
            expansion_count=s.query_expansion_count,
            hyde_enabled=s.hyde_enabled,
            retrieval_candidates=s.fusion_retrieval_candidates,
        )

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------

    async def process(self, query: str) -> PreprocessingResult:
        """Run the full preprocessing pipeline for ``query``.

        Steps:
        1. Validate the query.
        2. Fetch cross-department candidate chunks from ChromaDB.
        3. Run fusion routing (XGBoost + Reranker).
        4. Run query expansion and HyDE *concurrently*.
        5. Return a :class:`PreprocessingResult`.

        Partial failures in steps 4–5 are captured in the result rather than
        raising exceptions.
        """
        # ── Step 1: Validate ──────────────────────────────────────────────
        query = query.strip()
        if not query:
            raise ValueError("Query must not be empty")

        # ── Step 2: Fetch candidates from ChromaDB ────────────────────────
        candidates = await self._fetch_candidates(query)

        # ── Step 3: Fusion routing ────────────────────────────────────────
        routing: RoutingResult = await self.fusion_router.route(query, candidates)
        logger.info(
            "Routing result: %s (method=%s, fusion_score=%.4f)",
            routing.primary_department,
            routing.routing_method,
            routing.fusion_score,
        )

        # ── Step 4: Concurrent expansion + HyDE ──────────────────────────
        expansion_result, hyde_result = await self._run_expansion_and_hyde(
            query=query,
            department=routing.primary_department,
            alternatives=routing.alternatives,
        )

        return PreprocessingResult(
            original_query=query,
            routing=routing,
            query_expansion=expansion_result,
            hyde=hyde_result,
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _fetch_candidates(self, query: str) -> list[CandidateChunk]:
        """Retrieve cross-department candidate chunks from ChromaDB.

        Returns an empty list (rather than raising) if ChromaDB is unavailable.
        """
        if self.chroma_collection is None:
            logger.debug("No ChromaDB collection configured; skipping candidate retrieval")
            return []

        try:
            embedding_array = await self.embeddings.embed_query(query)
            query_vector: list[float] = embedding_array.tolist()

            results = self.chroma_collection.query(
                query_embeddings=[query_vector],
                n_results=min(self.retrieval_candidates, self.chroma_collection.count()),
                include=["documents", "metadatas"],
            )
            documents: list[str] = results.get("documents", [[]])[0] or []
            metadatas: list[dict] = results.get("metadatas", [[]])[0] or []
            ids: list[str] = results.get("ids", [[]])[0] or []

            chunks: list[CandidateChunk] = []
            for i, (text, meta) in enumerate(zip(documents, metadatas, strict=False)):
                dept = meta.get("department", "") if isinstance(meta, dict) else ""
                if text and dept:
                    chunks.append(
                        CandidateChunk(
                            text=text,
                            department=dept,
                            chunk_id=ids[i] if i < len(ids) else "",
                        )
                    )
            logger.debug("Fetched %d cross-department candidate chunks", len(chunks))
            return chunks

        except Exception as exc:  # noqa: BLE001
            logger.warning("ChromaDB candidate retrieval failed: %s", exc)
            return []

    async def _run_expansion_and_hyde(
        self,
        query: str,
        department: str,
        alternatives: list[str],
    ) -> tuple[QueryExpansionResult, HyDEResult]:
        """Run query expansion and HyDE concurrently.

        Each task has its own timeout and error handling.  A failure in one
        does not cancel the other.
        """
        expansion_coro = expand_query(
            self.llm,
            query,
            department,
            alternative_departments=alternatives or None,
            n=self.expansion_count,
        )

        if self.hyde_enabled:
            hyde_coro = generate_hyde(self.llm, self.embeddings, query, department)
        else:

            async def _skipped_hyde() -> HyDEResult:
                return HyDEResult(status=StageStatus.SKIPPED)

            hyde_coro = _skipped_hyde()

        expansion_result, hyde_result = await asyncio.gather(
            expansion_coro,
            hyde_coro,
            return_exceptions=False,  # individual functions already catch exceptions
        )
        return expansion_result, hyde_result
