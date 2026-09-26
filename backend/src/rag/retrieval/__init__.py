"""Hybrid retrieval for the chat pipeline: ChromaDB + BM25, RRF, evidence filter, MMR."""

from src.rag.retrieval.bm25 import BM25Index
from src.rag.retrieval.filtering import Candidate, EvidenceConfig, plan_departments
from src.rag.retrieval.hybrid import HybridRetriever, QueryVectors, RetrievalConfig, RetrievalResult

__all__ = [
    "BM25Index",
    "Candidate",
    "EvidenceConfig",
    "HybridRetriever",
    "QueryVectors",
    "RetrievalConfig",
    "RetrievalResult",
    "plan_departments",
]
