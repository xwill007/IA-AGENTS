from __future__ import annotations

from datetime import datetime
from typing import Any

import pandas as pd
from binance.spot import Spot

from app.core.config import settings


TESTNET_BASE_URL = "https://testnet.binance.vision"


class BinanceService:
    def __init__(self) -> None:
        if settings.binance_testnet:
            self.client = Spot(
                api_key=settings.binance_api_key or "",
                api_secret=settings.binance_api_secret or "",
                base_url=TESTNET_BASE_URL,
            )
        else:
            self.client = Spot(
                api_key=settings.binance_api_key or "",
                api_secret=settings.binance_api_secret or "",
            )

    def get_klines_df(self, symbol: str, interval: str, limit: int = 500) -> pd.DataFrame:
        raw = self.client.klines(symbol=symbol, interval=interval, limit=limit)
        cols = [
            "open_time",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "quote_asset_volume",
            "number_of_trades",
            "taker_buy_base_asset_volume",
            "taker_buy_quote_asset_volume",
            "ignore",
        ]
        df = pd.DataFrame(raw, columns=cols)
        df["open_time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
        df["close_time"] = pd.to_datetime(df["close_time"], unit="ms", utc=True)
        for c in ["open", "high", "low", "close", "volume"]:
            df[c] = pd.to_numeric(df[c], errors="coerce")
        df = df[["open_time", "open", "high", "low", "close", "volume", "close_time"]]
        df = df.sort_values("open_time").reset_index(drop=True)
        return df

    def place_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
        order_type: str = "MARKET",
        test: bool = True,
    ) -> dict[str, Any]:
        side = side.upper()
        order_type = order_type.upper()

        if test:
            # Orden de prueba (no se ejecuta), válida para verificar firma y parámetros
            self.client.new_order_test(symbol=symbol, side=side, type=order_type, quantity=quantity)
            return {"status": "test_order_ok", "symbol": symbol, "side": side, "quantity": quantity}

        # Orden real
        resp = self.client.new_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        return resp



