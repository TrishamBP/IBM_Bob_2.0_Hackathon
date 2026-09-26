"""XGBoost-based department router for the RAG pipeline."""

from src.rag.router.router import DepartmentRouter, RouterCompatibilityError, RoutingThresholds

__all__ = ["DepartmentRouter", "RouterCompatibilityError", "RoutingThresholds"]
