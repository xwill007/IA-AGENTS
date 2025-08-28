from typing import Optional, List
from datetime import datetime, timedelta

from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.core.database import get_db
from app.models.binance_logs import BinanceRequestLog, TradingOperation


router = APIRouter(prefix="/logs", tags=["logs"])


@router.get("/binance-requests")
def get_binance_request_logs(
    limit: int = Query(default=50, ge=1, le=500),
    symbol: Optional[str] = Query(default=None),
    operation_type: Optional[str] = Query(default=None),
    success_only: bool = Query(default=False),
    hours_back: int = Query(default=24, ge=1, le=168),  # Max 1 semana
    db: Session = Depends(get_db)
):
    """Obtener logs de solicitudes a Binance"""
    
    query = db.query(BinanceRequestLog)
    
    # Filtros
    since = datetime.utcnow() - timedelta(hours=hours_back)
    query = query.filter(BinanceRequestLog.timestamp >= since)
    
    if symbol:
        query = query.filter(BinanceRequestLog.symbol == symbol.upper())
    
    if operation_type:
        query = query.filter(BinanceRequestLog.operation_type == operation_type)
    
    if success_only:
        query = query.filter(BinanceRequestLog.success == True)
    
    # Ordenar por timestamp descendente y limitar
    logs = query.order_by(desc(BinanceRequestLog.timestamp)).limit(limit).all()
    
    return {
        "total_logs": len(logs),
        "filters": {
            "symbol": symbol,
            "operation_type": operation_type,
            "success_only": success_only,
            "hours_back": hours_back
        },
        "logs": [
            {
                "id": log.id,
                "timestamp": log.timestamp,
                "endpoint": log.endpoint,
                "method": log.method,
                "symbol": log.symbol,
                "operation_type": log.operation_type,
                "response_status": log.response_status,
                "response_time_ms": log.response_time_ms,
                "success": log.success,
                "error_message": log.error_message
            }
            for log in logs
        ]
    }


@router.get("/trading-operations")
def get_trading_operation_logs(
    limit: int = Query(default=50, ge=1, le=500),
    symbol: Optional[str] = Query(default=None),
    operation_type: Optional[str] = Query(default=None),
    success_only: bool = Query(default=False),
    hours_back: int = Query(default=24, ge=1, le=168),
    db: Session = Depends(get_db)
):
    """Obtener logs de operaciones de trading"""
    
    query = db.query(TradingOperation)
    
    # Filtros
    since = datetime.utcnow() - timedelta(hours=hours_back)
    query = query.filter(TradingOperation.timestamp >= since)
    
    if symbol:
        query = query.filter(TradingOperation.symbol == symbol.upper())
    
    if operation_type:
        query = query.filter(TradingOperation.operation_type == operation_type)
    
    if success_only:
        query = query.filter(TradingOperation.success == True)
    
    # Ordenar por timestamp descendente y limitar
    logs = query.order_by(desc(TradingOperation.timestamp)).limit(limit).all()
    
    return {
        "total_logs": len(logs),
        "filters": {
            "symbol": symbol,
            "operation_type": operation_type,
            "success_only": success_only,
            "hours_back": hours_back
        },
        "logs": [
            {
                "id": log.id,
                "timestamp": log.timestamp,
                "operation_type": log.operation_type,
                "symbol": log.symbol,
                "execution_time_ms": log.execution_time_ms,
                "success": log.success,
                "model_accuracy": log.model_accuracy,
                "prediction_signal": log.prediction_signal,
                "prediction_probability": log.prediction_probability,
                "error_message": log.error_message
            }
            for log in logs
        ]
    }


@router.get("/stats")
def get_logs_stats(
    hours_back: int = Query(default=24, ge=1, le=168),
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de los logs"""
    
    since = datetime.utcnow() - timedelta(hours=hours_back)
    
    # Stats de requests de Binance
    total_requests = db.query(BinanceRequestLog).filter(
        BinanceRequestLog.timestamp >= since
    ).count()
    
    successful_requests = db.query(BinanceRequestLog).filter(
        BinanceRequestLog.timestamp >= since,
        BinanceRequestLog.success == True
    ).count()
    
    failed_requests = total_requests - successful_requests
    
    # Stats de operaciones de trading
    total_operations = db.query(TradingOperation).filter(
        TradingOperation.timestamp >= since
    ).count()
    
    successful_operations = db.query(TradingOperation).filter(
        TradingOperation.timestamp >= since,
        TradingOperation.success == True
    ).count()
    
    failed_operations = total_operations - successful_operations
    
    # Operaciones por tipo
    operation_types = db.query(
        TradingOperation.operation_type,
        db.func.count(TradingOperation.id).label('count')
    ).filter(
        TradingOperation.timestamp >= since
    ).group_by(TradingOperation.operation_type).all()
    
    return {
        "period_hours": hours_back,
        "binance_requests": {
            "total": total_requests,
            "successful": successful_requests,
            "failed": failed_requests,
            "success_rate": round(successful_requests / max(total_requests, 1) * 100, 2)
        },
        "trading_operations": {
            "total": total_operations,
            "successful": successful_operations,
            "failed": failed_operations,
            "success_rate": round(successful_operations / max(total_operations, 1) * 100, 2)
        },
        "operations_by_type": [
            {"operation_type": op_type, "count": count}
            for op_type, count in operation_types
        ]
    }
