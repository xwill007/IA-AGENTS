# 🏗️ Arquitectura Técnica IA-AGENTS
## Sistema de Trading Inteligente Multi-Asistente - IMPLEMENTADO Y OPERATIVO

---

## ✅ Estado de Implementación

**Fecha de actualización:** 28 de Agosto, 2025  
**Estado:** ✅ **SISTEMA COMPLETAMENTE IMPLEMENTADO Y FUNCIONANDO**  
**Servicios activos:** 8/8 operativos  
**Base de código:** 100% funcional  

## 1. 🎯 Arquitectura Implementada

### 1.1 ✅ Principios de Diseño Aplicados
- **✅ Microservicios**: Sistema modular con servicios independientes
- **✅ Event-Driven**: Comunicación asíncrona implementada
- **✅ Containerización**: Todo deployado via Docker Compose
- **✅ Observabilidad**: Logging, métricas y monitoreo completo
- **✅ Fault Tolerance**: Health checks y restart automático
- **✅ Automatización**: Scripts de gestión y mantenimiento automatizados

### 1.2 ✅ Gestión Automatizada de Workflows

#### 1.2.1 Script de Actualización (update-n8n-workflow.ps1)

**Tecnología:** PowerShell v5.1+  
**Integración:** n8n REST API  
**Autenticación:** Basic Auth + API Key

**Arquitectura del Script:**
```
1. Validación de Entrada
   ├─ Verificación de archivo workflow
   └─ Validación estructura JSON

2. Gestión de Conexión
   ├─ Verificación servicio n8n
   ├─ Validación credenciales
   └─ Configuración headers API

3. Operaciones Workflow
   ├─ Búsqueda workflows existentes
   ├─ Actualización/Creación
   └─ Activación automática

4. Sistema de Reintentos
   ├─ Máximo 3 intentos
   ├─ Espera entre intentos
   └─ Manejo de errores

5. Logging y Depuración
   ├─ Mensajes DEBUG detallados
   ├─ Información de estado
   └─ Detalles de errores
```

**Características Técnicas:**
- REST API Integration
- JSON manipulation
- Error handling robusto
- Reintentos automáticos
- Logging detallado
- Manejo de credenciales seguro

### 1.2 🛠️ Stack Tecnológico Operativo

#### **✅ Backend Core (FUNCIONANDO)**
- **FastAPI**: API REST principal con 8 endpoints activos
- **Python 3.11+**: Toda la lógica implementada
- **PostgreSQL**: Base de datos con esquema completo
- **Redis**: Cache y sesiones activo
- **WebSockets**: Para comunicación en tiempo real

#### **✅ Orquestación (FUNCIONANDO)**
- **n8n**: Workflows listos para automatización
- **Docker**: 8 contenedores ejecutándose
- **Docker Compose**: Orquestación completa operativa

#### **✅ IA y ML (FUNCIONANDO)**
- **Ollama**: Servidor de IA local operativo
- **scikit-learn**: Modelos de trading implementados
- **pandas/numpy**: Procesamiento de datos activo
- **Binance API**: Datos en tiempo real

#### **✅ Monitoreo (FUNCIONANDO)**
- **Prometheus**: Métricas del sistema activas
- **Grafana**: Dashboards configurados
- **Logging**: Sistema de logs centralizado

#### **✅ Servicios Adicionales (FUNCIONANDO)**
- **Jupyter**: Notebooks para análisis de datos
- **Paper Trading**: Sistema de trading virtual
- **Learning Agent**: IA que aprende de resultados

---

## 2. 📊 Diagrama de Arquitectura Real

