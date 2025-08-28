# Especificaciones de Asistentes IA
## Sistema de Trading Inteligente Multi-Asistente

---

## 1. Monitor de Mercado Assistant

### 1.1 Propósito y Especialización
**Función Principal**: Vigilancia continua de mercados para detectar oportunidades y anomalías

**Especialización**:
- Detección de patrones de precio y volumen
- Identificación de breakouts y reversiones
- Monitoreo de liquidez y order flow
- Alertas de eventos de mercado significativos

### 1.2 Configuración Técnica

```python
# Monitor Assistant Configuration
monitor_config = {
    "assistant_id": "market_monitor",
    "model": "llama3.1:8b",
    "temperature": 0.1,  # Baja creatividad, alta precisión
    "max_tokens": 2048,
    "specialization": "pattern_detection",
    "update_frequency": 60,  # segundos
    "alert_thresholds": {
        "price_change": 0.03,  # 3%
        "volume_spike": 2.0,   # 2x promedio
        "spread_abnormal": 0.005  # 0.5%
    }
}
```

### 1.3 Inputs y Fuentes de Datos

```python
class MonitorInputs:
    # Datos en tiempo real
    price_data: Dict[str, float]  # OHLCV actual
    volume_data: Dict[str, float]  # Volumen por timeframe
    orderbook: Dict[str, Any]     # Bid/Ask depth
    spread_data: Dict[str, float] # Bid-ask spreads
    
    # Datos históricos para contexto
    historical_prices: pd.DataFrame  # 24h de datos
    average_volume: float           # Promedio 24h
    volatility_regime: str          # HIGH/MEDIUM/LOW
    
    # Indicadores técnicos básicos
    sma_20: float
    rsi_14: float
    bollinger_position: float
```

### 1.4 Prompts Especializados

```python
MONITOR_SYSTEM_PROMPT = """
Eres un Monitor de Mercado especializado en detectar oportunidades de trading en tiempo real.

TU ESPECIALIDAD:
- Detectar cambios significativos en precio y volumen
- Identificar patrones de breakout y reversión
- Evaluar liquidez y condiciones de mercado
- Generar alertas tempranas de oportunidades

DATOS QUE ANALIZAS:
- Precios en tiempo real (múltiples timeframes)
- Volumen y su relación con promedios históricos
- Profundidad del orderbook
- Spreads bid-ask

CRITERIOS DE ALERTA:
- Cambios de precio >3% en 15 minutos
- Picos de volumen >2x el promedio
- Breakouts de rangos establecidos
- Anomalías en liquidez

FORMATO DE RESPUESTA:
- ALERT/NORMAL
- Confianza (0-1)
- Reasoning detallado
- Datos de soporte
"""

MONITOR_ANALYSIS_PROMPT = """
Analiza los siguientes datos de mercado para {symbol}:

DATOS ACTUALES:
- Precio: {current_price} (cambio: {price_change}%)
- Volumen: {current_volume} (promedio 24h: {avg_volume})
- Spread: {spread}%
- RSI: {rsi}

CONTEXTO HISTÓRICO:
- Rango 24h: {high_24h} - {low_24h}
- Volumen promedio: {avg_volume_24h}
- Volatilidad: {volatility_regime}

¿Hay alguna oportunidad o anomalía que requiera atención inmediata?
Proporciona análisis detallado y nivel de urgencia.
"""
```

### 1.5 Outputs y Decisiones

```python
class MonitorOutput:
    alert_level: str  # NORMAL, WATCH, ALERT, URGENT
    confidence: float  # 0.0 - 1.0
    reasoning: str
    detected_patterns: List[str]
    recommended_action: str  # MONITOR, ANALYZE, ESCALATE
    
    supporting_data: Dict = {
        "price_change": float,
        "volume_ratio": float,
        "pattern_type": str,
        "timeframe": str,
        "urgency_score": float
    }
    
    next_check_interval: int  # segundos hasta próxima revisión
```

---

## 2. Analista Técnico Assistant

