"""LLM-assisted semantic document ingestion (structure -> metadata -> sections -> chunks)."""

from src.rag.semantic.chunks import CoverageError, SemanticChunk, build_chunks, contextualize
from src.rag.semantic.metadata import MetadataGenerator
from src.rag.semantic.segmentation import SegmentationResult, SemanticSegmenter

__all__ = [
    "CoverageError",
    "MetadataGenerator",
    "SegmentationResult",
    "SemanticChunk",
    "SemanticSegmenter",
    "build_chunks",
    "contextualize",
]