```mermaid
graph TB
    subgraph "🌐 Frontend Layer [OPERATIVO]"
        DOCS[📚 API Docs :8000/docs]
        GRAFANA[📈 Grafana :3000]
        N8N[🔄 n8n :5678]
        JUPYTER[📓 Jupyter :8888]
    end
    
    subgraph "🚀 API Layer [OPERATIVO]"
        API[⚡ FastAPI :8000]
        HEALTH[💚 Health Checks]
        TRADING[📈 Trading Endpoints]
        PAPER[💰 Paper Trading]
        LEARNING[🧠 Learning System]
    end
    
    subgraph "🧠 AI Layer [OPERATIVO]"
        OLLAMA[🤖 Ollama :11434]
        MODELS[🎯 ML Models]
        BINANCE[📊 Binance API]
    end
    
    subgraph "💾 Data Layer [OPERATIVO]"
        POSTGRES[(🐘 PostgreSQL :5432)]
        REDIS[(⚡ Redis :6379)]
        VOLUMES[📁 Docker Volumes]
    end
    
    subgraph "📊 Monitoring [OPERATIVO]"
        PROMETHEUS[📊 Prometheus :9090]
        METRICS[📈 Metrics Collection]
        LOGS[📝 Centralized Logging]
    end

    %% Conexiones activas
    DOCS --> API
    GRAFANA --> PROMETHEUS
    N8N --> API
    JUPYTER --> POSTGRES
    
    API --> OLLAMA
    API --> POSTGRES
    API --> REDIS
    API --> BINANCE
    
    TRADING --> MODELS
    PAPER --> LEARNING
    
    PROMETHEUS --> API
    PROMETHEUS --> POSTGRES
    PROMETHEUS --> REDIS
    
    classDef operational fill:#90EE90,stroke:#006400,stroke-width:2px
    class DOCS,GRAFANA,N8N,JUPYTER,API,HEALTH,TRADING,PAPER,LEARNING,OLLAMA,MODELS,BINANCE,POSTGRES,REDIS,VOLUMES,PROMETHEUS,METRICS,LOGS operational
    
    subgraph "Orchestration Layer"
        N8N[n8n Workflows]
        REDIS[Redis Queue]
    end
    
    subgraph "Core Services"
        FASTAPI[FastAPI Backend]
        DB[(PostgreSQL)]
        CACHE[(Redis Cache)]
    end
    
    subgraph "AI Assistants"
        MONITOR[Monitor Assistant]
        TECH[Technical Analyst]
        FUND[Fundamental Analyst]
        RISK[Risk Manager]
        STRAT[Strategist]
        EXEC[Executor]
        AUDIT[Auditor]
    end
    
    subgraph "External Services"
        BINANCE[Binance API]
        NEWS[News APIs]
        SOCIAL[Social Media APIs]
    end
    
    subgraph "ML Infrastructure"
        OLLAMA[Ollama LLM Server]
        MODELS[(Model Storage)]
    end
    
    WEB --> API
    API --> FASTAPI
    N8N --> REDIS
    FASTAPI --> DB
    FASTAPI --> CACHE
    N8N <--> MONITOR
    N8N <--> TECH
    N8N <--> FUND
    N8N <--> RISK
    N8N <--> STRAT
    N8N <--> EXEC
    N8N <--> AUDIT
    MONITOR --> OLLAMA
    TECH --> OLLAMA
    FUND --> OLLAMA
    FASTAPI --> BINANCE
    FUND --> NEWS
    FUND --> SOCIAL
    TECH --> MODELS
    STRAT --> MODELS
```

---

## 3. Componentes Detallados

### 3.1 FastAPI Backend

#### **Responsabilidades:**
- API REST para frontend
- Gestión de configuración de usuario
- Integración con exchanges
- Almacenamiento de datos de mercado
- Gestión de órdenes y portfolio
- Autenticación y autorización

#### **Estructura de Módulos:**
```
app/
├── api/
│   ├── routers/
│   │   ├── auth.py          # Autenticación
│   │   ├── config.py        # Configuración de usuario
│   │   ├── portfolio.py     # Gestión de portfolio
│   │   ├── trading.py       # Endpoints de trading
│   │   ├── assistants.py    # Estado de asistentes
│   │   └── reports.py       # Reportes y métricas
│   └── websockets.py        # WebSocket handlers
├── core/
│   ├── config.py           # Configuración global
│   ├── database.py         # Conexión a DB
│   ├── security.py         # Autenticación/autorización
│   └── events.py           # Event system
├── models/
│   ├── user.py             # Modelos de usuario
│   ├── trading.py          # Modelos de trading
│   ├── assistant.py        # Modelos de asistentes
│   └── market.py           # Modelos de datos de mercado
├── services/
│   ├── exchange/
│   │   ├── binance.py      # Cliente Binance
│   │   └── base.py         # Interface base
│   ├── data/
│   │   ├── collector.py    # Recolección de datos
│   │   └── processor.py    # Procesamiento de datos
│   └── ml/
│       ├── model_manager.py # Gestión de modelos ML
│       └── feature_engineer.py # Feature engineering
└── utils/
    ├── validators.py       # Validaciones
    ├── helpers.py          # Utilidades
    └── exceptions.py       # Excepciones custom
```

