"""
API Router para el sistema de aprendizaje
"""
from fastapi import APIRouter, HTTPException
from app.services.learning_agent import learning_agent, TradeOutcome
from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/learning", tags=["learning"])

class TradeOutcomeRequest(BaseModel):
    trade_id: str
    symbol: str
    side: str  # BUY or SELL
    entry_price: float
    exit_price: float
    quantity: float
    hold_time_minutes: int = 60
    market_conditions: Optional[Dict] = None
    decision_confidence: float = 0.7

class TradeEvaluationRequest(BaseModel):
    market_conditions: Dict
    signal_confidence: float

@router.post("/record-trade")
def record_trade_outcome(trade_req: TradeOutcomeRequest):
    """Registra el resultado de un trade para aprendizaje"""
    try:
        # Calcular PnL
        if trade_req.side.upper() == "BUY":
            pnl = (trade_req.exit_price - trade_req.entry_price) * trade_req.quantity
        else:  # SELL
            pnl = (trade_req.entry_price - trade_req.exit_price) * trade_req.quantity
        
        pnl_percentage = (pnl / (trade_req.entry_price * trade_req.quantity)) * 100
        
        # Crear outcome
        outcome = TradeOutcome(
            trade_id=trade_req.trade_id,
            symbol=trade_req.symbol,
            side=trade_req.side.upper(),
            entry_price=trade_req.entry_price,
            exit_price=trade_req.exit_price,
            quantity=trade_req.quantity,
            pnl=pnl,
            pnl_percentage=pnl_percentage,
            hold_time_minutes=trade_req.hold_time_minutes,
            market_conditions=trade_req.market_conditions or {},
            decision_confidence=trade_req.decision_confidence,
            timestamp=datetime.now()
        )
        
        # Registrar en el agente de aprendizaje
        learning_agent.record_trade_outcome(outcome)
        
        return {
            "message": "Trade outcome registrado exitosamente",
            "trade_id": trade_req.trade_id,
            "pnl": round(pnl, 2),
            "pnl_percentage": round(pnl_percentage, 2),
            "total_lifetime_trades": len(learning_agent.trade_outcomes)
        }
        
    except Exception as e:
        logger.error(f"Error registrando trade outcome: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/performance")
