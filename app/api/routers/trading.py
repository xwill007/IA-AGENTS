from typing import Optional

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.services.binance_client import BinanceService
from app.services.strategy_service import build_features
from app.services.model_service import LocalClassifier
from app.services.logging_service import BinanceLogger, TimingContext


router = APIRouter(prefix="/trading", tags=["trading"])


@router.get("/klines")
def get_klines(
    symbol: str = Query(default=settings.default_symbol),
    interval: str = Query(default=settings.default_interval),
    limit: int = Query(default=500, ge=10, le=1000),
    db: Session = Depends(get_db)
):
    svc = BinanceService(db=db)
    df = svc.get_klines_df(symbol=symbol, interval=interval, limit=limit)
    return {
        "symbol": symbol,
        "interval": interval,
        "limit": limit,
        "rows": len(df),
        "columns": list(df.columns),
        "head": df.head(5).to_dict(orient="records"),
    }


@router.post("/train")
def train_model(
    symbol: str = Query(default=settings.default_symbol),
    interval: str = Query(default=settings.default_interval),
    limit: int = Query(default=1000, ge=100, le=2000),
    db: Session = Depends(get_db)
):
    with TimingContext() as timer:
        try:
            svc = BinanceService(db=db)
            df = svc.get_klines_df(symbol=symbol, interval=interval, limit=limit)
            feat_df = build_features(df)

            clf = LocalClassifier(models_dir=settings.models_dir)
            metrics = clf.train(feat_df)
            
            result = {"trained": True, "metrics": metrics}
            
            # Log trading operation
            BinanceLogger.log_trading_operation(
                db=db,
                operation_type="train",
                symbol=symbol,
                parameters={"interval": interval, "limit": limit},
                result=result,
                execution_time_ms=timer.execution_time_ms,
                success=True,
                model_accuracy=metrics.get("train_accuracy")
            )
            
            return result
        except Exception as e:
            BinanceLogger.log_trading_operation(
                db=db,
                operation_type="train",
                symbol=symbol,
                parameters={"interval": interval, "limit": limit},
                execution_time_ms=timer.execution_time_ms,
                success=False,
                error_message=str(e)
            )
            raise


@router.post("/predict")
def predict_signal(
    symbol: str = Query(default=settings.default_symbol),
    interval: str = Query(default=settings.default_interval),
    lookback: int = Query(default=100, ge=20, le=500),
):
    svc = BinanceService()
    df = svc.get_klines_df(symbol=symbol, interval=interval, limit=lookback)
    feat_df = build_features(df)

    clf = LocalClassifier(models_dir=settings.models_dir)
    if not clf.available:
        raise HTTPException(status_code=400, detail="Modelo no entrenado aún. Llama /api/trading/train primero.")

    pred = clf.predict_latest(feat_df)
    return pred


@router.get("/backtest")
def backtest(
    symbol: str = Query(default=settings.default_symbol),
    interval: str = Query(default=settings.default_interval),
    limit: int = Query(default=1000, ge=200, le=2000),
):
    svc = BinanceService()
    df = svc.get_klines_df(symbol=symbol, interval=interval, limit=limit)
    feat_df = build_features(df)

    clf = LocalClassifier(models_dir=settings.models_dir)
    if not clf.available:
        # Entrenado rápido sobre el mismo set para demo/backtest simple
        clf.train(feat_df)

    result = clf.simple_backtest(feat_df)
    return result


@router.post("/order")
def place_order(
    symbol: str = Query(default=settings.default_symbol),
    side: str = Query(default="BUY"),
    quantity: float = Query(default=0.001, gt=0),
    order_type: str = Query(default="MARKET"),
    test: Optional[bool] = Query(default=True),
):
    if not settings.trading_enabled and not test:
        raise HTTPException(status_code=403, detail="TRADING_ENABLED=false. Usa test=true para ordenes de prueba.")

    svc = BinanceService()
    resp = svc.place_order(symbol=symbol, side=side, quantity=quantity, order_type=order_type, test=test)
    return resp