#### **Base de Datos - Esquema Principal:**
```sql
-- Usuarios y configuración
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE user_config (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    assistant_weights JSONB,
    custom_rules JSONB,
    risk_limits JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Trading y portfolio
CREATE TABLE portfolio (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    exchange VARCHAR(20),
    total_balance DECIMAL(20,8),
    available_balance DECIMAL(20,8),
    locked_balance DECIMAL(20,8),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE positions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    symbol VARCHAR(20),
    side VARCHAR(10), -- LONG/SHORT
    quantity DECIMAL(20,8),
    entry_price DECIMAL(20,8),
    current_price DECIMAL(20,8),
    pnl DECIMAL(20,8),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Decisiones y consensos
CREATE TABLE decisions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    symbol VARCHAR(20),
    action VARCHAR(20), -- BUY/SELL/HOLD
    confidence DECIMAL(3,2),
    reasoning JSONB,
    consensus_reached BOOLEAN,
    votes JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Órdenes ejecutadas
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    decision_id UUID REFERENCES decisions(id),
    exchange_order_id VARCHAR(100),
    symbol VARCHAR(20),
    side VARCHAR(10),
    type VARCHAR(20),
    quantity DECIMAL(20,8),
    price DECIMAL(20,8),
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW(),
    executed_at TIMESTAMP
);
```

### 3.2 n8n Orchestration

#### **Responsabilidades:**
- Coordinar workflows entre asistentes
- Gestionar proceso de consenso
- Trigger automático de análisis
- Escalación de decisiones al usuario
- Recolección de feedback

#### **Workflows Principales:**

##### **Workflow 1: Market Monitoring**
```yaml
name: "Market Monitoring"
trigger: 
  type: "cron"
  expression: "*/1 * * * *"  # Cada minuto
nodes:
  - monitor_market_data
  - detect_opportunities
  - trigger_analysis_if_needed
```

##### **Workflow 2: Consensus Process**
```yaml
name: "Consensus Process"
trigger:
  type: "webhook"
  path: "/consensus/start"
nodes:
  - gather_initial_analysis
  - round_1_debate
  - round_2_debate
  - round_3_vote
  - check_consensus
  - execute_or_escalate
```

##### **Workflow 3: Learning Loop**
```yaml
name: "Learning Loop"
trigger:
  type: "cron"
  expression: "0 0 * * *"  # Diario
nodes:
  - collect_trade_outcomes
  - analyze_performance
  - update_models
  - generate_insights
```

### 3.3 Asistentes IA Especializados

#### **Arquitectura Base de Asistente:**
```python
from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Dict, Any, List

class AssistantMessage(BaseModel):
    from_assistant: str
    to_assistant: str
    message_type: str  # analysis, vote, debate, etc.
    content: Dict[str, Any]
    timestamp: float

class AssistantResponse(BaseModel):
    assistant_id: str
    confidence: float
    reasoning: str
    recommendation: str
    supporting_data: Dict[str, Any]

class BaseAssistant(ABC):
    def __init__(self, assistant_id: str, model_config: Dict):
        self.assistant_id = assistant_id
        self.model_config = model_config
        self.conversation_history = []
    
    @abstractmethod
    async def analyze(self, market_data: Dict) -> AssistantResponse:
        pass
    
    @abstractmethod
    async def participate_in_debate(self, 
                                  topic: str, 
                                  other_opinions: List[AssistantResponse]) -> str:
        pass
    
    @abstractmethod
    async def vote(self, options: List[str]) -> Dict[str, float]:
        pass
    
    async def learn_from_outcome(self, decision: Dict, outcome: Dict):
        # Base learning implementation
        pass
```