### 2.1 Propósito y Especialización
**Función Principal**: Análisis profundo de indicadores técnicos y patrones de gráficos

**Especialización**:
- Interpretación de indicadores técnicos múltiples
- Reconocimiento de patrones de velas japonesas
- Análisis de tendencias y niveles de soporte/resistencia
- Señales de entrada y salida optimizadas

### 2.2 Configuración Técnica

```python
technical_config = {
    "assistant_id": "technical_analyst",
    "model": "llama3.1:8b",
    "temperature": 0.2,
    "specialization": "technical_analysis",
    "indicators": [
        "RSI", "MACD", "Bollinger Bands", "EMA", "SMA",
        "Stochastic", "Williams %R", "CCI", "ADX",
        "Ichimoku", "VWAP", "Fibonacci"
    ],
    "timeframes": ["5m", "15m", "1h", "4h", "1d"],
    "pattern_recognition": True
}
```

### 2.3 Inputs Especializados

```python
class TechnicalInputs:
    # Datos OHLCV históricos
    candle_data: pd.DataFrame  # Múltiples timeframes
    
    # Indicadores calculados
    indicators: Dict[str, Dict[str, float]] = {
        "RSI_14": {"current": float, "signal": str},
        "MACD": {"line": float, "signal": float, "histogram": float},
        "BB": {"upper": float, "middle": float, "lower": float, "position": float},
        "EMA_20": float,
        "SMA_50": float,
        "Stoch": {"k": float, "d": float},
        "ADX": {"adx": float, "di_plus": float, "di_minus": float}
    }
    
    # Niveles importantes
    support_levels: List[float]
    resistance_levels: List[float]
    fibonacci_levels: Dict[str, float]
    
    # Patrones detectados automáticamente
    candlestick_patterns: List[str]
    chart_patterns: List[str]
```

### 2.4 Prompts Especializados

```python
TECHNICAL_SYSTEM_PROMPT = """
Eres un Analista Técnico experto especializado en análisis cuantitativo de mercados.

TU ESPECIALIDAD:
- Interpretación de indicadores técnicos múltiples
- Reconocimiento de patrones de velas y gráficos
- Análisis de tendencias y momentum
- Identificación de niveles críticos de soporte/resistencia

METODOLOGÍA:
1. Evalúa múltiples timeframes (5m, 15m, 1h, 4h, 1d)
2. Correlaciona indicadores para confirmar señales
3. Identifica niveles críticos de precio
4. Calcula probabilidades de éxito de señales

INDICADORES PRINCIPALES:
- Momentum: RSI, Stochastic, Williams %R
- Tendencia: MACD, ADX, EMA/SMA
- Volatilidad: Bollinger Bands, ATR
- Volumen: VWAP, OBV

FORMATO DE RESPUESTA:
- Señal: BUY/SELL/HOLD
- Confianza: 0-1
- Timeframe recomendado
- Niveles de entrada/salida
- Stop loss y take profit
"""

TECHNICAL_ANALYSIS_PROMPT = """
Analiza técnicamente {symbol} con los siguientes datos:

INDICADORES ACTUALES:
- RSI (14): {rsi} - Señal: {rsi_signal}
- MACD: {macd_line} | Signal: {macd_signal} | Histogram: {macd_hist}
- Bollinger: Precio en {bb_position}% del rango
- EMA 20: {ema_20} | SMA 50: {sma_50}
- ADX: {adx} (tendencia: {trend_strength})

NIVELES CLAVE:
- Soporte: {support_levels}
- Resistencia: {resistance_levels}
- Precio actual: {current_price}

PATRONES DETECTADOS:
- Velas: {candlestick_patterns}
- Gráficos: {chart_patterns}

Proporciona:
1. Señal principal (BUY/SELL/HOLD)
2. Confianza de la señal
3. Niveles de entrada óptimos
4. Stop loss y take profit recomendados
5. Reasoning detallado basado en múltiples indicadores
"""
```

### 2.5 Algoritmos de Análisis

