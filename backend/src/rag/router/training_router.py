"""Train the XGBoost department router.

Run from the backend directory:

    uv run python -m src.rag.router.training_router --estimate-only  # API usage estimate
    uv run python -m src.rag.router.training_router                  # train + promote
    uv run python -m src.rag.router.training_router --show           # also open the plots

Pipeline: validate dataset.json -> embed queries with Fireworks (Qwen3 Embedding 8B,
356-d, L2-normalized, Qwen3 query instruction; cached on disk) -> group-aware 70/15/15
split on ``source_group`` (same seed and algorithm as v1, so the same split) -> XGBoost
with early stopping on validation mlogloss (merror and macro F1 monitored) ->
temperature calibration on validation -> evaluate once on the held-out test set.

Artifacts are written to staging directories first. Only after training, evaluation and
a reload check succeed is the previous active model archived under ``archive/v<version>``
and the new one promoted.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import re
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import joblib
import matplotlib
import numpy as np
import pandas as pd
import sklearn
import xgboost as xgb
from scipy.optimize import minimize_scalar
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    log_loss,
    precision_recall_fscore_support,
    top_k_accuracy_score,
)
from sklearn.preprocessing import LabelEncoder

from src.config import get_settings
from src.rag.embeddings import build_embedder, build_fireworks_client
from src.rag.fireworks import FireworksEmbeddings
from src.rag.router.router import (
    DEFAULT_MODEL_DIR,
    DEPARTMENTS,
    EMBEDDING_PROVIDER,
    LABEL_ENCODER_FILENAME,
    METADATA_FILENAME,
    MODEL_FILENAME,
    ROUTER_DIR,
    DepartmentRouter,
    apply_temperature,
)

MODEL_VERSION = "2.0.0"
RANDOM_STATE = 42
DATASET_PATH = ROUTER_DIR / "dataset.json"
EVALUATION_DIR = ROUTER_DIR / "evaluation"
CACHE_DIR = ROUTER_DIR / ".cache"
# Fireworks serverless price for qwen3-embedding-8b (USD per 1M input tokens) at the time
# of writing; used only for the pre-run estimate.
EMBEDDING_PRICE_PER_MTOK = 0.10

SPLIT_RATIOS = {"train": 0.70, "validation": 0.15, "test": 0.15}
REQUIRED_FIELDS = ("id", "query", "department", "difficulty", "topic", "source_group")
DIFFICULTIES = {"easy", "medium", "hard"}
# Cosine similarity above which two queries from *different* source groups are reported
# as near-duplicates (possible train/test leakage).
NEAR_DUPLICATE_THRESHOLD = 0.95
CHECKPOINT_EVERY = 25

# early_stopping_rounds uses the *last* metric in eval_metric, so mlogloss is listed last
# to early-stop on the smoother log loss rather than on the step-wise error rate.
INITIAL_XGB_PARAMS: dict[str, Any] = {
    "objective": "multi:softprob",
    "n_estimators": 500,
    "max_depth": 5,
    "learning_rate": 0.05,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "eval_metric": ["merror", "mlogloss"],
    "random_state": RANDOM_STATE,
    "n_jobs": -1,
    "tree_method": "hist",
    "early_stopping_rounds": 30,
}

# Tuned on the validation split only (grid over max_depth, colsample_bytree,
# min_child_weight, reg_lambda; selected by validation mlogloss). The initial config hit
# train accuracy ~1.0 within 25 rounds and never early-stopped at 500 rounds; shallower
# trees, fewer features per tree and stronger L2 reduce that overfitting.
XGB_PARAMS: dict[str, Any] = {
    "objective": "multi:softprob",
    "n_estimators": 1500,
    "max_depth": 3,
    "learning_rate": 0.1,
    "subsample": 0.8,
    "colsample_bytree": 0.4,
    "min_child_weight": 1,
    "reg_lambda": 5.0,
    "eval_metric": ["merror", "mlogloss"],
    "random_state": RANDOM_STATE,
    "n_jobs": -1,
    "tree_method": "hist",
    "early_stopping_rounds": 50,
}


def log(message: str = "") -> None:
    print(message, flush=True)


def section(title: str) -> None:
    log()
    log(f"=== {title} " + "=" * max(0, 70 - len(title)))


# ---------------------------------------------------------------------------
# Dataset loading and validation
# ---------------------------------------------------------------------------


def normalize_text(text: str) -> str:
    return re.sub(r"[^a-z0-9 ]", "", re.sub(r"\s+", " ", text.lower())).strip()


def load_dataset(path: Path) -> pd.DataFrame:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("queries"), list):
        raise ValueError("dataset.json must be an object with a 'queries' list")

    errors: list[str] = []
    for i, item in enumerate(data["queries"]):
        missing = [f for f in REQUIRED_FIELDS if not isinstance(item.get(f), str) or not item[f]]
        if missing:
            errors.append(f"entry {i}: missing/empty fields {missing}")
            continue
        if item["department"] not in DEPARTMENTS:
            errors.append(f"{item['id']}: unknown department {item['department']!r}")
        if item["difficulty"] not in DIFFICULTIES:
            errors.append(f"{item['id']}: invalid difficulty {item['difficulty']!r}")
    if errors:
        raise ValueError("Invalid dataset entries:\n  " + "\n  ".join(errors[:20]))

    df = pd.DataFrame(data["queries"], columns=list(REQUIRED_FIELDS))
    duplicate_ids = df["id"][df["id"].duplicated()].tolist()
    if duplicate_ids:
        raise ValueError(f"Duplicate ids: {duplicate_ids[:10]}")

    groups_per_department = df.groupby("source_group")["department"].nunique()
    mixed = groups_per_department[groups_per_department > 1].index.tolist()
    if mixed:
        raise ValueError(f"source_groups spanning several departments: {mixed[:10]}")

    log(
        f"Loaded {len(df)} queries from {path.name} "
        f"(dataset={data.get('dataset_name')!r}, version={data.get('version')!r})"
    )
    return df


def check_departments(df: pd.DataFrame) -> dict[str, int]:
    counts = df["department"].value_counts()
    absent = [d for d in DEPARTMENTS if d not in counts]
    if absent:
        raise ValueError(f"Departments with no queries: {absent}")

    distribution = {d: int(counts[d]) for d in DEPARTMENTS}
    groups = df.groupby("department")["source_group"].nunique()
    log(f"{'Department':<28}{'Queries':>8}{'Groups':>8}")
    for department, n in distribution.items():
        log(f"{department:<28}{n:>8}{groups[department]:>8}")

    ratio = max(distribution.values()) / min(distribution.values())
    log(f"Imbalance ratio (max/min): {ratio:.2f}")
    if ratio > 1.5:
        log("WARNING: class distribution is noticeably imbalanced.")
    return distribution


def check_exact_duplicates(df: pd.DataFrame) -> None:
    normalized = df["query"].map(normalize_text)
    duplicated = df[normalized.duplicated(keep=False)]
    if not duplicated.empty:
        raise ValueError(
            "Exact duplicate queries (after normalization):\n"
            + duplicated.sort_values("query")[["id", "query"]].to_string(index=False)
        )
    log("Exact duplicates: none")


def find_near_duplicates(df: pd.DataFrame, embeddings: np.ndarray) -> list[dict[str, Any]]:
    """Pairs of queries from different source groups whose embeddings are nearly identical."""
    similarity = embeddings @ embeddings.T
    np.fill_diagonal(similarity, 0.0)
    groups = df["source_group"].to_numpy()
    rows, cols = np.where(np.triu(similarity, k=1) >= NEAR_DUPLICATE_THRESHOLD)
    pairs = [
        {
            "a": df["query"].iat[i],
            "b": df["query"].iat[j],
            "group_a": groups[i],
            "group_b": groups[j],
            "similarity": round(float(similarity[i, j]), 4),
        }
        for i, j in zip(rows, cols, strict=True)
        if groups[i] != groups[j]
    ]
    log(f"Cross-group near-duplicates (cosine >= {NEAR_DUPLICATE_THRESHOLD}): {len(pairs)}")
    for pair in pairs[:10]:
        log(f"  {pair['similarity']:.3f}  {pair['a']!r} <-> {pair['b']!r}")
    return pairs


# ---------------------------------------------------------------------------
# Embeddings and splitting
# ---------------------------------------------------------------------------


def estimate_usage(embedder: FireworksEmbeddings, queries: list[str]) -> dict[str, Any]:
    """Rough token estimate (~4 characters per token, plus instruction prefix)."""
    chars = sum(len(embedder.format_query(q)) for q in queries)
    tokens = int(chars / 4)
    return {
        "queries": len(queries),
        "requests": -(-len(queries) // embedder.batch_size),
        "estimated_tokens": tokens,
        "estimated_cost_usd": round(tokens / 1e6 * EMBEDDING_PRICE_PER_MTOK, 5),
    }


def embedding_cache_path(embedder: FireworksEmbeddings, queries: list[str]) -> Path:
    key = json.dumps(
        [embedder.model, embedder.dimensions, embedder.query_instruction, queries]
    ).encode("utf-8")
    return CACHE_DIR / f"embeddings_{hashlib.sha256(key).hexdigest()[:20]}.npy"


async def embed_queries(
    embedder: FireworksEmbeddings, queries: list[str], *, use_cache: bool = True
) -> np.ndarray:
    cache_path = embedding_cache_path(embedder, queries)
    if use_cache and cache_path.exists():
        embeddings = np.load(cache_path)
        log(f"Loaded cached embeddings from {cache_path}")
    else:
        started = datetime.now(UTC)
        embeddings = await embedder.embed_queries(queries)
        seconds = (datetime.now(UTC) - started).total_seconds()
        log(f"Embedded {len(queries)} queries via Fireworks in {seconds:.1f}s")
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        np.save(cache_path, embeddings)
    if embeddings.shape != (len(queries), embedder.dimensions):
        raise RuntimeError(
            f"Expected ({len(queries)}, {embedder.dimensions}) embeddings, got {embeddings.shape}"
        )
    norms = np.linalg.norm(embeddings, axis=1)
    if not np.allclose(norms, 1.0, atol=1e-3):
        raise RuntimeError("Embeddings are not L2-normalized")
    log(f"Embeddings: shape={embeddings.shape}, mean L2 norm={norms.mean():.4f}")
    return embeddings


def group_split(df: pd.DataFrame, seed: int) -> dict[str, np.ndarray]:
    """Assign whole source_groups to splits, per department, to approximate SPLIT_RATIOS.

    Splitting within each department guarantees every department appears in every split;
    keeping groups intact keeps paraphrases of one question out of multiple splits.
    """
    rng = np.random.default_rng(seed)
    assignment: dict[str, str] = {}

    for department in DEPARTMENTS:
        sizes = df[df["department"] == department].groupby("source_group").size()
        groups = sizes.index.to_numpy()
        rng.shuffle(groups)
        if len(groups) < len(SPLIT_RATIOS):
            raise ValueError(f"{department} needs at least {len(SPLIT_RATIOS)} source groups")

        total = int(sizes.sum())
        filled = dict.fromkeys(SPLIT_RATIOS, 0)
        # Seed each split with one group, then give each next group to the split
        # furthest below its target share.
        for split, group in zip(SPLIT_RATIOS, groups, strict=False):
            assignment[group] = split
            filled[split] += int(sizes[group])
        for group in groups[len(SPLIT_RATIOS) :]:
            split = max(SPLIT_RATIOS, key=lambda s: SPLIT_RATIOS[s] * total - filled[s])
            assignment[group] = split
            filled[split] += int(sizes[group])

    split_labels = df["source_group"].map(assignment).to_numpy()
    indices = {split: np.flatnonzero(split_labels == split) for split in SPLIT_RATIOS}

    for split, idx in indices.items():
        present = set(df["department"].iloc[idx])
        if len(present) != len(DEPARTMENTS):
            missing = set(DEPARTMENTS) - present
            raise RuntimeError(f"{split} split is missing departments: {missing}")
    split_groups = {split: set(df["source_group"].iloc[idx]) for split, idx in indices.items()}
    overlap = {
        (a, b)
        for a in SPLIT_RATIOS
        for b in SPLIT_RATIOS
        if a < b and split_groups[a] & split_groups[b]
    }
    if overlap:
        raise RuntimeError(f"source_group leakage between splits: {overlap}")

    for split, idx in indices.items():
        log(
            f"{split:<11} {len(idx):>5} queries ({len(idx) / len(df):.1%}), "
            f"{df['source_group'].iloc[idx].nunique()} groups"
        )
    return indices


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------


class ProgressCallback(xgb.callback.TrainingCallback):
    """Prints train/validation loss, accuracy and validation macro F1 every ``every`` rounds."""

    def __init__(self, every: int, x_val: np.ndarray, y_val: np.ndarray) -> None:
        super().__init__()
        self.every = every
        self.x_val = x_val
        self.y_val = y_val
        self.checkpoints: list[dict[str, float]] = []

    def after_iteration(self, model: Any, epoch: int, evals_log: dict) -> bool:
        if epoch % self.every == 0:
            self._record(model, epoch, evals_log)
        return False

    def after_training(self, model: Any) -> Any:
        return model

    def _record(self, booster: Any, epoch: int, evals_log: dict) -> None:
        train, val = evals_log["validation_0"], evals_log["validation_1"]
        probabilities = booster.inplace_predict(self.x_val, iteration_range=(0, epoch + 1))
        val_macro_f1 = f1_score(
            self.y_val, np.asarray(probabilities).argmax(axis=1), average="macro", zero_division=0
        )
        checkpoint = {
            "iteration": epoch,
            "train_mlogloss": float(train["mlogloss"][-1]),
            "val_mlogloss": float(val["mlogloss"][-1]),
            "train_accuracy": 1.0 - float(train["merror"][-1]),
            "val_accuracy": 1.0 - float(val["merror"][-1]),
            "val_macro_f1": float(val_macro_f1),
        }
        self.checkpoints.append(checkpoint)
        if not self.checkpoints[:-1]:
            log(
                f"{'iter':>6}{'train_loss':>12}{'val_loss':>10}{'train_acc':>11}"
                f"{'val_acc':>9}{'val_macroF1':>13}"
            )
        log(
            f"{epoch:>6}{checkpoint['train_mlogloss']:>12.4f}{checkpoint['val_mlogloss']:>10.4f}"
            f"{checkpoint['train_accuracy']:>11.3f}{checkpoint['val_accuracy']:>9.3f}"
            f"{checkpoint['val_macro_f1']:>13.3f}"
        )


def train_model(
    x_train: np.ndarray, y_train: np.ndarray, x_val: np.ndarray, y_val: np.ndarray
) -> tuple[xgb.XGBClassifier, ProgressCallback]:
    progress = ProgressCallback(CHECKPOINT_EVERY, x_val, y_val)
    model = xgb.XGBClassifier(**XGB_PARAMS, callbacks=[progress])
    model.fit(x_train, y_train, eval_set=[(x_train, y_train), (x_val, y_val)], verbose=False)
    return model, progress


def summarize_history(model: xgb.XGBClassifier) -> dict[str, Any]:
    history = model.evals_result()
    train, val = history["validation_0"], history["validation_1"]
    best = int(model.best_iteration)
    n_rounds = len(val["mlogloss"])
    val_loss = np.asarray(val["mlogloss"])
    train_acc = 1.0 - np.asarray(train["merror"])
    val_acc = 1.0 - np.asarray(val["merror"])

    at_best = {
        "train_mlogloss": float(train["mlogloss"][best]),
        "val_mlogloss": float(val_loss[best]),
        "train_merror": float(train["merror"][best]),
        "val_merror": float(val["merror"][best]),
        "train_accuracy": float(train_acc[best]),
        "val_accuracy": float(val_acc[best]),
    }
    accuracy_gap = at_best["train_accuracy"] - at_best["val_accuracy"]
    loss_ratio = at_best["val_mlogloss"] / max(at_best["train_mlogloss"], 1e-9)

    notes = []
    if at_best["train_accuracy"] < 0.85:
        notes.append(
            f"Training accuracy at the best iteration is only {at_best['train_accuracy']:.3f}: "
            "the model is underfitting (more rounds, deeper trees or a higher learning rate "
            "may help)."
        )
    if accuracy_gap > 0.10 or loss_ratio > 3.0:
        notes.append(
            f"Train/validation gap at the best iteration: accuracy {accuracy_gap:+.3f}, "
            f"log loss x{loss_ratio:.1f}. Trees memorise the training embeddings faster than "
            "they generalise to unseen question families - classic overfitting, bounded "
            "by early stopping."
        )
    if not notes:
        notes.append("No strong sign of over- or underfitting at the selected iteration.")
    if n_rounds > best + 1:
        notes.append(
            f"Validation log loss did not improve for {n_rounds - best - 1} rounds after "
            f"iteration {best} (val loss at stop: {val_loss[-1]:.4f} vs best "
            f"{val_loss[best]:.4f}); "
            "early stopping kept the best iteration."
        )
    else:
        notes.append(
            f"Early stopping did not trigger: validation log loss was still improving at the "
            f"n_estimators cap ({n_rounds}). More rounds or a higher learning rate may help."
        )
    non_monotonic = int(np.sum(np.diff(val_acc[: best + 1]) < 0))
    notes.append(
        f"Validation accuracy decreased on {non_monotonic} of {best} steps up to the best "
        "iteration: accuracy is a step function of argmax changes and need not rise "
        "monotonically even while log loss falls."
    )

    return {
        "best_iteration": best,
        "best_validation_mlogloss": float(model.best_score),
        "rounds_trained": n_rounds,
        "at_best_iteration": at_best,
        "final_round": {
            "train_mlogloss": float(train["mlogloss"][-1]),
            "val_mlogloss": float(val_loss[-1]),
            "train_accuracy": float(train_acc[-1]),
            "val_accuracy": float(val_acc[-1]),
        },
        "diagnosis": notes,
        "history": {
            "train_mlogloss": [float(v) for v in train["mlogloss"]],
            "val_mlogloss": [float(v) for v in val_loss],
            "train_merror": [float(v) for v in train["merror"]],
            "val_merror": [float(v) for v in val["merror"]],
        },
    }


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------


def evaluate(
    model: xgb.XGBClassifier, x: np.ndarray, y: np.ndarray, labels: list[str]
) -> dict[str, Any]:
    iteration_range = (0, int(model.best_iteration) + 1)
    probabilities = model.predict_proba(x, iteration_range=iteration_range)
    predictions = probabilities.argmax(axis=1)
    class_ids = np.arange(len(labels))

    precision, recall, f1, support = precision_recall_fscore_support(
        y, predictions, labels=class_ids, zero_division=0
    )
    macro_p, macro_r, macro_f1, _ = precision_recall_fscore_support(
        y, predictions, labels=class_ids, average="macro", zero_division=0
    )
    matrix = confusion_matrix(y, predictions, labels=class_ids)

    confusions = [
        {
            "true": labels[i],
            "predicted": labels[j],
            "count": int(matrix[i, j]),
            "share_of_true_class": round(float(matrix[i, j] / matrix[i].sum()), 4),
        }
        for i in class_ids
        for j in class_ids
        if i != j and matrix[i, j] > 0
    ]
    confusions.sort(key=lambda c: c["count"], reverse=True)

    return {
        "n_samples": int(len(y)),
        "accuracy": float(accuracy_score(y, predictions)),
        "top3_accuracy": float(top_k_accuracy_score(y, probabilities, k=3, labels=class_ids)),
        "macro_precision": float(macro_p),
        "macro_recall": float(macro_r),
        "macro_f1": float(macro_f1),
        "weighted_f1": float(f1_score(y, predictions, average="weighted", zero_division=0)),
        "mean_confidence": float(probabilities.max(axis=1).mean()),
        "per_department": {
            labels[i]: {
                "precision": float(precision[i]),
                "recall": float(recall[i]),
                "f1": float(f1[i]),
                "support": int(support[i]),
            }
            for i in class_ids
        },
        "confusion_matrix": matrix.tolist(),
        "top_confusions": confusions[:15],
        "_predictions": predictions,
        "_probabilities": probabilities,
    }


def public(metrics: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in metrics.items() if not k.startswith("_")}


def headline(metrics: dict[str, Any]) -> dict[str, float]:
    keys = (
        "accuracy",
        "top3_accuracy",
        "macro_precision",
        "macro_recall",
        "macro_f1",
        "weighted_f1",
        "mean_confidence",
    )
    return {k: round(metrics[k], 4) for k in keys}


def print_metrics(name: str, metrics: dict[str, Any]) -> None:
    log(f"{name}: " + ", ".join(f"{k}={v:.4f}" for k, v in headline(metrics).items()))


# ---------------------------------------------------------------------------
# Plots and reports
# ---------------------------------------------------------------------------


def plot_training_history(
    summary: dict[str, Any], checkpoints: list[dict[str, float]], path: Path
) -> None:
    import matplotlib.pyplot as plt

    history = summary["history"]
    rounds = np.arange(len(history["train_mlogloss"]))
    best = summary["best_iteration"]

    fig, (ax_loss, ax_acc, ax_f1) = plt.subplots(1, 3, figsize=(20, 5))
    ax_f1.plot(
        [c["iteration"] for c in checkpoints],
        [c["val_macro_f1"] for c in checkpoints],
        marker="o",
        markersize=3,
        color="tab:green",
        label="Validation macro F1",
    )
    ax_f1.set(
        title=f"Validation macro F1 (every {CHECKPOINT_EVERY} rounds)",
        xlabel="Boosting iteration",
        ylabel="macro F1",
        ylim=(0, 1.02),
    )
    ax_loss.plot(rounds, history["train_mlogloss"], label="Train log loss")
    ax_loss.plot(rounds, history["val_mlogloss"], label="Validation log loss")
    ax_loss.set(title="Multiclass log loss", xlabel="Boosting iteration", ylabel="mlogloss")

    ax_acc.plot(rounds, 1 - np.asarray(history["train_merror"]), label="Train accuracy")
    ax_acc.plot(rounds, 1 - np.asarray(history["val_merror"]), label="Validation accuracy")
    ax_acc.set(
        title="Accuracy (1 - merror)",
        xlabel="Boosting iteration",
        ylabel="accuracy",
        ylim=(0, 1.02),
    )

    for ax in (ax_loss, ax_acc, ax_f1):
        ax.axvline(best, color="grey", linestyle="--", label=f"Best iteration ({best})")
        ax.grid(alpha=0.3)
        ax.legend()
    fig.suptitle("XGBoost department router - training history")
    fig.tight_layout()
    fig.savefig(path, dpi=150)


def plot_confusion_matrix(metrics: dict[str, Any], labels: list[str], path: Path) -> None:
    import matplotlib.pyplot as plt

    matrix = np.asarray(metrics["confusion_matrix"])
    normalized = matrix / matrix.sum(axis=1, keepdims=True).clip(min=1)

    fig, ax = plt.subplots(figsize=(12, 10))
    image = ax.imshow(normalized, cmap="Blues", vmin=0, vmax=1)
    fig.colorbar(image, ax=ax, label="Share of true department")
    ax.set_xticks(range(len(labels)), labels, rotation=45, ha="right")
    ax.set_yticks(range(len(labels)), labels)
    for i in range(len(labels)):
        for j in range(len(labels)):
            if matrix[i, j]:
                color = "white" if normalized[i, j] > 0.5 else "black"
                ax.text(j, i, matrix[i, j], ha="center", va="center", color=color, fontsize=8)
    ax.set(
        xlabel="Predicted department",
        ylabel="True department",
        title=f"Test confusion matrix (accuracy {metrics['accuracy']:.3f}, "
        f"n={metrics['n_samples']})",
    )
    fig.tight_layout()
    fig.savefig(path, dpi=150)


def plot_per_department(metrics: dict[str, Any], labels: list[str], path: Path) -> None:
    import matplotlib.pyplot as plt

    per = metrics["per_department"]
    y = np.arange(len(labels))
    height = 0.27
    fig, ax = plt.subplots(figsize=(11, 8))
    for offset, key in zip((-height, 0, height), ("precision", "recall", "f1"), strict=True):
        ax.barh(y + offset, [per[d][key] for d in labels], height, label=key)
    ax.set_yticks(y, labels)
    ax.invert_yaxis()
    ax.set(xlim=(0, 1), xlabel="score", title="Test metrics per department")
    ax.axvline(
        metrics["macro_f1"],
        color="grey",
        linestyle="--",
        label=f"macro F1 ({metrics['macro_f1']:.3f})",
    )
    ax.grid(axis="x", alpha=0.3)
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(path, dpi=150)


def plot_split_distribution(df: pd.DataFrame, indices: dict[str, np.ndarray], path: Path) -> None:
    counts = pd.DataFrame(
        {split: df["department"].iloc[idx].value_counts() for split, idx in indices.items()}
    ).reindex(list(DEPARTMENTS))
    ax = counts.plot.barh(stacked=True, figsize=(11, 7))
    ax.invert_yaxis()
    ax.set(xlabel="queries", title="Dataset distribution by department and split")
    ax.grid(axis="x", alpha=0.3)
    ax.figure.tight_layout()
    ax.figure.savefig(path, dpi=150)


def write_classification_report(
    y_test: np.ndarray,
    test_metrics: dict[str, Any],
    val_metrics: dict[str, Any],
    summary: dict[str, Any],
    labels: list[str],
    path: Path,
    embedding_label: str,
) -> None:
    report = classification_report(
        y_test,
        test_metrics["_predictions"],
        labels=np.arange(len(labels)),
        target_names=labels,
        digits=4,
        zero_division=0,
    )
    lines = [
        "ACME department router - held-out test set evaluation",
        f"Generated: {datetime.now(UTC).isoformat(timespec='seconds')}",
        f"Embedding model: {embedding_label}",
        f"Best iteration: {summary['best_iteration']} "
        f"(validation mlogloss {summary['best_validation_mlogloss']:.4f})",
        "",
        "Validation: " + ", ".join(f"{k}={v}" for k, v in headline(val_metrics).items()),
        "Test:       " + ", ".join(f"{k}={v}" for k, v in headline(test_metrics).items()),
        "",
        report,
        "Most frequent confusions (true -> predicted):",
    ]
    lines += [
        f"  {c['count']:>3}  ({c['share_of_true_class']:.1%} of true)  "
        f"{c['true']} -> {c['predicted']}"
        for c in test_metrics["top_confusions"]
    ] or ["  none"]
    lines += ["", "Training diagnosis:"] + [f"  - {note}" for note in summary["diagnosis"]]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def error_examples(
    df: pd.DataFrame, idx: np.ndarray, y: np.ndarray, metrics: dict[str, Any], labels: list[str]
) -> list[dict[str, Any]]:
    predictions, probabilities = metrics["_predictions"], metrics["_probabilities"]
    wrong = np.flatnonzero(predictions != y)
    return [
        {
            "id": df["id"].iat[idx[i]],
            "query": df["query"].iat[idx[i]],
            "true": labels[y[i]],
            "predicted": labels[predictions[i]],
            "confidence": round(float(probabilities[i].max()), 4),
        }
        for i in wrong
    ]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def expected_calibration_error(probabilities: np.ndarray, y: np.ndarray, bins: int = 10) -> float:
    confidence = probabilities.max(axis=1)
    correct = probabilities.argmax(axis=1) == y
    edges = np.linspace(0.0, 1.0, bins + 1)
    ece = 0.0
    for low, high in zip(edges[:-1], edges[1:], strict=True):
        mask = (confidence > low) & (confidence <= high)
        if mask.any():
            ece += mask.mean() * abs(correct[mask].mean() - confidence[mask].mean())
    return float(ece)


def fit_temperature(probabilities: np.ndarray, y: np.ndarray, n_classes: int) -> float:
    """Temperature minimizing validation log loss (argmax, and so accuracy, is unchanged)."""
    labels = np.arange(n_classes)

    def nll(t: float) -> float:
        return float(log_loss(y, apply_temperature(probabilities, t), labels=labels))

    return float(minimize_scalar(nll, bounds=(0.05, 10.0), method="bounded").x)


def calibration_report(
    probabilities: np.ndarray, y: np.ndarray, temperature: float, n_classes: int
) -> dict[str, float]:
    labels = np.arange(n_classes)
    calibrated = apply_temperature(probabilities, temperature)
    return {
        "nll_before": float(log_loss(y, probabilities, labels=labels)),
        "nll_after": float(log_loss(y, calibrated, labels=labels)),
        "ece_before": expected_calibration_error(probabilities, y),
        "ece_after": expected_calibration_error(calibrated, y),
        "mean_confidence_before": float(probabilities.max(axis=1).mean()),
        "mean_confidence_after": float(calibrated.max(axis=1).mean()),
    }


def _move_files(src: Path, dst: Path) -> list[Path]:
    """Move the regular files (not subdirectories) of ``src`` into ``dst``."""
    dst.mkdir(parents=True, exist_ok=True)
    moved = []
    for path in sorted(src.iterdir()):
        if path.is_file():
            target = dst / path.name
            if target.exists():
                target.unlink()
            shutil.move(str(path), target)
            moved.append(target)
    return moved


def promote(staging_model: Path, staging_eval: Path, model_dir: Path, eval_dir: Path) -> str | None:
    """Archive the current active model + evaluation, then move staged artifacts in."""
    archived = None
    current = model_dir / METADATA_FILENAME
    if current.exists():
        version = json.loads(current.read_text(encoding="utf-8")).get("model_version", "unknown")
        name = f"v{version}"
        if (model_dir / "archive" / name).exists():
            name = f"{name}-{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}"
        _move_files(model_dir, model_dir / "archive" / name)
        _move_files(eval_dir, eval_dir / "archive" / name)
        archived = name
    _move_files(staging_model, model_dir)
    _move_files(staging_eval, eval_dir)
    staging_model.rmdir()
    staging_eval.rmdir()
    return archived


def load_previous_metadata(model_dir: Path) -> dict[str, Any] | None:
    path = model_dir / METADATA_FILENAME
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


async def run(args: argparse.Namespace) -> int:
    if not args.show:
        matplotlib.use("Agg")
    settings = get_settings()

    section("1. Load and validate dataset")
    df = load_dataset(args.dataset)
    check_exact_duplicates(df)
    queries = df["query"].tolist()

    section("2. Department distribution")
    distribution = check_departments(df)

    section("3. Encode labels")
    label_encoder = LabelEncoder().fit(list(DEPARTMENTS))
    labels = [str(c) for c in label_encoder.classes_]
    y = label_encoder.transform(df["department"])
    log(f"{len(labels)} classes: " + ", ".join(f"{i}={name}" for i, name in enumerate(labels)))

    async with build_fireworks_client(settings) as client:
        embedder = build_embedder(settings, client)
        embedding_label = f"{embedder.model} ({embedder.dimensions}d, Fireworks)"

        section(f"4. Query embeddings: {embedding_label}")
        usage = estimate_usage(embedder, queries)
        cached = embedding_cache_path(embedder, queries).exists() and not args.no_cache
        log(
            f"API usage estimate: {usage['queries']} queries in {usage['requests']} requests, "
            f"~{usage['estimated_tokens']:,} tokens, ~${usage['estimated_cost_usd']:.4f} "
            f"at ${EMBEDDING_PRICE_PER_MTOK}/1M tokens"
            + (" (cache hit: no API calls needed)" if cached else "")
        )
        if args.estimate_only:
            return 0
        embeddings = await embed_queries(embedder, queries, use_cache=not args.no_cache)
        near_duplicates = find_near_duplicates(df, embeddings)

        section("5. Group-aware train / validation / test split")
        indices = group_split(df, args.seed)
        previous = load_previous_metadata(args.model_dir)
        split_sizes = {split: int(len(idx)) for split, idx in indices.items()}
        if previous and previous.get("split_seed") == args.seed:
            same = previous.get("split_sizes") == split_sizes
            log(
                f"Split vs previous model v{previous.get('model_version')}: "
                + (
                    "identical sizes (same seed, same deterministic algorithm)"
                    if same
                    else f"DIFFERENT sizes {previous.get('split_sizes')}"
                )
            )
        x_train, y_train = embeddings[indices["train"]], y[indices["train"]]
        x_val, y_val = embeddings[indices["validation"]], y[indices["validation"]]
        x_test, y_test = embeddings[indices["test"]], y[indices["test"]]

        section("6. Train XGBoost (early stopping on validation mlogloss)")
        log(f"xgboost {xgb.__version__}, params: {XGB_PARAMS}")
        model, progress = await asyncio.to_thread(train_model, x_train, y_train, x_val, y_val)
        summary = summarize_history(model)
        log(
            f"Best iteration: {summary['best_iteration']} of {summary['rounds_trained']} "
            f"trained, best validation mlogloss: {summary['best_validation_mlogloss']:.4f}"
        )
        at_best = summary["at_best_iteration"]
        log(
            f"At best iteration: train acc={at_best['train_accuracy']:.4f}, "
            f"val acc={at_best['val_accuracy']:.4f}, train loss={at_best['train_mlogloss']:.4f}, "
            f"val loss={at_best['val_mlogloss']:.4f}"
        )
        best_f1 = max(progress.checkpoints, key=lambda c: c["val_macro_f1"])
        log(
            f"Best checkpoint validation macro F1: {best_f1['val_macro_f1']:.4f} "
            f"at iteration {best_f1['iteration']}"
        )
        for note in summary["diagnosis"]:
            log(f"  - {note}")

        section("7. Evaluate (validation for reference, test held out until now)")
        val_metrics = evaluate(model, x_val, y_val, labels)
        test_metrics = evaluate(model, x_test, y_test, labels)
        print_metrics("Validation", val_metrics)
        print_metrics("Test      ", test_metrics)
        log(f"{'Department':<28}{'precision':>10}{'recall':>8}{'f1':>8}{'n':>5}")
        for department, m in test_metrics["per_department"].items():
            log(
                f"{department:<28}{m['precision']:>10.3f}{m['recall']:>8.3f}{m['f1']:>8.3f}"
                f"{m['support']:>5}"
            )
        log("Most frequent test confusions:")
        for c in test_metrics["top_confusions"][:8]:
            log(f"  {c['count']:>3}  {c['true']} -> {c['predicted']}")

        section("8. Temperature calibration (fitted on validation)")
        temperature = fit_temperature(val_metrics["_probabilities"], y_val, len(labels))
        calibration = {
            "method": "temperature_scaling",
            "fitted_on": "validation",
            "temperature": temperature,
            "validation": calibration_report(
                val_metrics["_probabilities"], y_val, temperature, len(labels)
            ),
            "test": calibration_report(
                test_metrics["_probabilities"], y_test, temperature, len(labels)
            ),
        }
        log(f"Temperature: {temperature:.4f}")
        for split in ("validation", "test"):
            c = calibration[split]
            log(
                f"  {split:<10} NLL {c['nll_before']:.4f} -> {c['nll_after']:.4f}, "
                f"ECE {c['ece_before']:.4f} -> {c['ece_after']:.4f}, mean confidence "
                f"{c['mean_confidence_before']:.3f} -> {c['mean_confidence_after']:.3f}"
            )

        if previous:
            log()
            log(
                f"Comparison with active model v{previous.get('model_version')} "
                f"({previous.get('embedding_model_name')}), same test split:"
            )
            new = headline(test_metrics)
            for key, old_value in previous.get("test_metrics", {}).items():
                if key in new:
                    log(
                        f"  {key:<16} {old_value:.4f} -> {new[key]:.4f} "
                        f"({new[key] - old_value:+.4f})"
                    )

        section("9. Save artifacts to staging")
        staging_model = args.model_dir / ".staging"
        staging_eval = args.evaluation_dir / ".staging"
        for staging in (staging_model, staging_eval):
            shutil.rmtree(staging, ignore_errors=True)
            staging.mkdir(parents=True)

        model.save_model(staging_model / MODEL_FILENAME)
        joblib.dump(label_encoder, staging_model / LABEL_ENCODER_FILENAME)
        metadata = {
            "model_version": MODEL_VERSION,
            "training_date": datetime.now(UTC).isoformat(timespec="seconds"),
            "embedding_provider": EMBEDDING_PROVIDER,
            "embedding_model_name": embedder.model,
            "embedding_dimensions": embedder.dimensions,
            "query_instruction": embedder.query_instruction,
            "normalized_embeddings": True,
            "department_labels": labels,
            "dataset_size": int(len(df)),
            "dataset_distribution": distribution,
            "split_sizes": split_sizes,
            "split_seed": args.seed,
            "training_params": dict(XGB_PARAMS),
            "initial_training_params": dict(INITIAL_XGB_PARAMS),
            "tuning": "Hyperparameters carried over from v1 (selected on validation only); "
            "test set not used for any decision.",
            "best_iteration": summary["best_iteration"],
            "best_validation_mlogloss": summary["best_validation_mlogloss"],
            "calibration": {"method": "temperature_scaling", "temperature": temperature},
            "validation_metrics": headline(val_metrics),
            "test_metrics": headline(test_metrics),
            "previous_model": (
                {
                    "model_version": previous.get("model_version"),
                    "embedding_model_name": previous.get("embedding_model_name"),
                    "test_metrics": previous.get("test_metrics"),
                }
                if previous
                else None
            ),
            "library_versions": {
                "xgboost": xgb.__version__,
                "scikit-learn": sklearn.__version__,
                "python": sys.version.split()[0],
            },
        }
        (staging_model / METADATA_FILENAME).write_text(json.dumps(metadata, indent=2), "utf-8")

        metrics = {
            "generated": metadata["training_date"],
            "model_version": MODEL_VERSION,
            "embedding": embedding_label,
            "api_usage_estimate": usage,
            "training": {
                "best_iteration": summary["best_iteration"],
                "best_validation_mlogloss": summary["best_validation_mlogloss"],
                "rounds_trained": summary["rounds_trained"],
                "at_best_iteration": summary["at_best_iteration"],
                "final_round": summary["final_round"],
                "checkpoints": progress.checkpoints,
                "diagnosis": summary["diagnosis"],
                "history": summary["history"],
            },
            "calibration": calibration,
            "validation": public(val_metrics),
            "test": public(test_metrics),
            "previous_model_test_metrics": metadata["previous_model"],
            "test_errors": error_examples(df, indices["test"], y_test, test_metrics, labels),
            "data_quality": {
                "near_duplicate_threshold": NEAR_DUPLICATE_THRESHOLD,
                "cross_group_near_duplicates": near_duplicates,
            },
        }
        (staging_eval / "metrics.json").write_text(json.dumps(metrics, indent=2), "utf-8")
        split_ids = {s: df["id"].iloc[idx].tolist() for s, idx in indices.items()}
        (staging_eval / "split.json").write_text(json.dumps(split_ids, indent=2), "utf-8")
        write_classification_report(
            y_test,
            test_metrics,
            val_metrics,
            summary,
            labels,
            staging_eval / "classification_report.txt",
            embedding_label,
        )
        plot_training_history(summary, progress.checkpoints, staging_eval / "training_history.png")
        plot_confusion_matrix(test_metrics, labels, staging_eval / "confusion_matrix.png")
        plot_per_department(test_metrics, labels, staging_eval / "per_department_metrics.png")
        plot_split_distribution(df, indices, staging_eval / "dataset_distribution.png")

        section("10. Verify staged model loads with the inference embedder config")
        staged = DepartmentRouter(embedder, model_dir=staging_model)
        reloaded = await staged.predict_proba_from_embeddings(x_test)
        expected = apply_temperature(test_metrics["_probabilities"], temperature)
        if not np.allclose(reloaded, expected, atol=1e-5):
            raise RuntimeError("Reloaded staged model does not reproduce test predictions")
        log("Staged model reloads and reproduces calibrated test predictions.")

    section("11. Promote")
    archived = promote(staging_model, staging_eval, args.model_dir, args.evaluation_dir)
    if archived:
        log(f"Archived previous model to {args.model_dir / 'archive' / archived}")
        log(f"Archived previous evaluation to {args.evaluation_dir / 'archive' / archived}")
    for path in sorted([*args.model_dir.iterdir(), *args.evaluation_dir.iterdir()]):
        if path.is_file():
            log(f"  wrote {path}")

    if args.show:
        import matplotlib.pyplot as plt

        plt.show()
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dataset", type=Path, default=DATASET_PATH)
    parser.add_argument("--model-dir", type=Path, default=DEFAULT_MODEL_DIR)
    parser.add_argument("--evaluation-dir", type=Path, default=EVALUATION_DIR)
    parser.add_argument("--seed", type=int, default=RANDOM_STATE, help="group split seed")
    parser.add_argument("--show", action="store_true", help="open the plots when done")
    parser.add_argument(
        "--estimate-only", action="store_true", help="print the API usage estimate and exit"
    )
    parser.add_argument("--no-cache", action="store_true", help="re-embed even if cached")
    args = parser.parse_args(argv)
    args.model_dir.mkdir(parents=True, exist_ok=True)
    args.evaluation_dir.mkdir(parents=True, exist_ok=True)
    return asyncio.run(run(args))


if __name__ == "__main__":
    raise SystemExit(main())
