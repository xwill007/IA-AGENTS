"""
API Router para Paper Trading
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.paper_trading_service import paper_engine, OrderSide
from app.services.binance_client import BinanceService
from pydantic import BaseModel
from typing import Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/paper-trading", tags=["paper-trading"])

class OrderRequest(BaseModel):
    symbol: str
    side: str  # BUY or SELL
    quantity: float
    order_type: str = "MARKET"
    price: Optional[float] = None

class PortfolioResetRequest(BaseModel):
    new_balance: float = 10000.0

@router.post("/order")
def place_paper_order(
    order_req: OrderRequest,
    db: Session = Depends(get_db)
):
    """Coloca una orden de paper trading"""
    
    try:
        # Validar side
        try:
            order_side = OrderSide(order_req.side.upper())
        except ValueError:
            raise HTTPException(status_code=400, detail="Side debe ser 'BUY' o 'SELL'")
        
        # Actualizar precio de mercado
        binance_svc = BinanceService(db=db)
        try:
            df = binance_svc.get_klines_df(symbol=order_req.symbol, interval="1m", limit=1)
            current_price = float(df.iloc[-1]['close'])
            paper_engine.update_market_price(order_req.symbol, current_price)
            
            logger.info(f"💰 Precio actual {order_req.symbol}: ${current_price:.4f}")
        except Exception as e:
            logger.error(f"Error obteniendo precio para {order_req.symbol}: {e}")
            raise HTTPException(status_code=400, detail=f"Error obteniendo precio: {str(e)}")
        
        # Colocar orden
        result = paper_engine.place_order(
            symbol=order_req.symbol,
            side=order_side,
            quantity=order_req.quantity,
            order_type=order_req.order_type.upper(),
            price=order_req.price
        )
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        # Agregar información del precio actual
        result["current_market_price"] = current_price
        result["symbol"] = order_req.symbol
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error ejecutando orden: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/portfolio")
def get_portfolio():
    """Obtiene estado actual del portfolio de paper trading"""
    try:
        summary = paper_engine.get_portfolio_summary()
        
        # Actualizar precios de posiciones actuales
        for position in summary["positions"]:
            symbol = position["symbol"]
            if symbol in paper_engine.current_prices:
                current_price = paper_engine.current_prices[symbol]
                position["current_price"] = current_price
                position["market_value"] = position["quantity"] * current_price
                
                # Recalcular PnL no realizado
                unrealized_pnl = (current_price - position["avg_entry_price"]) * position["quantity"]
                position["unrealized_pnl"] = unrealized_pnl
                position["unrealized_pnl_percentage"] = (unrealized_pnl / (position["avg_entry_price"] * position["quantity"])) * 100
        
        return summary
        
    except Exception as e:
        logger.error(f"Error obteniendo portfolio: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/trades")
def get_trade_history():
    """Obtiene historial de trades"""
    try:
        return {
            "trades": paper_engine.trade_history,
            "total_trades": len(paper_engine.trade_history)
        }
    except Exception as e:
        logger.error(f"Error obteniendo historial: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/statistics")
def get_trade_statistics():
    """Obtiene estadísticas de trading"""
    try:
        return paper_engine.get_trade_statistics()
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.post("/reset")
def reset_portfolio(reset_req: PortfolioResetRequest = PortfolioResetRequest()):
    """Resetea el portfolio de paper trading"""
    try:
        paper_engine.reset_portfolio(reset_req.new_balance)
        return {
            "message": "Portfolio reseteado exitosamente",
            "new_balance": reset_req.new_balance
        }
    except Exception as e:
        logger.error(f"Error reseteando portfolio: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.post("/close-position/{symbol}")
def close_position(symbol: str):
    """Cierra completamente una posición"""
    try:
        result = paper_engine.close_position(symbol)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return {
            "message": f"Posición {symbol} cerrada exitosamente",
            "close_order": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error cerrando posición {symbol}: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/positions")
def get_positions_only():
    """Obtiene solo las posiciones activas"""
    try:
        portfolio = paper_engine.get_portfolio_summary()
        return {
            "positions": portfolio["positions"],
            "num_positions": portfolio["num_positions"]
        }
    except Exception as e:
        logger.error(f"Error obteniendo posiciones: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.post("/update-price/{symbol}")
def update_symbol_price(symbol: str, db: Session = Depends(get_db)):
    """Actualiza manualmente el precio de un símbolo"""
    try:
        binance_svc = BinanceService(db=db)
        df = binance_svc.get_klines_df(symbol=symbol, interval="1m", limit=1)
        current_price = float(df.iloc[-1]['close'])
        
        paper_engine.update_market_price(symbol, current_price)
        
        return {
            "symbol": symbol,
            "updated_price": current_price,
            "timestamp": df.iloc[-1]['timestamp']
        }
        
    except Exception as e:
        logger.error(f"Error actualizando precio {symbol}: {e}")
        raise HTTPException(status_code=400, detail=f"Error actualizando precio: {str(e)}")

@router.get("/balance")
def get_current_balance():
    """Obtiene el balance actual disponible"""
    try:
        return {
            "initial_balance": paper_engine.initial_balance,
            "current_balance": paper_engine.current_balance,
            "available_balance": paper_engine.current_balance
        }
    except Exception as e:
        logger.error(f"Error obteniendo balance: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/performance")
def get_performance_metrics():
    """Obtiene métricas de performance del portfolio"""
    try:
        portfolio = paper_engine.get_portfolio_summary()
        statistics = paper_engine.get_trade_statistics()
        
        return {
            "portfolio_summary": {
                "total_value": portfolio["total_value"],
                "total_pnl": portfolio["total_pnl"],
                "total_return_percentage": portfolio["total_return_percentage"],
                "unrealized_pnl": portfolio["unrealized_pnl"],
                "realized_pnl": portfolio["realized_pnl"]
            },
            "trading_statistics": statistics,
            "timestamp": paper_engine.trade_history[-1]["timestamp"] if paper_engine.trade_history else None
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo métricas: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