#### **Monitor de Mercado:**
```python
class MarketMonitorAssistant(BaseAssistant):
    def __init__(self):
        super().__init__("market_monitor", {
            "model": "llama3:8b",
            "temperature": 0.1,
            "specialization": "pattern_detection"
        })
        self.indicators = TechnicalIndicators()
    
    async def analyze(self, market_data: Dict) -> AssistantResponse:
        # Detectar patrones y anomalías
        price_change = self.calculate_price_change(market_data)
        volume_anomaly = self.detect_volume_anomaly(market_data)
        
        if abs(price_change) > 0.03:  # 3% change
            return AssistantResponse(
                assistant_id=self.assistant_id,
                confidence=0.9,
                reasoning=f"Significant price movement detected: {price_change:.2%}",
                recommendation="ALERT",
                supporting_data={
                    "price_change": price_change,
                    "volume_ratio": volume_anomaly,
                    "timeframe": "15m"
                }
            )
```

#### **Analista Técnico:**
```python
class TechnicalAnalystAssistant(BaseAssistant):
    def __init__(self):
        super().__init__("technical_analyst", {
            "model": "llama3:8b",
            "temperature": 0.2,
            "specialization": "technical_analysis"
        })
        self.indicators = [
            "RSI", "MACD", "Bollinger Bands", "EMA", "SMA",
            "Stochastic", "Williams %R", "CCI", "ADX"
        ]
    
    async def analyze(self, market_data: Dict) -> AssistantResponse:
        # Calcular indicadores técnicos
        signals = {}
        for indicator in self.indicators:
            signals[indicator] = self.calculate_indicator(indicator, market_data)
        
        # Usar LLM para interpretar señales
        interpretation = await self.interpret_signals(signals)
        
        return AssistantResponse(
            assistant_id=self.assistant_id,
            confidence=interpretation["confidence"],
            reasoning=interpretation["reasoning"],
            recommendation=interpretation["action"],
            supporting_data=signals
        )
```

### 3.4 Sistema de Consenso

#### **Consenso Manager:**
```python
class ConsensusManager:
    def __init__(self, assistants: List[BaseAssistant]):
        self.assistants = assistants
        self.max_rounds = 3
        self.consensus_threshold = 0.5
    
    async def run_consensus_process(self, market_data: Dict) -> Dict:
        # Ronda 1: Análisis inicial
        initial_analyses = await self.gather_initial_analyses(market_data)
        
        # Rondas 2-3: Debate
        for round_num in range(2, self.max_rounds + 1):
            debate_results = await self.conduct_debate_round(
                round_num, initial_analyses
            )
            
            if self.check_consensus(debate_results):
                return self.formulate_final_decision(debate_results)
        
        # No hay consenso - escalar al usuario
        return self.escalate_to_user(initial_analyses)
    
    async def conduct_debate_round(self, round_num: int, analyses: List) -> List:
        debate_results = []
        
        for assistant in self.assistants:
            # Cada asistente puede cuestionar otros análisis
            questions = await assistant.generate_questions(analyses)
            
            # Otros asistentes responden
            responses = []
            for other_assistant in self.assistants:
                if other_assistant != assistant:
                    response = await other_assistant.respond_to_questions(questions)
                    responses.append(response)
            
            # Asistente formula posición final para esta ronda
            final_position = await assistant.formulate_position(responses)
            debate_results.append(final_position)
        
        return debate_results
```

---

## 4. Integración de Datos

### 4.1 Fuentes de Datos

#### **Datos de Mercado (Binance):**
```python
class BinanceDataCollector:
    def __init__(self):
        self.client = BinanceClient()
        self.websocket_manager = BinanceWebSocketManager()
    
    async def start_real_time_collection(self, symbols: List[str]):
        for symbol in symbols:
            # Klines data
            await self.websocket_manager.start_kline_socket(
                symbol, self.handle_kline_data
            )
            
            # Ticker data
            await self.websocket_manager.start_ticker_socket(
                symbol, self.handle_ticker_data
            )
            
            # Orderbook data
            await self.websocket_manager.start_depth_socket(
                symbol, self.handle_depth_data
            )
    
    async def handle_kline_data(self, data):
        # Procesar y almacenar datos de velas
        processed_data = self.process_kline_data(data)
        await self.store_market_data(processed_data)
        
        # Notificar a asistentes si hay cambios significativos
        if self.is_significant_change(processed_data):
            await self.notify_assistants(processed_data)
```