def get_learning_performance():
    """Obtiene métricas de performance y aprendizaje"""
    try:
        return learning_agent.get_performance_summary()
    except Exception as e:
        logger.error(f"Error obteniendo performance: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.post("/evaluate-trade")
def evaluate_trade_decision(eval_req: TradeEvaluationRequest):
    """Evalúa si se debe realizar un trade basado en aprendizaje"""
    try:
        decision = learning_agent.should_trade(
            market_conditions=eval_req.market_conditions,
            signal_confidence=eval_req.signal_confidence
        )
        
        return decision
        
    except Exception as e:
        logger.error(f"Error evaluando decisión de trade: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/trades-history")
def get_learning_trades():
    """Obtiene historial de trades usados para aprendizaje"""
    try:
        recent_trades = learning_agent.trade_outcomes[-50:]  # Últimos 50
        
        return {
            "total_trades": len(learning_agent.trade_outcomes),
            "recent_trades": [
                {
                    "trade_id": t.trade_id,
                    "symbol": t.symbol,
                    "side": t.side,
                    "entry_price": t.entry_price,
                    "exit_price": t.exit_price,
                    "pnl": round(t.pnl, 2),
                    "pnl_percentage": round(t.pnl_percentage, 2),
                    "hold_time_minutes": t.hold_time_minutes,
                    "decision_confidence": t.decision_confidence,
                    "timestamp": t.timestamp
                }
                for t in recent_trades
            ]
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo historial de trades: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/learning-parameters")
def get_learning_parameters():
    """Obtiene los parámetros actuales de aprendizaje"""
    try:
        return {
            "confidence_threshold": learning_agent.confidence_threshold,
            "market_conditions_weights": learning_agent.market_conditions_weights,
            "optimal_conditions": learning_agent.optimal_conditions,
            "learning_rate": learning_agent.learning_rate,
            "min_trades_for_learning": learning_agent.min_trades_for_learning,
            "total_performance_updates": len(learning_agent.performance_history)
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo parámetros: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.post("/adjust-threshold")
def adjust_confidence_threshold(new_threshold: float):
    """Ajusta manualmente el threshold de confianza"""
    try:
        if not 0.1 <= new_threshold <= 0.9:
            raise HTTPException(status_code=400, detail="Threshold debe estar entre 0.1 y 0.9")
        
        old_threshold = learning_agent.confidence_threshold
        learning_agent.confidence_threshold = new_threshold
        
        logger.info(f"🎯 Threshold ajustado manualmente: {old_threshold:.3f} → {new_threshold:.3f}")
        
        return {
            "message": "Confidence threshold ajustado",
            "old_threshold": old_threshold,
            "new_threshold": new_threshold
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error ajustando threshold: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/market-analysis")
def get_market_conditions_analysis():
    """Obtiene análisis de condiciones de mercado basado en aprendizaje"""
    try:
        if len(learning_agent.trade_outcomes) < 10:
            return {
                "message": "Datos insuficientes para análisis de mercado",
                "total_trades": len(learning_agent.trade_outcomes),
                "required_trades": 10
            }
        
        # Analizar últimos 30 trades
        recent_trades = learning_agent.trade_outcomes[-30:]
        
        # Agrupar por condiciones de mercado
        volatility_analysis = {"HIGH": [], "MEDIUM": [], "LOW": []}
        trend_analysis = {"STRONG_BULLISH": [], "STRONG_BEARISH": [], "WEAK": []}
        volume_analysis = {"HIGH": [], "NORMAL": [], "LOW": []}
        
        for trade in recent_trades:
            conditions = trade.market_conditions
            
            # Volatilidad
            vol_level = conditions.get("volatility_level", "MEDIUM")
            if vol_level in volatility_analysis:
                volatility_analysis[vol_level].append(trade.pnl_percentage)
            
            # Tendencia
            trend_level = conditions.get("trend_strength", "WEAK")
            if trend_level in trend_analysis:
                trend_analysis[trend_level].append(trade.pnl_percentage)
            
            # Volumen
            volume_ratio = conditions.get("volume_ratio", 1.0)
            if volume_ratio > 1.5:
                volume_analysis["HIGH"].append(trade.pnl_percentage)
            elif volume_ratio > 0.8:
                volume_analysis["NORMAL"].append(trade.pnl_percentage)
            else:
                volume_analysis["LOW"].append(trade.pnl_percentage)
        
        # Calcular estadísticas
        def analyze_condition(data_dict):
            result = {}
            for condition, values in data_dict.items():
                if values:
                    result[condition] = {
                        "avg_pnl": round(sum(values) / len(values), 2),
                        "win_rate": round(len([v for v in values if v > 0]) / len(values), 3),
                        "trade_count": len(values),
                        "best_trade": round(max(values), 2),
                        "worst_trade": round(min(values), 2)
                    }
                else:
                    result[condition] = {
                        "avg_pnl": 0,
                        "win_rate": 0,
                        "trade_count": 0,
                        "best_trade": 0,
                        "worst_trade": 0
                    }
            return result
        
        return {
            "analysis_period": f"Últimos {len(recent_trades)} trades",
            "volatility_performance": analyze_condition(volatility_analysis),
            "trend_performance": analyze_condition(trend_analysis),
            "volume_performance": analyze_condition(volume_analysis),
            "current_weights": learning_agent.market_conditions_weights,
            "optimal_conditions": learning_agent.optimal_conditions
        }
        
    except Exception as e:
        logger.error(f"Error en análisis de mercado: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.post("/reset-learning")
def reset_learning_data():
    """Resetea todos los datos de aprendizaje"""
    try:
        trades_count = len(learning_agent.trade_outcomes)
        performance_count = len(learning_agent.performance_history)
        
        # Resetear datos
        learning_agent.trade_outcomes.clear()
        learning_agent.performance_history.clear()
        
        # Resetear parámetros a valores iniciales
        learning_agent.confidence_threshold = 0.6
        learning_agent.market_conditions_weights = {
            "volatility": 1.0,
            "trend_strength": 1.0,
            "volume_ratio": 1.0,
            "rsi_level": 1.0,
            "macd_signal": 1.0
        }
        learning_agent.optimal_conditions = {
            "volatility_range": (1.0, 3.0),
            "volume_ratio_min": 1.2,
            "trend_strength_min": 0.7
        }
        
        logger.info("🔄 Datos de aprendizaje reseteados")
        
        return {
            "message": "Datos de aprendizaje reseteados exitosamente",
            "trades_removed": trades_count,
            "performance_records_removed": performance_count,
            "reset_timestamp": datetime.now()
        }
        
    except Exception as e:
        logger.error(f"Error reseteando datos: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@router.get("/recommendations")
def get_trading_recommendations():
    """Obtiene recomendaciones basadas en el aprendizaje actual"""
    try:
        if len(learning_agent.trade_outcomes) < 5:
            return {
                "message": "Datos insuficientes para recomendaciones",
                "recommendation": "Continúe operando para recopilar más datos"
            }
        
        latest_metrics = learning_agent.performance_history[-1]["metrics"] if learning_agent.performance_history else None
        
        recommendations = []
        
        if latest_metrics:
            # Recomendaciones basadas en win rate
            if latest_metrics.win_rate < 0.4:
                recommendations.append({
                    "type": "CONSERVATIVE",
                    "message": "Win rate bajo. Considere ser más selectivo con las operaciones.",
                    "action": "Aumentar confidence threshold"
                })
            elif latest_metrics.win_rate > 0.7:
                recommendations.append({
                    "type": "AGGRESSIVE",
                    "message": "Excelente win rate. Puede ser menos conservador.",
                    "action": "Reducir confidence threshold gradualmente"
                })
            
            # Recomendaciones basadas en profit factor
            if latest_metrics.profit_factor < 1.0:
                recommendations.append({
                    "type": "RISK_MANAGEMENT",
                    "message": "Profit factor negativo. Revise estrategia de stop loss.",
                    "action": "Implementar stop loss más estricto"
                })
            
            # Recomendaciones basadas en drawdown
            if latest_metrics.max_drawdown < -500:  # Drawdown grande
                recommendations.append({
                    "type": "POSITION_SIZING",
                    "message": "Drawdown significativo. Considere reducir tamaño de posiciones.",
                    "action": "Reducir position sizing"
                })
        
        # Recomendaciones generales
        if learning_agent.confidence_threshold > 0.75:
            recommendations.append({
                "type": "OPPORTUNITY",
                "message": "Threshold muy conservador puede estar perdiendo oportunidades.",
                "action": "Evaluar reducir threshold gradualmente"
            })
        
        return {
            "current_status": {
                "confidence_threshold": learning_agent.confidence_threshold,
                "total_trades": len(learning_agent.trade_outcomes),
                "learning_active": len(learning_agent.trade_outcomes) >= learning_agent.min_trades_for_learning
            },
            "recommendations": recommendations,
            "next_optimization": f"En {learning_agent.min_trades_for_learning - (len(learning_agent.trade_outcomes) % learning_agent.min_trades_for_learning)} trades más" if len(learning_agent.trade_outcomes) >= learning_agent.min_trades_for_learning else "Datos insuficientes"
        }
        
    except Exception as e:
        logger.error(f"Error generando recomendaciones: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
