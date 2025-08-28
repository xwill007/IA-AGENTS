"""
Agente de Aprendizaje para Trading Automatizado
"""
from typing import Dict, List, Tuple
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from dataclasses import dataclass
import json
import logging

logger = logging.getLogger(__name__)

@dataclass
class TradeOutcome:
    trade_id: str
    symbol: str
    side: str
    entry_price: float
    exit_price: float
    quantity: float
    pnl: float
    pnl_percentage: float
    hold_time_minutes: int
    market_conditions: Dict
    decision_confidence: float
    timestamp: datetime

@dataclass
class LearningMetrics:
    total_trades: int
    win_rate: float
    avg_pnl: float
    avg_win: float
    avg_loss: float
    sharpe_ratio: float
    max_drawdown: float
    profit_factor: float
    best_trade: float
    worst_trade: float

class LearningAgent:
    def __init__(self):
        self.trade_outcomes: List[TradeOutcome] = []
        self.performance_history: List[Dict] = []
        
        # Parámetros de aprendizaje ajustables
        self.market_conditions_weights: Dict = {
            "volatility": 1.0,
            "trend_strength": 1.0,
            "volume_ratio": 1.0,
            "rsi_level": 1.0,
            "macd_signal": 1.0
        }
        
        self.confidence_threshold = 0.6
        self.learning_rate = 0.1
        self.min_trades_for_learning = 5
        
        # Métricas de mercado óptimas aprendidas
        self.optimal_conditions = {
            "volatility_range": (1.0, 3.0),  # Rango óptimo de volatilidad
            "volume_ratio_min": 1.2,  # Ratio de volumen mínimo
            "trend_strength_min": 0.7  # Fuerza de tendencia mínima
        }
        
        logger.info("🧠 Learning Agent inicializado")
    
    def record_trade_outcome(self, outcome: TradeOutcome):
        """Registra el resultado de un trade para aprendizaje"""
        self.trade_outcomes.append(outcome)
        
        logger.info(f"📝 Trade registrado: {outcome.symbol} PnL: {outcome.pnl:.2f} ({outcome.pnl_percentage:.2f}%)")
        
        # Actualizar métricas cada 5 trades
        if len(self.trade_outcomes) % 5 == 0:
            self._update_performance_metrics()
            self._adjust_parameters()
    
    def _update_performance_metrics(self):
        """Actualiza métricas de performance"""
        if len(self.trade_outcomes) < self.min_trades_for_learning:
            return
        
        # Usar últimos 50 trades para métricas
        recent_trades = self.trade_outcomes[-50:]
        
        total_trades = len(recent_trades)
        winning_trades = [t for t in recent_trades if t.pnl > 0]
        losing_trades = [t for t in recent_trades if t.pnl < 0]
        
        win_rate = len(winning_trades) / total_trades if total_trades > 0 else 0
        avg_pnl = np.mean([t.pnl for t in recent_trades])
        avg_win = np.mean([t.pnl for t in winning_trades]) if winning_trades else 0
        avg_loss = np.mean([t.pnl for t in losing_trades]) if losing_trades else 0
        
        # Calcular Sharpe ratio
        returns = [t.pnl_percentage for t in recent_trades]
        sharpe_ratio = np.mean(returns) / np.std(returns) if np.std(returns) > 0 else 0
        
        # Calcular max drawdown
        cumulative_pnl = np.cumsum([t.pnl for t in recent_trades])
        running_max = np.maximum.accumulate(cumulative_pnl)
        drawdown = (cumulative_pnl - running_max)
        max_drawdown = np.min(drawdown) if len(drawdown) > 0 else 0
        
        # Profit factor
        total_wins = sum(t.pnl for t in winning_trades)
        total_losses = abs(sum(t.pnl for t in losing_trades))
        profit_factor = total_wins / total_losses if total_losses > 0 else float('inf')
        
        # Mejores y peores trades
        best_trade = max([t.pnl for t in recent_trades]) if recent_trades else 0
        worst_trade = min([t.pnl for t in recent_trades]) if recent_trades else 0
        
        metrics = LearningMetrics(
            total_trades=total_trades,
            win_rate=win_rate,
            avg_pnl=avg_pnl,
            avg_win=avg_win,
            avg_loss=avg_loss,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=max_drawdown,
            profit_factor=profit_factor,
            best_trade=best_trade,
            worst_trade=worst_trade
        )
        
        performance_record = {
            "timestamp": datetime.now(),
            "metrics": metrics,
            "total_lifetime_trades": len(self.trade_outcomes),
            "learning_parameters": {
                "confidence_threshold": self.confidence_threshold,
                "market_weights": self.market_conditions_weights.copy()
            }
        }
        
        self.performance_history.append(performance_record)
        
        logger.info(f"📊 Métricas actualizadas: Win Rate: {win_rate:.2%}, Avg PnL: {avg_pnl:.2f}, Sharpe: {sharpe_ratio:.2f}")
        
        return metrics
    
    def _adjust_parameters(self):
        """Ajusta parámetros basado en performance reciente"""
        if len(self.performance_history) < 2:
            return
        
        current_metrics = self.performance_history[-1]["metrics"]
        previous_metrics = self.performance_history[-2]["metrics"]
        
        # Ajustar confidence threshold basado en win rate
        if current_metrics.win_rate > 0.65:
            # Win rate excelente: ser menos conservador
            old_threshold = self.confidence_threshold
            self.confidence_threshold = max(0.5, self.confidence_threshold - 0.05)
            if self.confidence_threshold != old_threshold:
                logger.info(f"🎯 Confidence threshold reducido: {old_threshold:.3f} → {self.confidence_threshold:.3f}")
                
        elif current_metrics.win_rate < 0.45:
            # Win rate malo: ser más conservador
            old_threshold = self.confidence_threshold
            self.confidence_threshold = min(0.8, self.confidence_threshold + 0.05)
            if self.confidence_threshold != old_threshold:
                logger.info(f"🛡️ Confidence threshold aumentado: {old_threshold:.3f} → {self.confidence_threshold:.3f}")
        
        # Ajustar basado en profit factor
        if current_metrics.profit_factor < 1.2:
            # Profit factor bajo: ser más selectivo
            self.confidence_threshold = min(0.8, self.confidence_threshold + 0.02)
        
        # Analizar condiciones de mercado
        self._analyze_market_conditions_performance()
        
        # Actualizar condiciones óptimas
        self._update_optimal_conditions()
    
    def _analyze_market_conditions_performance(self):
        """Analiza qué condiciones de mercado dan mejores resultados"""
        if len(self.trade_outcomes) < 10:
            return
        
        recent_trades = self.trade_outcomes[-30:]
        
        # Agrupar trades por condiciones de mercado
        volatility_performance = {"HIGH": [], "MEDIUM": [], "LOW": []}
        trend_performance = {"STRONG_BULLISH": [], "STRONG_BEARISH": [], "WEAK": []}
        volume_performance = {"HIGH": [], "NORMAL": [], "LOW": []}
        
        for trade in recent_trades:
            conditions = trade.market_conditions
            
            # Clasificar volatilidad
            vol_level = conditions.get("volatility_level", "MEDIUM")
            if vol_level in volatility_performance:
                volatility_performance[vol_level].append(trade.pnl_percentage)
            
            # Clasificar tendencia
            trend_level = conditions.get("trend_strength", "WEAK")
            if trend_level in trend_performance:
                trend_performance[trend_level].append(trade.pnl_percentage)
            
            # Clasificar volumen
            volume_ratio = conditions.get("volume_ratio", 1.0)
            if volume_ratio > 1.5:
                volume_performance["HIGH"].append(trade.pnl_percentage)
            elif volume_ratio > 0.8:
                volume_performance["NORMAL"].append(trade.pnl_percentage)
            else:
                volume_performance["LOW"].append(trade.pnl_percentage)
        
        # Calcular performance promedio por condición
        vol_scores = {
            level: np.mean(pnls) if pnls else 0 
            for level, pnls in volatility_performance.items()
        }
        
        trend_scores = {
            level: np.mean(pnls) if pnls else 0 
            for level, pnls in trend_performance.items()
        }
        
        volume_scores = {
            level: np.mean(pnls) if pnls else 0 
            for level, pnls in volume_performance.items()
        }
        
        # Log mejores condiciones
        best_vol = max(vol_scores, key=vol_scores.get) if vol_scores else "UNKNOWN"
        best_trend = max(trend_scores, key=trend_scores.get) if trend_scores else "UNKNOWN"
        best_volume = max(volume_scores, key=volume_scores.get) if volume_scores else "UNKNOWN"
        
        logger.info(f"🔍 Análisis condiciones: Vol={best_vol}, Trend={best_trend}, Vol={best_volume}")
        
        # Ajustar pesos basado en performance (simplificado)
        if vol_scores.get("HIGH", 0) > vol_scores.get("LOW", 0):
            self.market_conditions_weights["volatility"] = min(2.0, self.market_conditions_weights["volatility"] + 0.1)
        
        if trend_scores.get("STRONG_BULLISH", 0) > trend_scores.get("WEAK", 0):
            self.market_conditions_weights["trend_strength"] = min(2.0, self.market_conditions_weights["trend_strength"] + 0.1)
    
    def _update_optimal_conditions(self):
        """Actualiza las condiciones óptimas de mercado basado en datos"""
        if len(self.trade_outcomes) < 20:
            return
        
        profitable_trades = [t for t in self.trade_outcomes[-50:] if t.pnl > 0]
        
        if not profitable_trades:
            return
        
        # Analizar condiciones de trades rentables
        volatilities = []
        volume_ratios = []
        
        for trade in profitable_trades:
            conditions = trade.market_conditions
            
            vol_value = conditions.get("volatility_value", 0)
            if vol_value > 0:
                volatilities.append(vol_value)
            
            vol_ratio = conditions.get("volume_ratio", 0)
            if vol_ratio > 0:
                volume_ratios.append(vol_ratio)
        
        # Actualizar rangos óptimos
        if volatilities:
            vol_mean = np.mean(volatilities)
            vol_std = np.std(volatilities)
            self.optimal_conditions["volatility_range"] = (
                max(0.5, vol_mean - vol_std),
                vol_mean + vol_std
            )
        
        if volume_ratios:
            self.optimal_conditions["volume_ratio_min"] = np.percentile(volume_ratios, 25)
        
        logger.info(f"📈 Condiciones óptimas actualizadas: {self.optimal_conditions}")
    
    def should_trade(self, market_conditions: Dict, signal_confidence: float) -> Dict:
        """Decide si se debe realizar un trade basado en aprendizaje"""
        
        # Verificar confidence threshold
        if signal_confidence < self.confidence_threshold:
            return {
                "should_trade": False,
                "reason": f"Confianza {signal_confidence:.3f} menor que threshold {self.confidence_threshold:.3f}",
                "confidence_score": signal_confidence,
                "threshold": self.confidence_threshold
            }
        
        # Evaluar condiciones de mercado
        market_score = self._evaluate_market_conditions(market_conditions)
        
        # Aplicar filtros aprendidos
        filters_passed, filter_reason = self._apply_learned_filters(market_conditions)
        
        if not filters_passed:
            return {
                "should_trade": False,
                "reason": f"Filtros de mercado: {filter_reason}",
                "market_score": market_score,
                "confidence_score": signal_confidence
            }
        
        # Combinar confidence con market score
        final_score = (signal_confidence * 0.7) + (market_score * 0.3)
        
        should_trade = final_score > 0.65  # Threshold más alto para final score
        
        return {
            "should_trade": should_trade,
            "final_score": final_score,
            "signal_confidence": signal_confidence,
            "market_score": market_score,
            "confidence_threshold": self.confidence_threshold,
            "reason": "Condiciones favorables" if should_trade else "Score final insuficiente"
        }
    
    def _evaluate_market_conditions(self, conditions: Dict) -> float:
        """Evalúa qué tan favorables son las condiciones actuales"""
        score = 0.5  # Base score
        
        # Evaluar volatilidad
        vol_value = conditions.get("volatility_value", 2.0)
        vol_range = self.optimal_conditions["volatility_range"]
        if vol_range[0] <= vol_value <= vol_range[1]:
            score += 0.15 * self.market_conditions_weights["volatility"]
        
        # Evaluar volumen
        volume_ratio = conditions.get("volume_ratio", 1.0)
        if volume_ratio >= self.optimal_conditions["volume_ratio_min"]:
            score += 0.1 * self.market_conditions_weights["volume_ratio"]
        
        # Evaluar tendencia
        trend_strength = conditions.get("trend_strength", "WEAK")
        if trend_strength in ["STRONG_BULLISH", "STRONG_BEARISH"]:
            score += 0.2 * self.market_conditions_weights["trend_strength"]
        
        # Evaluar RSI si está disponible
        rsi = conditions.get("rsi", 50)
        if 30 <= rsi <= 70:  # RSI en rango normal
            score += 0.05 * self.market_conditions_weights["rsi_level"]
        
        return min(1.0, score)
    
    def _apply_learned_filters(self, conditions: Dict) -> Tuple[bool, str]:
        """Aplica filtros aprendidos a las condiciones de mercado"""
        
        # Filtro de volatilidad extrema
        vol_value = conditions.get("volatility_value", 2.0)
        if vol_value > 5.0:  # Volatilidad extremadamente alta
            return False, "Volatilidad demasiado alta"
        
        if vol_value < 0.5:  # Volatilidad muy baja
            return False, "Volatilidad demasiado baja"
        
        # Filtro de volumen
        volume_ratio = conditions.get("volume_ratio", 1.0)
        if volume_ratio < 0.5:  # Volumen muy bajo
            return False, "Volumen insuficiente"
        
        # Filtro basado en performance reciente
        if len(self.performance_history) > 0:
            recent_performance = self.performance_history[-1]["metrics"]
            
            # Si performance reciente es muy mala, ser más conservador
            if recent_performance.win_rate < 0.3 and recent_performance.profit_factor < 0.8:
                # Aplicar filtros más estrictos
                if vol_value < 1.0 or volume_ratio < 1.0:
                    return False, "Performance reciente mala, aplicando filtros estrictos"
        
        return True, "Filtros pasados"
    
    def get_performance_summary(self) -> Dict:
        """Obtiene resumen de performance y aprendizaje"""
        if not self.performance_history:
            return {
                "message": "No hay datos de performance aún",
                "total_trades": len(self.trade_outcomes),
                "learning_status": "Recopilando datos iniciales"
            }
        
        latest_metrics = self.performance_history[-1]["metrics"]
        
        # Calcular tendencia de performance
        performance_trend = "estable"
        if len(self.performance_history) > 1:
            prev_wr = self.performance_history[-2]["metrics"].win_rate
            curr_wr = latest_metrics.win_rate
            
            if curr_wr > prev_wr + 0.05:
                performance_trend = "mejorando"
            elif curr_wr < prev_wr - 0.05:
                performance_trend = "empeorando"
        
        return {
            "current_performance": {
                "total_trades": latest_metrics.total_trades,
                "win_rate": round(latest_metrics.win_rate, 4),
                "avg_pnl": round(latest_metrics.avg_pnl, 2),
                "avg_win": round(latest_metrics.avg_win, 2),
                "avg_loss": round(latest_metrics.avg_loss, 2),
                "sharpe_ratio": round(latest_metrics.sharpe_ratio, 3),
                "max_drawdown": round(latest_metrics.max_drawdown, 2),
                "profit_factor": round(latest_metrics.profit_factor, 2),
                "best_trade": round(latest_metrics.best_trade, 2),
                "worst_trade": round(latest_metrics.worst_trade, 2)
            },
            "learning_parameters": {
                "confidence_threshold": round(self.confidence_threshold, 3),
                "market_conditions_weights": {k: round(v, 2) for k, v in self.market_conditions_weights.items()},
                "optimal_conditions": self.optimal_conditions
            },
            "learning_status": {
                "total_lifetime_trades": len(self.trade_outcomes),
                "performance_updates": len(self.performance_history),
                "performance_trend": performance_trend,
                "learning_active": len(self.trade_outcomes) >= self.min_trades_for_learning
            }
        }

# Instancia global del learning agent
learning_agent = LearningAgent()