```python
class TechnicalAnalyzer:
    def calculate_signal_strength(self, indicators: Dict) -> float:
        """Calcula fuerza de señal basada en múltiples indicadores"""
        signals = []
        
        # RSI signal
        rsi = indicators["RSI_14"]["current"]
        if rsi < 30:
            signals.append(("BUY", 0.8))
        elif rsi > 70:
            signals.append(("SELL", 0.8))
        else:
            signals.append(("NEUTRAL", 0.3))
        
        # MACD signal
        macd_line = indicators["MACD"]["line"]
        macd_signal = indicators["MACD"]["signal"]
        if macd_line > macd_signal:
            signals.append(("BUY", 0.7))
        else:
            signals.append(("SELL", 0.7))
        
        # Bollinger Bands
        bb_pos = indicators["BB"]["position"]
        if bb_pos < 0.2:
            signals.append(("BUY", 0.6))
        elif bb_pos > 0.8:
            signals.append(("SELL", 0.6))
        
        # Weighted average
        return self.weighted_signal_average(signals)
    
    def identify_support_resistance(self, price_data: pd.DataFrame) -> Dict:
        """Identifica niveles de soporte y resistencia usando pivots"""
        # Implementar algoritmo de pivot points
        pass
    
    def pattern_recognition(self, candle_data: pd.DataFrame) -> List[str]:
        """Reconoce patrones de velas japonesas"""
        # Implementar reconocimiento de patrones
        pass
```

---

## 3. Analista Fundamental Assistant

### 3.1 Propósito y Especialización
**Función Principal**: Análisis de factores fundamentales que afectan precios de criptomonedas

**Especialización**:
- Análisis de noticias y eventos
- Sentiment analysis de redes sociales
- Métricas on-chain cuando disponibles
- Correlaciones macro-económicas

### 3.2 Configuración Técnica

```python
fundamental_config = {
    "assistant_id": "fundamental_analyst",
    "model": "llama3.1:8b",
    "temperature": 0.3,  # Más creatividad para interpretar noticias
    "specialization": "fundamental_analysis",
    "news_sources": [
        "CoinTelegraph", "CoinDesk", "CryptoPanic",
        "BeInCrypto", "Decrypt", "The Block"
    ],
    "social_sources": ["Twitter", "Reddit"],
    "update_frequency": 300,  # 5 minutos
    "sentiment_threshold": 0.1  # Cambio mínimo para alerta
}
```

### 3.3 Inputs de Noticias y Social

```python
class FundamentalInputs:
    # Noticias recientes
    news_articles: List[Dict] = [
        {
            "title": str,
            "content": str,
            "source": str,
            "timestamp": datetime,
            "relevance_score": float,
            "sentiment": float  # -1 to 1
        }
    ]
    
    # Social media data
    social_mentions: Dict[str, Any] = {
        "twitter_mentions": int,
        "reddit_posts": int,
        "sentiment_score": float,
        "trending_topics": List[str]
    }
    
    # Market context
    market_events: List[Dict] = [
        {
            "event_type": str,  # "earnings", "partnership", "regulation"
            "impact_level": str,  # "HIGH", "MEDIUM", "LOW"
            "expected_date": datetime
        }
    ]
    
    # Correlations
    btc_correlation: float
    stock_market_correlation: float
    dxy_correlation: float
```

### 3.4 Prompts Especializados

