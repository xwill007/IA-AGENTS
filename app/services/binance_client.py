from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

import pandas as pd
from binance.spot import Spot
from sqlalchemy.orm import Session

from app.core.config import settings
from app.services.logging_service import BinanceLogger, TimingContext


TESTNET_BASE_URL = "https://testnet.binance.vision"


class BinanceService:
    def __init__(self, db: Optional[Session] = None) -> None:
        self.db = db
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
        params = {"symbol": symbol, "interval": interval, "limit": limit}
        
        with TimingContext() as timer:
            try:
                raw = self.client.klines(symbol=symbol, interval=interval, limit=limit)
                success = True
                error_msg = None
            except Exception as e:
                if self.db:
                    BinanceLogger.log_binance_request(
                        self.db,
                        endpoint="klines",
                        method="GET",
                        request_params=params,
                        response_status=500,
                        response_time_ms=timer.execution_time_ms,
                        success=False,
                        error_message=str(e),
                        symbol=symbol,
                        operation_type="klines"
                    )
                raise
        
        # Log successful request
        if self.db:
            BinanceLogger.log_binance_request(
                self.db,
                endpoint="klines",
                method="GET",
                request_params=params,
                response_data={"rows_count": len(raw)},
                response_status=200,
                response_time_ms=timer.execution_time_ms,
                success=True,
                symbol=symbol,
                operation_type="klines"
            )
        
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
        params = {"symbol": symbol, "side": side, "quantity": quantity, "type": order_type, "test": test}

        with TimingContext() as timer:
            try:
                if test:
                    # Orden de prueba (no se ejecuta), válida para verificar firma y parámetros
                    self.client.new_order_test(symbol=symbol, side=side, type=order_type, quantity=quantity)
                    response = {"status": "test_order_ok", "symbol": symbol, "side": side, "quantity": quantity}
                else:
                    # Orden real
                    response = self.client.new_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
                
                success = True
                error_msg = None
            except Exception as e:
                if self.db:
                    BinanceLogger.log_binance_request(
                        self.db,
                        endpoint="new_order_test" if test else "new_order",
                        method="POST",
                        request_params=params,
                        response_status=500,
                        response_time_ms=timer.execution_time_ms,
                        success=False,
                        error_message=str(e),
                        symbol=symbol,
                        operation_type="order"
                    )
                raise
        
        # Log successful request
        if self.db:
            BinanceLogger.log_binance_request(
                self.db,
                endpoint="new_order_test" if test else "new_order",
                method="POST",
                request_params=params,
                response_data=response,
                response_status=200,
                response_time_ms=timer.execution_time_ms,
                success=True,
                symbol=symbol,
                operation_type="order"
            )
        
        return response



