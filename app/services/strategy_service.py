from __future__ import annotations

import numpy as np
import pandas as pd


def compute_sma(series: pd.Series, window: int) -> pd.Series:
    return series.rolling(window=window, min_periods=window).mean()


def compute_rsi(series: pd.Series, window: int = 14) -> pd.Series:
    delta = series.diff()
    up = delta.clip(lower=0).rolling(window).mean()
    down = -delta.clip(upper=0).rolling(window).mean()
    rs = up / (down + 1e-12)
    rsi = 100 - (100 / (1 + rs))
    return rsi


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()
    data["return"] = data["close"].pct_change().fillna(0.0)
    data["sma_fast"] = compute_sma(data["close"], 10)
    data["sma_slow"] = compute_sma(data["close"], 30)
    data["rsi"] = compute_rsi(data["close"], 14)
    data["volatility"] = data["return"].rolling(30).std()

    # Objetivo binario: 1 si la vela siguiente sube, 0 si baja/igual
    data["target"] = (data["close"].shift(-1) > data["close"]).astype(int)

    # Limpiar NaNs generados por rolling
    data = data.dropna().reset_index(drop=True)

    feature_cols = ["return", "sma_fast", "sma_slow", "rsi", "volatility"]

    # Normalización simple por robustez
    for c in feature_cols:
        series = data[c]
        median = series.median()
        mad = np.median(np.abs(series - median)) + 1e-9
        data[c] = (series - median) / (1.4826 * mad)

    data["bias"] = 1.0
    return data