```python
FUNDAMENTAL_SYSTEM_PROMPT = """
Eres un Analista Fundamental especializado en factores que afectan precios de criptomonedas.

TU ESPECIALIDAD:
- Análisis de impacto de noticias en precios
- Evaluación de sentiment del mercado
- Identificación de catalizadores fundamentales
- Correlaciones con factores macro-económicos

FUENTES DE ANÁLISIS:
- Noticias de fuentes confiables de crypto
- Sentiment de redes sociales (Twitter, Reddit)
- Eventos regulatorios y adopción institucional
- Métricas on-chain cuando disponibles

METODOLOGÍA:
1. Evalúa relevancia de noticias para activos específicos
2. Analiza sentiment agregado de múltiples fuentes
3. Identifica catalizadores de corto y largo plazo
4. Evalúa probabilidad de impacto en precio

FACTORES CLAVE:
- Adopción institucional
- Desarrollos regulatorios
- Partnerships y colaboraciones
- Actualizaciones tecnológicas
- Sentiment general del mercado

FORMATO DE RESPUESTA:
- Impacto: BULLISH/BEARISH/NEUTRAL
- Confianza: 0-1
- Timeframe de impacto
- Reasoning detallado
- Catalizadores identificados
"""

FUNDAMENTAL_ANALYSIS_PROMPT = """
Analiza el contexto fundamental para {symbol}:

NOTICIAS RECIENTES (últimas 24h):
{recent_news}

SENTIMENT SOCIAL:
- Twitter mentions: {twitter_mentions}
- Reddit activity: {reddit_activity}
- Sentiment score: {social_sentiment}

EVENTOS PRÓXIMOS:
{upcoming_events}

CORRELACIONES:
- BTC correlation: {btc_corr}
- Stock market correlation: {stock_corr}

Evalúa:
1. Impacto fundamental general (BULLISH/BEARISH/NEUTRAL)
2. Confianza en el análisis
3. Timeframe del impacto esperado
4. Catalizadores clave identificados
5. Riesgos fundamentales a considerar
"""
```

### 3.5 Algoritmos de Sentiment

```python
class SentimentAnalyzer:
    def analyze_news_sentiment(self, articles: List[Dict]) -> Dict:
        """Analiza sentiment de noticias usando LLM"""
        sentiments = []
        
        for article in articles:
            # Usar LLM para análisis de sentiment
            sentiment_prompt = f"""
            Analiza el sentiment de esta noticia sobre criptomonedas:
            
            Título: {article['title']}
            Contenido: {article['content'][:500]}...
            
            Clasifica el sentiment como:
            - Muy Positivo (0.8-1.0)
            - Positivo (0.3-0.7)
            - Neutral (-0.2-0.2)
            - Negativo (-0.7--0.3)
            - Muy Negativo (-1.0--0.8)
            
            Responde solo con el valor numérico.
            """
            
            sentiment_score = self.llm_client.analyze(sentiment_prompt)
            sentiments.append({
                "score": float(sentiment_score),
                "weight": article["relevance_score"]
            })
        
        # Weighted average
        total_weight = sum(s["weight"] for s in sentiments)
        weighted_sentiment = sum(s["score"] * s["weight"] for s in sentiments) / total_weight
        
        return {
            "overall_sentiment": weighted_sentiment,
            "num_articles": len(articles),
            "confidence": min(len(articles) / 10, 1.0)  # Más artículos = más confianza
        }
```

---

## 4. Gestor de Riesgo Assistant

### 4.1 Propósito y Especialización
**Función Principal**: Evaluación y gestión de riesgos de trading

**Especialización**:
- Cálculo de métricas de riesgo
- Validación de límites de exposición
- Optimización de position sizing
- Gestión de correlaciones entre posiciones

### 4.2 Configuración de Riesgo

```python
risk_config = {
    "assistant_id": "risk_manager",
    "model": "llama3.1:8b",
    "temperature": 0.1,  # Muy conservador
    "specialization": "risk_management",
    "default_limits": {
        "max_position_size": 0.1,      # 10% del portfolio
        "max_portfolio_risk": 0.02,     # 2% VAR diario
        "max_correlation": 0.7,         # Entre posiciones
        "max_drawdown": 0.1,           # 10% máximo
        "stop_loss_percentage": 0.02,   # 2%
        "take_profit_ratio": 2.5       # 2.5:1 reward:risk
    }
}
```

### 4.3 Inputs de Riesgo