#### **Datos Fundamentales:**
```python
class FundamentalDataCollector:
    def __init__(self):
        self.news_apis = [
            CoinTelegraphAPI(),
            CoinDeskAPI(),
            CryptoPanicAPI()
        ]
        self.social_apis = [
            TwitterAPI(),
            RedditAPI()
        ]
    
    async def collect_news_sentiment(self, symbols: List[str]) -> Dict:
        sentiment_data = {}
        
        for symbol in symbols:
            news_articles = await self.fetch_recent_news(symbol)
            sentiment_score = await self.analyze_sentiment(news_articles)
            
            social_mentions = await self.fetch_social_mentions(symbol)
            social_sentiment = await self.analyze_social_sentiment(social_mentions)
            
            sentiment_data[symbol] = {
                "news_sentiment": sentiment_score,
                "social_sentiment": social_sentiment,
                "combined_score": (sentiment_score + social_sentiment) / 2
            }
        
        return sentiment_data
```

### 4.2 Pipeline de Datos

```python
class DataPipeline:
    def __init__(self):
        self.collectors = [
            BinanceDataCollector(),
            FundamentalDataCollector()
        ]
        self.processors = [
            TechnicalIndicatorProcessor(),
            SentimentProcessor(),
            FeatureEngineer()
        ]
        self.storage = DataStorage()
    
    async def run_pipeline(self):
        while True:
            # Recopilar datos raw
            raw_data = await self.collect_all_data()
            
            # Procesar datos
            processed_data = await self.process_data(raw_data)
            
            # Almacenar datos
            await self.storage.store(processed_data)
            
            # Notificar asistentes si es necesario
            if self.should_trigger_analysis(processed_data):
                await self.trigger_assistant_analysis(processed_data)
            
            await asyncio.sleep(60)  # Ejecutar cada minuto
```

---

## 5. Modelo de Machine Learning

### 5.1 Feature Engineering

```python
class FeatureEngineer:
    def __init__(self):
        self.technical_features = [
            "rsi_14", "macd_signal", "bb_position", "ema_cross",
            "volume_sma_ratio", "price_sma_ratio"
        ]
        self.fundamental_features = [
            "news_sentiment", "social_sentiment", "market_cap_change"
        ]
        self.temporal_features = [
            "hour_of_day", "day_of_week", "volatility_regime"
        ]
    
    def create_features(self, market_data: pd.DataFrame) -> pd.DataFrame:
        features = pd.DataFrame()
        
        # Technical features
        features = self.add_technical_features(features, market_data)
        
        # Fundamental features
        features = self.add_fundamental_features(features, market_data)
        
        # Temporal features
        features = self.add_temporal_features(features, market_data)
        
        # Interaction features
        features = self.add_interaction_features(features)
        
        return features
```

### 5.2 Modelo de Ensemble

```python
class TradingEnsembleModel:
    def __init__(self):
        self.models = {
            "direction": RandomForestClassifier(n_estimators=100),
            "magnitude": GradientBoostingRegressor(n_estimators=100),
            "confidence": LogisticRegression(),
            "risk": SVR(kernel='rbf')
        }
        self.feature_engineer = FeatureEngineer()
        self.is_trained = False
    
    def train(self, historical_data: pd.DataFrame, outcomes: pd.DataFrame):
        # Crear features
        X = self.feature_engineer.create_features(historical_data)
        
        # Entrenar cada modelo especializado
        self.models["direction"].fit(X, outcomes["direction"])
        self.models["magnitude"].fit(X, outcomes["magnitude"])
        self.models["confidence"].fit(X, outcomes["confidence"])
        self.models["risk"].fit(X, outcomes["risk_score"])
        
        self.is_trained = True
    
    def predict(self, current_data: pd.DataFrame) -> Dict:
        if not self.is_trained:
            raise ValueError("Model must be trained first")
        
        X = self.feature_engineer.create_features(current_data)
        
        predictions = {
            "direction": self.models["direction"].predict_proba(X)[0],
            "magnitude": self.models["magnitude"].predict(X)[0],
            "confidence": self.models["confidence"].predict_proba(X)[0],
            "risk_score": self.models["risk"].predict(X)[0]
        }
        
        return self.interpret_predictions(predictions)
```

