"""Department router: classifies a natural-language query into an ACME department.

Queries are embedded with Fireworks (Qwen3 Embedding 8B, 356 dimensions, L2-normalized)
and classified by a trained XGBoost model (see ``training_router.py``). Probabilities are
temperature-calibrated with a temperature fitted on the validation split during training.

This class only classifies. Retrieval-backed routing lives in ``fusion.py``.
"""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import numpy as np
from xgboost import XGBClassifier

from src.rag.departments import DEPARTMENTS
from src.rag.fireworks import FireworksEmbeddings

EMBEDDING_PROVIDER = "fireworks"

ROUTER_DIR = Path(__file__).resolve().parent
DEFAULT_MODEL_DIR = ROUTER_DIR / "models"
MODEL_FILENAME = "department_router.json"
LABEL_ENCODER_FILENAME = "label_encoder.joblib"
METADATA_FILENAME = "model_metadata.json"

__all__ = [
    "DEPARTMENTS",
    "DepartmentRouter",
    "RouterCompatibilityError",
    "RoutingThresholds",
    "apply_temperature",
]


class RouterCompatibilityError(RuntimeError):
    """Raised when saved router artifacts do not match each other or the embedding model."""


@dataclass(frozen=True)
class RoutingThresholds:
    """Confidence thresholds for routing decisions.

    The defaults are starting points, not calibrated values. Tune them against
    validation data (or production feedback) before relying on them.

    - ``min_confidence``: primary predictions below this are flagged ``low_confidence``.
    - ``candidate_min_confidence``: when low confidence, other departments at or above
      this probability are added to ``candidate_departments``.
    - ``max_candidates``: upper bound on ``candidate_departments`` length.
    """

    min_confidence: float = 0.5
    candidate_min_confidence: float = 0.15
    max_candidates: int = 3

    def __post_init__(self) -> None:
        for name in ("min_confidence", "candidate_min_confidence"):
            value = getattr(self, name)
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be between 0 and 1, got {value}")
        if self.max_candidates < 1:
            raise ValueError(f"max_candidates must be >= 1, got {self.max_candidates}")


def apply_temperature(probabilities: np.ndarray, temperature: float) -> np.ndarray:
    """Temperature-scale a probability matrix: softmax(log(p) / T)."""
    if temperature == 1.0:
        return probabilities
    logits = np.log(np.clip(probabilities, 1e-12, 1.0)) / temperature
    logits -= logits.max(axis=1, keepdims=True)
    exp = np.exp(logits)
    return exp / exp.sum(axis=1, keepdims=True)