```python
class RiskInputs:
    # Portfolio actual
    current_portfolio: Dict[str, Dict] = {
        "symbol": {
            "quantity": float,
            "entry_price": float,
            "current_price": float,
            "unrealized_pnl": float,
            "position_size_pct": float
        }
    }
    
    # Propuesta de trade
    trade_proposal: Dict = {
        "symbol": str,
        "side": str,  # BUY/SELL
        "quantity": float,
        "entry_price": float,
        "stop_loss": float,
        "take_profit": float,
        "confidence": float
    }
    
    # Métricas de riesgo
    portfolio_metrics: Dict = {
        "total_value": float,
        "available_balance": float,
        "current_drawdown": float,
        "daily_var": float,
        "sharpe_ratio": float
    }
    
    # Correlaciones
    correlations: Dict[str, Dict[str, float]]
    
    # Volatilidad histórica
    volatilities: Dict[str, float]
```

### 4.4 Prompts de Gestión de Riesgo

```python
RISK_SYSTEM_PROMPT = """
Eres un Gestor de Riesgo especializado en proteger el capital de trading.

TU RESPONSABILIDAD:
- Validar que todos los trades cumplan límites de riesgo
- Optimizar position sizing basado en volatilidad
- Gestionar correlaciones entre posiciones
- Prevenir riesgos de concentración y drawdown

LÍMITES QUE VIGILAS:
- Tamaño máximo de posición por trade
- Riesgo máximo del portfolio (VAR)
- Correlación máxima entre posiciones
- Drawdown máximo permitido

METODOLOGÍA:
1. Evalúa riesgo individual del trade propuesto
2. Analiza impacto en riesgo total del portfolio
3. Valida cumplimiento de todos los límites
4. Optimiza position sizing si es necesario

PRINCIPIOS:
- Preservación de capital es prioridad #1
- Nunca exceder límites pre-establecidos
- Diversificación obligatoria
- Gestión activa de correlaciones

FORMATO DE RESPUESTA:
- Decisión: APPROVE/REJECT/MODIFY
- Risk score: 0-1
- Reasoning detallado
- Modificaciones recomendadas si aplican
"""

RISK_EVALUATION_PROMPT = """
Evalúa el riesgo de este trade propuesto:

TRADE PROPUESTO:
- Symbol: {symbol}
- Side: {side}
- Quantity: {quantity}
- Entry price: {entry_price}
- Stop loss: {stop_loss}
- Take profit: {take_profit}
- Position size: {position_size_pct}% del portfolio

PORTFOLIO ACTUAL:
- Total value: ${total_value:,.2f}
- Available balance: ${available_balance:,.2f}
- Current drawdown: {current_drawdown:.2%}
- Daily VAR: {daily_var:.2%}

POSICIONES EXISTENTES:
{existing_positions}

CORRELACIONES:
{correlations}

LÍMITES:
- Max position size: {max_position_size:.1%}
- Max portfolio risk: {max_portfolio_risk:.1%}
- Max drawdown: {max_drawdown:.1%}

Evalúa:
1. ¿Cumple todos los límites de riesgo?
2. ¿Cuál es el riesgo agregado del portfolio?
3. ¿Hay riesgos de concentración?
4. ¿Recomendaciones para optimizar el trade?
"""
```

### 4.5 Algoritmos de Gestión de Riesgo

```python
class RiskManager:
    def validate_trade(self, trade_proposal: Dict, portfolio: Dict) -> Dict:
        """Valida si un trade cumple límites de riesgo"""
        validations = {}
        
        # Position size validation
        validations["position_size"] = self.validate_position_size(
            trade_proposal, portfolio
        )
        
        # Portfolio risk validation
        validations["portfolio_risk"] = self.validate_portfolio_risk(
            trade_proposal, portfolio
        )
        
        # Correlation validation
        validations["correlation"] = self.validate_correlation(
            trade_proposal, portfolio
        )
        
        # Drawdown validation
        validations["drawdown"] = self.validate_drawdown(portfolio)
        
        return self.aggregate_validation_results(validations)
    
    def calculate_optimal_position_size(self, trade_proposal: Dict, 
                                      portfolio: Dict) -> float:
        """Calcula tamaño óptimo de posición usando Kelly Criterion modificado"""
        # Probability of success (from assistant confidence)
        p = trade_proposal["confidence"]
        
        # Reward to risk ratio
        stop_loss_distance = abs(trade_proposal["entry_price"] - trade_proposal["stop_loss"])
        take_profit_distance = abs(trade_proposal["take_profit"] - trade_proposal["entry_price"])
        reward_risk_ratio = take_profit_distance / stop_loss_distance
        
        # Kelly fraction
        kelly_fraction = (p * reward_risk_ratio - (1 - p)) / reward_risk_ratio
        
        # Conservative adjustment (use 25% of Kelly)
        optimal_fraction = max(0, min(kelly_fraction * 0.25, self.max_position_size))
        
        return optimal_fraction
    
    def calculate_portfolio_var(self, portfolio: Dict, 
                               correlations: Dict) -> float:
        """Calcula Value at Risk del portfolio"""
        # Implementar cálculo de VAR usando correlaciones
        pass
```

