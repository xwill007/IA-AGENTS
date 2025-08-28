import json
import time
from datetime import datetime
from typing import Any, Optional, Dict
from sqlalchemy.orm import Session

from app.models.binance_logs import BinanceRequestLog, TradingOperation
from app.core.database import get_db


class BinanceLogger:
    """Servicio para registrar todas las operaciones de Binance"""

    @staticmethod
    def log_binance_request(
        db: Session,
        endpoint: str,
        method: str = "GET",
        request_params: Optional[Dict[str, Any]] = None,
        response_data: Optional[Any] = None,
        response_status: int = 200,
        response_time_ms: float = 0.0,
        success: bool = True,
        error_message: Optional[str] = None,
        symbol: Optional[str] = None,
        operation_type: Optional[str] = None
    ) -> BinanceRequestLog:
        """Registrar una solicitud a Binance"""
        
        log_entry = BinanceRequestLog(
            endpoint=endpoint,
            method=method,
            request_params=json.dumps(request_params) if request_params else None,
            response_data=json.dumps(response_data) if response_data else None,
            response_status=response_status,
            response_time_ms=response_time_ms,
            success=success,
            error_message=error_message,
            symbol=symbol,
            operation_type=operation_type
        )
        
        db.add(log_entry)
        db.commit()
        db.refresh(log_entry)
        return log_entry

    @staticmethod
    def log_trading_operation(
        db: Session,
        operation_type: str,
        symbol: str,
        parameters: Optional[Dict[str, Any]] = None,
        result: Optional[Any] = None,
        execution_time_ms: float = 0.0,
        success: bool = True,
        error_message: Optional[str] = None,
        model_accuracy: Optional[float] = None,
        prediction_signal: Optional[str] = None,
        prediction_probability: Optional[float] = None
    ) -> TradingOperation:
        """Registrar una operación de trading"""
        
        operation_log = TradingOperation(
            operation_type=operation_type,
            symbol=symbol,
            parameters=json.dumps(parameters) if parameters else None,
            result=json.dumps(result) if result else None,
            execution_time_ms=execution_time_ms,
            success=success,
            error_message=error_message,
            model_accuracy=model_accuracy,
            prediction_signal=prediction_signal,
            prediction_probability=prediction_probability
        )
        
        db.add(operation_log)
        db.commit()
        db.refresh(operation_log)
        return operation_log


class TimingContext:
    """Context manager para medir tiempo de ejecución"""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
    
    @property
    def execution_time_ms(self) -> float:
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time) * 1000
        return 0.0