class DepartmentRouter:
    """Routes queries to departments using a saved XGBoost model.

    Artifacts are loaded lazily (once, in a worker thread) on first use, or eagerly with
    :meth:`load`. The embedder must match the configuration recorded at training time.
    """

    def __init__(
        self,
        embedder: FireworksEmbeddings,
        model_dir: str | Path | None = None,
        thresholds: RoutingThresholds | None = None,
    ) -> None:
        self.embedder = embedder
        self.model_dir = Path(model_dir) if model_dir is not None else DEFAULT_MODEL_DIR
        self.thresholds = thresholds or RoutingThresholds()
        self.metadata: dict[str, Any] = {}
        self.departments: list[str] = []
        self.temperature = 1.0
        self._model: XGBClassifier | None = None
        self._iteration_range: tuple[int, int] | None = None
        self._load_lock = asyncio.Lock()

    @property
    def loaded(self) -> bool:
        return self._model is not None

    async def load(self) -> None:
        async with self._load_lock:
            if self._model is None:
                await asyncio.to_thread(self._load_sync)

    def _load_sync(self) -> None:
        model_path = self.model_dir / MODEL_FILENAME
        encoder_path = self.model_dir / LABEL_ENCODER_FILENAME
        metadata_path = self.model_dir / METADATA_FILENAME
        missing = [p.name for p in (model_path, encoder_path, metadata_path) if not p.exists()]
        if missing:
            raise FileNotFoundError(
                f"Missing router artifacts in {self.model_dir}: {', '.join(missing)}. "
                "Run `uv run python -m src.rag.router.training_router` first."
            )
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        label_encoder = joblib.load(encoder_path)
        model = XGBClassifier()
        model.load_model(model_path)
        departments = [str(label) for label in label_encoder.classes_]
        self._validate_compatibility(metadata, model, departments)

        best_iteration = metadata.get("best_iteration")
        self._iteration_range = (0, best_iteration + 1) if best_iteration is not None else None
        self.temperature = float(metadata.get("calibration", {}).get("temperature", 1.0))
        self.metadata, self.departments, self._model = metadata, departments, model

    def _validate_compatibility(
        self, metadata: dict[str, Any], model: XGBClassifier, departments: list[str]
    ) -> None:
        expected = {
            "embedding_provider": EMBEDDING_PROVIDER,
            "embedding_model_name": self.embedder.model,
            "embedding_dimensions": self.embedder.dimensions,
            "query_instruction": self.embedder.query_instruction,
        }
        for key, value in expected.items():
            if metadata.get(key) != value:
                raise RouterCompatibilityError(
                    f"Router was trained with {key}={metadata.get(key)!r}, but the configured "
                    f"embedder has {value!r}. Retrain or fix the embedding configuration."
                )
        model_dim = model.get_booster().num_features()
        if model_dim != self.embedder.dimensions:
            raise RouterCompatibilityError(
                f"XGBoost expects {model_dim} features, embedder produces "
                f"{self.embedder.dimensions}"
            )
        if departments != list(metadata.get("department_labels", [])):
            raise RouterCompatibilityError(
                "Label encoder classes do not match department_labels in metadata"
            )
        if set(departments) != set(DEPARTMENTS):
            raise RouterCompatibilityError("Model departments do not match DEPARTMENTS")
        n_classes = getattr(model, "n_classes_", None)
        if n_classes is not None and n_classes != len(departments):
            raise RouterCompatibilityError(
                f"XGBoost model has {n_classes} classes but label encoder has {len(departments)}"
            )

    async def route(self, query: str, top_k: int = 3) -> dict[str, Any]:
        """Return the primary department, confidence and the top-k predictions for a query."""
        return (await self._route_many([self._validate_query(query)], top_k))[0]

    async def predict_department(self, query: str) -> dict[str, Any]:
        """Return only the most likely department and its probability."""
        result = await self.route(query, top_k=1)
        return {
            "department": result["primary_department"],
            "confidence": result["confidence"],
            "low_confidence": result["low_confidence"],
        }

    async def predict_batch(self, queries: list[str], top_k: int = 3) -> list[dict[str, Any]]:
        """Route several queries with batched embedding and a single prediction pass."""
        if isinstance(queries, str):
            raise TypeError("predict_batch expects a list of strings, not a single string")
        if not queries:
            return []
        return await self._route_many([self._validate_query(q) for q in queries], top_k)

    async def predict_proba(self, queries: list[str]) -> np.ndarray:
        """Calibrated probability matrix, columns ordered as ``self.departments``."""
        embeddings = await self.embedder.embed_queries(queries)
        return await self.predict_proba_from_embeddings(embeddings)

    async def predict_proba_from_embeddings(
        self, embeddings: np.ndarray, *, calibrated: bool = True
    ) -> np.ndarray:
        """Predict from precomputed normalized query embeddings (e.g. shared with retrieval)."""
        await self.load()
        embeddings = np.atleast_2d(embeddings)
        if embeddings.shape[1] != self.embedder.dimensions:
            raise RouterCompatibilityError(
                f"Expected {self.embedder.dimensions}-d embeddings, got {embeddings.shape[1]}"
            )
        assert self._model is not None
        raw = await asyncio.to_thread(
            self._model.predict_proba, embeddings, iteration_range=self._iteration_range
        )
        return apply_temperature(raw, self.temperature) if calibrated else raw

    async def _route_many(self, queries: list[str], top_k: int) -> list[dict[str, Any]]:
        top_k = self._validate_top_k(top_k)
        probabilities = await self.predict_proba(queries)
        return [
            self._build_result(query, row, top_k)
            for query, row in zip(queries, probabilities, strict=True)
        ]

    def _build_result(self, query: str, probabilities: np.ndarray, top_k: int) -> dict[str, Any]:
        order = np.argsort(probabilities)[::-1]
        ranked = [
            {"department": self.departments[i], "confidence": round(float(probabilities[i]), 4)}
            for i in order
        ]
        primary = ranked[0]
        low_confidence = primary["confidence"] < self.thresholds.min_confidence

        if low_confidence:
            candidates = [primary["department"]] + [
                p["department"]
                for p in ranked[1:]
                if p["confidence"] >= self.thresholds.candidate_min_confidence
            ]
            candidates = candidates[: self.thresholds.max_candidates]
        else:
            candidates = [primary["department"]]

        return {
            "query": query,
            "primary_department": primary["department"],
            "confidence": primary["confidence"],
            "low_confidence": low_confidence,
            "candidate_departments": candidates,
            "predictions": ranked[:top_k],
        }

    @staticmethod
    def _validate_query(query: str) -> str:
        if not isinstance(query, str):
            raise TypeError(f"query must be a string, got {type(query).__name__}")
        query = query.strip()
        if not query:
            raise ValueError("query must not be empty")
        return query

    @staticmethod
    def _validate_top_k(top_k: int) -> int:
        if isinstance(top_k, bool) or not isinstance(top_k, int):
            raise TypeError(f"top_k must be an integer, got {type(top_k).__name__}")
        if top_k < 1:
            raise ValueError(f"top_k must be >= 1, got {top_k}")
        return min(top_k, len(DEPARTMENTS))