---

## 5. Estratega Assistant

### 5.1 Propósito y Especialización
**Función Principal**: Creación y optimización de estrategias de trading

**Especialización**:
- Desarrollo de estrategias basadas en condiciones de mercado
- Optimización de parámetros mediante backtesting
- Adaptación de estrategias según performance
- Gestión de múltiples estrategias simultáneas

### 5.2 Configuración del Estratega

```python
strategist_config = {
    "assistant_id": "strategist",
    "model": "llama3.1:8b",
    "temperature": 0.4,  # Creatividad moderada para estrategias
    "specialization": "strategy_development",
    "strategy_types": [
        "momentum", "mean_reversion", "breakout", 
        "swing", "scalping", "arbitrage"
    ],
    "optimization_period": "30d",
    "min_trades_for_validation": 20,
    "performance_threshold": 0.6  # 60% win rate mínima
}
```

### 5.3 Inputs del Estratega

```python
class StrategistInputs:
    # Market conditions
    market_regime: str  # TRENDING/RANGING/VOLATILE
    volatility_level: str  # HIGH/MEDIUM/LOW
    trend_direction: str  # BULLISH/BEARISH/SIDEWAYS
    
    # Performance histórica
    strategy_performance: Dict[str, Dict] = {
        "strategy_name": {
            "win_rate": float,
            "avg_return": float,
            "sharpe_ratio": float,
            "max_drawdown": float,
            "num_trades": int,
            "last_updated": datetime
        }
    }
    
    # Consensus de otros asistentes
    assistant_consensus: Dict[str, Dict] = {
        "monitor": {"signal": str, "confidence": float},
        "technical": {"signal": str, "confidence": float},
        "fundamental": {"signal": str, "confidence": float}
    }
    
    # User preferences
    user_profile: Dict = {
        "risk_tolerance": str,  # CONSERVATIVE/MODERATE/AGGRESSIVE
        "preferred_timeframe": str,
        "max_positions": int,
        "favorite_strategies": List[str]
    }
```

### 5.4 Prompts del Estratega

