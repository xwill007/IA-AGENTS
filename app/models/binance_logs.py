from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean
from sqlalchemy.sql import func

from app.core.database import Base


class BinanceRequestLog(Base):
    """Tabla para logs de solicitudes a Binance"""
    __tablename__ = "binance_request_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    endpoint = Column(String(255), nullable=False, index=True)
    method = Column(String(10), nullable=False)  # GET, POST, etc.
    request_params = Column(Text)  # JSON string de parámetros
    response_status = Column(Integer)  # HTTP status code
    response_data = Column(Text)  # JSON string de respuesta
    response_time_ms = Column(Float)  # Tiempo de respuesta en ms
    success = Column(Boolean, default=True)
    error_message = Column(Text, nullable=True)
    
    # Campos específicos para trading
    symbol = Column(String(20), nullable=True, index=True)
    operation_type = Column(String(50), nullable=True, index=True)  # klines, order, account, etc.


class TradingOperation(Base):
    """Tabla para operaciones de trading específicas"""
    __tablename__ = "trading_operations"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    operation_type = Column(String(50), nullable=False, index=True)  # train, predict, backtest, order
    symbol = Column(String(20), nullable=False, index=True)
    parameters = Column(Text)  # JSON string de parámetros
    result = Column(Text)  # JSON string del resultado
    execution_time_ms = Column(Float)
    success = Column(Boolean, default=True)
    error_message = Column(Text, nullable=True)
    
    # Campos específicos para ML
    model_accuracy = Column(Float, nullable=True)
    prediction_signal = Column(String(10), nullable=True)  # BUY, SELL
    prediction_probability = Column(Float, nullable=True)
