from __future__ import annotations

import json
import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


FEATURE_COLS = ["bias", "return", "sma_fast", "sma_slow", "rsi", "volatility"]


@dataclass
class ModelState:
    weights: np.ndarray
    feature_names: list[str]


class LocalClassifier:
    """Clasificador logístico muy simple entrenado localmente con numpy.

    - Guarda/lee el estado del modelo como pickle en `models_dir/model.pkl`.
    - Entrena con descenso de gradiente.
    """

    def __init__(self, models_dir: Path) -> None:
        self.models_dir = Path(models_dir)
        self.model_path = self.models_dir / "model.pkl"
        self.state: ModelState | None = None
        if self.model_path.exists():
            self._load()

    @property
    def available(self) -> bool:
        return self.state is not None

    def _save(self) -> None:
        assert self.state is not None
        with open(self.model_path, "wb") as f:
            pickle.dump(self.state, f)

    def _load(self) -> None:
        with open(self.model_path, "rb") as f:
            self.state = pickle.load(f)

    @staticmethod
    def _sigmoid(z: np.ndarray) -> np.ndarray:
        z = np.clip(z, -30, 30)
        return 1.0 / (1.0 + np.exp(-z))

    def _prepare_xy(self, feat_df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
        X = feat_df[FEATURE_COLS].to_numpy(dtype=float)
        y = feat_df["target"].to_numpy(dtype=float)
        return X, y

    def train(self, feat_df: pd.DataFrame, epochs: int = 400, lr: float = 0.05) -> dict[str, Any]:
        X, y = self._prepare_xy(feat_df)
        n_features = X.shape[1]
        w = np.zeros(n_features)

        for _ in range(epochs):
            logits = X @ w
            probs = self._sigmoid(logits)
            grad = X.T @ (probs - y) / X.shape[0]
            w -= lr * grad

        self.state = ModelState(weights=w, feature_names=FEATURE_COLS)
        self._save()

        # Métrica simple en train (accuracy)
        preds = (self._sigmoid(X @ w) >= 0.5).astype(int)
        acc = float((preds == y).mean())
        return {"train_accuracy": round(acc, 4)}

    def predict_latest(self, feat_df: pd.DataFrame) -> dict[str, Any]:
        if not self.available:
            raise RuntimeError("Modelo no disponible")
        X, y = self._prepare_xy(feat_df)
        x_last = X[-1]
        p = float(self._sigmoid(x_last @ self.state.weights))  # type: ignore[attr-defined]
        signal = "BUY" if p >= 0.5 else "SELL"
        return {"prob_up": round(p, 4), "signal": signal}

    def simple_backtest(self, feat_df: pd.DataFrame, fee: float = 0.0005) -> dict[str, Any]:
        if not self.available:
            raise RuntimeError("Modelo no disponible")
        X, y = self._prepare_xy(feat_df)
        probs = self._sigmoid(X @ self.state.weights)  # type: ignore[attr-defined]
        signals = (probs >= 0.5).astype(int)  # 1 buy, 0 sell

        # Retorno de la siguiente vela según posición
        rets = feat_df["return"].shift(-1).fillna(0.0).to_numpy()
        pnl = ((signals * rets) - fee * np.abs(np.diff(np.r_[signals[0], signals]))).cumsum()
        accuracy = float((signals == y).mean())
        return {
            "final_pnl": float(pnl[-1]),
            "accuracy": round(accuracy, 4),
            "samples": int(len(feat_df)),
        }