```python
STRATEGIST_SYSTEM_PROMPT = """
Eres un Estratega de Trading especializado en crear y optimizar estrategias ganadoras.

TU ESPECIALIDAD:
- Desarrollar estrategias adaptadas a condiciones de mercado
- Optimizar parámetros basado en backtesting
- Combinar señales de múltiples asistentes
- Adaptar estrategias según performance

TIPOS DE ESTRATEGIAS:
- Momentum: Sigue tendencias fuertes
- Mean Reversion: Aprovecha retornos a la media
- Breakout: Capitaliza rupturas de rangos
- Swing: Posiciones de medio plazo
- Scalping: Trades de muy corto plazo

METODOLOGÍA:
1. Analiza condiciones actuales de mercado
2. Evalúa performance de estrategias existentes
3. Considera consensus de otros asistentes
4. Adapta o crea estrategia óptima
5. Define parámetros específicos

OPTIMIZACIÓN:
- Usa datos históricos para validar
- Requiere mínimo 20 trades para validación
- Win rate objetivo >60%
- Sharpe ratio >1.5
- Max drawdown <10%

FORMATO DE RESPUESTA:
- Estrategia recomendada
- Parámetros específicos
- Reasoning detallado
- Expected performance
- Risk assessment
"""

STRATEGY_CREATION_PROMPT = """
Crea una estrategia optimal para las siguientes condiciones:

CONDICIONES DE MERCADO:
- Régimen: {market_regime}
- Volatilidad: {volatility_level}
- Tendencia: {trend_direction}
- Símbolo: {symbol}

CONSENSUS DE ASISTENTES:
- Monitor: {monitor_signal} (confianza: {monitor_confidence})
- Técnico: {technical_signal} (confianza: {technical_confidence})
- Fundamental: {fundamental_signal} (confianza: {fundamental_confidence})

PERFORMANCE ESTRATEGIAS ACTUALES:
{strategy_performance}

PERFIL DEL USUARIO:
- Tolerancia al riesgo: {risk_tolerance}
- Timeframe preferido: {timeframe}
- Máx posiciones: {max_positions}

Desarrolla:
1. Estrategia más adecuada para estas condiciones
2. Parámetros específicos (entry/exit rules)
3. Risk management rules
4. Expected win rate y returns
5. Adaptaciones necesarias basadas en performance previa
"""
```

### 5.5 Motor de Estrategias

```python
class StrategyEngine:
    def __init__(self):
        self.strategies = {
            "momentum": MomentumStrategy(),
            "mean_reversion": MeanReversionStrategy(),
            "breakout": BreakoutStrategy(),
            "swing": SwingStrategy(),
            "scalping": ScalpingStrategy()
        }
    
    def select_optimal_strategy(self, market_conditions: Dict, 
                               performance_data: Dict) -> Dict:
        """Selecciona estrategia óptima basada en condiciones"""
        
        # Analyze market regime
        regime = market_conditions["market_regime"]
        volatility = market_conditions["volatility_level"]
        
        # Strategy fitness for current conditions
        strategy_scores = {}
        
        for name, strategy in self.strategies.items():
            # Base score from strategy type fit
            base_score = strategy.fitness_for_conditions(market_conditions)
            
            # Performance adjustment
            if name in performance_data:
                perf = performance_data[name]
                performance_score = (
                    perf["win_rate"] * 0.4 +
                    min(perf["sharpe_ratio"] / 2, 1.0) * 0.3 +
                    (1 - perf["max_drawdown"]) * 0.3
                )
            else:
                performance_score = 0.5  # Neutral for new strategies
            
            # Combined score
            strategy_scores[name] = base_score * 0.6 + performance_score * 0.4
        
        # Select best strategy
        best_strategy = max(strategy_scores, key=strategy_scores.get)
        
        return {
            "strategy": best_strategy,
            "confidence": strategy_scores[best_strategy],
            "parameters": self.strategies[best_strategy].get_optimal_parameters(
                market_conditions
            )
        }

class MomentumStrategy:
    def fitness_for_conditions(self, conditions: Dict) -> float:
        """Calcula qué tan adecuada es la estrategia para las condiciones"""
        score = 0.5  # Base score
        
        if conditions["trend_direction"] in ["BULLISH", "BEARISH"]:
            score += 0.3
        
        if conditions["volatility_level"] == "HIGH":
            score += 0.2
        
        return min(score, 1.0)
    
    def get_optimal_parameters(self, conditions: Dict) -> Dict:
        """Retorna parámetros optimizados para las condiciones"""
        return {
            "entry_threshold": 0.02,  # 2% momentum
            "exit_threshold": 0.01,   # 1% reverse momentum
            "stop_loss": 0.03,        # 3% stop loss
            "take_profit": 0.06,      # 6% take profit
            "timeframe": "15m",
            "rsi_filter": 50          # Solo trades si RSI > 50 (momentum)
        }
```

---

## 6. Executor Assistant

### 6.1 Propósito y Especialización
**Función Principal**: Ejecución óptima de órdenes de trading