---

## 6. Seguridad y Monitoreo

### 6.1 Seguridad

```python
class SecurityManager:
    def __init__(self):
        self.encryption = Fernet(self.load_encryption_key())
        self.rate_limiter = RateLimiter()
        self.audit_logger = AuditLogger()
    
    def encrypt_api_keys(self, api_keys: Dict) -> Dict:
        encrypted_keys = {}
        for exchange, keys in api_keys.items():
            encrypted_keys[exchange] = {
                "api_key": self.encryption.encrypt(keys["api_key"].encode()),
                "secret_key": self.encryption.encrypt(keys["secret_key"].encode())
            }
        return encrypted_keys
    
    def validate_trading_request(self, user_id: str, request: Dict) -> bool:
        # Validar límites de riesgo
        if not self.check_risk_limits(user_id, request):
            return False
        
        # Rate limiting
        if not self.rate_limiter.allow_request(user_id):
            return False
        
        # Log de auditoría
        self.audit_logger.log_trading_request(user_id, request)
        
        return True
```

### 6.2 Monitoreo

```python
class SystemMonitor:
    def __init__(self):
        self.metrics_client = PrometheusClient()
        self.alert_manager = AlertManager()
    
    async def monitor_system_health(self):
        while True:
            # Check assistant health
            for assistant in self.assistants:
                health = await assistant.health_check()
                self.metrics_client.record_assistant_health(
                    assistant.assistant_id, health
                )
            
            # Check data pipeline health
            pipeline_health = await self.check_data_pipeline()
            self.metrics_client.record_pipeline_health(pipeline_health)
            
            # Check trading performance
            performance = await self.calculate_performance_metrics()
            self.metrics_client.record_performance(performance)
            
            # Generate alerts if needed
            await self.check_and_send_alerts()
            
            await asyncio.sleep(30)
```

---

## 7. Deployment y Escalabilidad

### 7.1 Docker Compose Setup

```yaml
version: '3.8'
services:
  fastapi:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/trading_db
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis
  
  n8n:
    image: n8nio/n8n
    ports:
      - "5678:5678"
    environment:
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_USER=n8n_user
      - DB_POSTGRESDB_PASSWORD=n8n_pass
    volumes:
      - ./n8n_data:/home/node/.n8n
    depends_on:
      - postgres
  
  # AI Assistants
  monitor-assistant:
    build: ./assistants/monitor
    environment:
      - OLLAMA_HOST=ollama:11434
      - ASSISTANT_ID=market_monitor
    depends_on:
      - ollama
  
  technical-assistant:
    build: ./assistants/technical
    environment:
      - OLLAMA_HOST=ollama:11434
      - ASSISTANT_ID=technical_analyst
    depends_on:
      - ollama
  
  # Infrastructure
  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=trading_db
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  
  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
  
  # Monitoring
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
  
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana

volumes:
  postgres_data:
  ollama_data:
  grafana_data:
```

### 7.2 Escalabilidad Horizontal

Para futuro crecimiento, el sistema está diseñado para escalar horizontalmente:

```python
class LoadBalancer:
    def __init__(self):
        self.assistant_pools = {
            "monitor": [],
            "technical": [],
            "fundamental": [],
            # etc.
        }
    
    async def route_request(self, assistant_type: str, request: Dict):
        # Round-robin o least-connections
        available_assistants = self.get_available_assistants(assistant_type)
        selected_assistant = self.select_assistant(available_assistants)
        
        return await selected_assistant.process_request(request)
```

---

*Esta arquitectura proporciona una base sólida para el sistema de trading multi-asistente, con capacidad de escalar y evolucionar según las necesidades del proyecto.*