**Especialización**:
- Timing óptimo de ejecución
- Minimización de slippage y market impact
- Gestión de diferentes tipos de órdenes
- Monitoreo post-ejecución

### 6.2 Configuración del Executor

```python
executor_config = {
    "assistant_id": "executor",
    "model": "llama3.1:8b",
    "temperature": 0.1,  # Muy preciso
    "specialization": "order_execution",
    "order_types": ["MARKET", "LIMIT", "STOP_LOSS", "TAKE_PROFIT", "OCO"],
    "max_slippage": 0.001,  # 0.1%
    "execution_timeout": 30,  # 30 seconds
    "split_threshold": 10000  # Split orders >$10k
}
```

### 6.3 Algoritmo de Ejecución

```python
class ExecutionEngine:
    def plan_execution(self, order: Dict, market_data: Dict) -> Dict:
        """Planifica la ejecución óptima de una orden"""
        
        # Analyze market conditions
        liquidity = self.analyze_liquidity(market_data["orderbook"])
        volatility = self.calculate_volatility(market_data["price_history"])
        
        # Determine execution strategy
        if order["size_usd"] > self.split_threshold:
            return self.plan_split_execution(order, liquidity)
        else:
            return self.plan_single_execution(order, market_data)
    
    def execute_order(self, execution_plan: Dict) -> Dict:
        """Ejecuta orden según el plan optimizado"""
        
        results = []
        
        for sub_order in execution_plan["sub_orders"]:
            # Wait for optimal timing
            if sub_order.get("delay"):
                time.sleep(sub_order["delay"])
            
            # Execute
            result = self.exchange_client.place_order(sub_order)
            results.append(result)
            
            # Monitor fill
            filled_order = self.monitor_fill(result["order_id"])
            results[-1].update(filled_order)
        
        return self.aggregate_execution_results(results)
```

---

## 7. Auditor Assistant

### 7.1 Propósito y Especialización
**Función Principal**: Análisis post-mortem y aprendizaje continuo

**Especialización**:
- Análisis de performance de trades
- Identificación de patrones de éxito/fracaso
- Generación de insights para mejora
- Detección de anomalías en comportamiento

### 7.2 Configuración del Auditor

```python
auditor_config = {
    "assistant_id": "auditor",
    "model": "llama3.1:8b",
    "temperature": 0.3,
    "specialization": "performance_analysis",
    "analysis_frequency": "daily",
    "lookback_period": "30d",
    "min_trades_for_analysis": 10
}
```

### 7.3 Motor de Análisis

```python
class PerformanceAuditor:
    def perform_daily_audit(self, trades: List[Dict]) -> Dict:
        """Realiza auditoría diaria de performance"""
        
        analysis = {
            "trade_analysis": self.analyze_individual_trades(trades),
            "pattern_analysis": self.identify_patterns(trades),
            "assistant_performance": self.evaluate_assistant_performance(trades),
            "recommendations": self.generate_recommendations(trades)
        }
        
        return analysis
    
    def identify_improvement_opportunities(self, performance_data: Dict) -> List[str]:
        """Identifica oportunidades de mejora específicas"""
        
        opportunities = []
        
        # Analyze win rate by conditions
        if performance_data["win_rate_by_volatility"]["HIGH"] < 0.5:
            opportunities.append(
                "Consider more conservative approach in high volatility"
            )
        
        # Analyze holding periods
        avg_holding_time = performance_data["avg_holding_time"]
        if avg_holding_time > timedelta(hours=4):
            opportunities.append(
                "Shorter holding periods might reduce risk"
            )
        
        return opportunities
```

---

Esta especificación detallada de cada asistente proporciona:

1. **Especialización Clara**: Cada asistente tiene un rol específico
2. **Configuración Técnica**: Parámetros optimizados por función
3. **Prompts Especializados**: Contexto específico para cada modelo
4. **Algoritmos de Soporte**: Lógica complementaria al LLM
5. **Integración**: Como interactúan entre ellos

¿Te gustaría que desarrolle algún asistente en particular con más detalle o que continúe con otro aspecto de la documentación?
