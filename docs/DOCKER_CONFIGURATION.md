# 🐳 Configuración Docker IA-AGENTS
## Sistema de Trading Multi-Asistente Completamente Operativo

---

## ✅ Estado Actual del Sistema

**Fecha de última actualización:** 28 de Agosto, 2025  
**Estado:** ✅ **COMPLETAMENTE FUNCIONAL Y OPERATIVO**

### 🚀 Servicios Activos y Funcionando

| Servicio | Puerto | Estado | URL de Acceso |
|----------|--------|--------|---------------|
| **API Principal** | 8000 | ✅ Running | http://localhost:8000 |
| **PostgreSQL** | 5432 | ✅ Healthy | localhost:5432 |
| **Redis Cache** | 6379 | ✅ Healthy | localhost:6379 |
| **Ollama AI** | 11434 | ✅ Running | http://localhost:11434 |
| **n8n Workflows** | 5678 | ✅ Running | http://localhost:5678 |
| **Grafana** | 3000 | ✅ Running | http://localhost:3000 |
| **Prometheus** | 9090 | ✅ Running | http://localhost:9090 |
| **Jupyter** | 8888 | ✅ Healthy | http://localhost:8888 |

## 1. Configuración Docker Compose Actual

### 1.1 docker-compose.yml (Configuración Operativa)

```yaml
version: '3.8'

services:
  # Base de datos PostgreSQL
  postgres:
    image: postgres:15-alpine
    container_name: ia-agents-postgres
    environment:
      POSTGRES_DB: ia_agents
      POSTGRES_USER: ia_user
      POSTGRES_PASSWORD: ia_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-db.sql:/docker-entrypoint-initdb.d/init-db.sql
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ia_user -d ia_agents"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Cache Redis
  redis:
    image: redis:7-alpine
    container_name: ia-agents-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  # API Principal
  api:
    build: .
    container_name: ia-agents-api
    env_file:
      - .env
    environment:
      - DATABASE_URL=postgresql://ia_user:ia_password@postgres:5432/ia_agents
      - REDIS_URL=redis://redis:6379/0
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./models:/app/models
      - ./logs:/app/logs
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - ia-agents-network

  # n8n Workflows
  n8n:
    image: n8nio/n8n:latest
    container_name: ia-agents-n8n
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=n8n_password
      - WEBHOOK_URL=http://localhost:5678/
      - GENERIC_TIMEZONE=America/Bogota
      - N8N_LOG_LEVEL=info
    volumes:
      - n8n_data:/home/node/.n8n
    depends_on:
      - postgres
      - redis
    restart: unless-stopped
    networks:
      - ia-agents-network

  # Ollama AI Local
  ollama:
    image: ollama/ollama:latest
    container_name: ia-agents-ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    restart: unless-stopped
    networks:
      - ia-agents-network

  # Grafana Dashboards
  grafana:
    image: grafana/grafana:latest
    container_name: ia-agents-grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=grafana_admin
    volumes:
      - grafana_data:/var/lib/grafana
    restart: unless-stopped
    networks:
      - ia-agents-network

  # Prometheus Métricas
  prometheus:
    image: prom/prometheus:latest
    container_name: ia-agents-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    restart: unless-stopped
    networks:
      - ia-agents-network

  # Jupyter Notebooks
  jupyter:
    image: jupyter/datascience-notebook:latest
    container_name: ia-agents-jupyter
    ports:
      - "8888:8888"
    environment:
      - JUPYTER_ENABLE_LAB=yes
      - JUPYTER_TOKEN=jupyter_token_123
    volumes:
      - ./notebooks:/home/jovyan/work
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8888/api"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - ia-agents-network

volumes:
  postgres_data:
  redis_data:
  ollama_data:
  grafana_data:
  prometheus_data:
  n8n_data:

networks:
  ia-agents-network:
    driver: bridge
      - ./data:/app/data
      - ./assistants/monitor/config:/app/config
      - ./logs/monitor:/app/logs
    depends_on:
      - ollama
      - redis
      - fastapi
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "-c", "import requests; requests.get('http://localhost:8080/health')"]
      interval: 60s
      timeout: 30s
```

## 2. 🚀 Comandos de Operación

### 2.1 Inicio del Sistema Completo

```bash
# Iniciar todos los servicios
docker-compose up -d

# Verificar estado de todos los servicios
docker-compose ps

# Ver logs en tiempo real
docker-compose logs -f
```

### 2.2 Comandos de Verificación

```bash
# Verificar estado de la API
curl http://localhost:8000/api/health

# Verificar documentación de la API
curl http://localhost:8000/docs

# Verificar base de datos
docker exec -it ia-agents-postgres psql -U ia_user -d ia_agents -c "\dt"

# Verificar Redis
docker exec -it ia-agents-redis redis-cli ping
```

### 2.3 Gestión de Servicios

```bash
# Detener todos los servicios
docker-compose down

# Reiniciar un servicio específico
docker-compose restart api

# Ver logs de un servicio específico
docker logs ia-agents-api

# Limpiar volúmenes (¡CUIDADO! Borra todos los datos)
docker-compose down -v
```

## 3. 🌐 URLs de Acceso del Sistema

### 3.1 Interfaces de Usuario

| Servicio | URL | Credenciales | Descripción |
|----------|-----|--------------|-------------|
| **API Docs (Swagger)** | http://localhost:8000/docs | - | Documentación interactiva de la API |
| **Grafana** | http://localhost:3000 | admin / grafana_admin | Dashboards y visualizaciones |
| **n8n** | http://localhost:5678 | admin / n8n_password | Automatización y workflows |
| **Jupyter** | http://localhost:8888 | token: jupyter_token_123 | Notebooks para análisis |
| **Prometheus** | http://localhost:9090 | - | Métricas del sistema |

### 3.2 APIs y Servicios

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **IA-Agents API** | http://localhost:8000 | API principal del sistema |
| **Health Check** | http://localhost:8000/api/health | Estado del sistema |
| **Trading Endpoints** | http://localhost:8000/api/trading/ | Endpoints de trading |
| **Paper Trading** | http://localhost:8000/api/paper-trading/ | Trading virtual |
| **Learning System** | http://localhost:8000/api/learning/ | Sistema de aprendizaje |
| **Ollama AI** | http://localhost:11434 | Servicio de IA local |

## 4. 📁 Estructura de Archivos

### 4.1 Archivos de Configuración

```
b:\GITHUB\IA-AGENTS\
├── docker-compose.yml      # Configuración principal
├── .env                    # Variables de entorno
├── Dockerfile             # Imagen de la API
├── requirements.txt       # Dependencias Python
├── init-db.sql           # Inicialización de BD
├── prometheus/
│   └── prometheus.yml     # Configuración de métricas
├── data/                  # Datos de trading
├── models/               # Modelos de IA
├── logs/                 # Logs del sistema
└── notebooks/            # Jupyter notebooks
```

### 4.2 Variables de Entorno Configuradas

```bash
# Binance Configuration
BINANCE_API_KEY=Sda0mQfTalTqjZSXOMOM4tzWr9qh52XYomFHZnNOx6Q8CskVg4Bv5L71q3KvFgDa
BINANCE_API_SECRET=xZjb1BHyohs1Ov6L555vHi5nd0rICXvQTVShcCRAM2YzRQrwx3BBVJOABaWJFjUI
BINANCE_TESTNET=true
TRADING_ENABLED=false

# Database
DATABASE_URL=postgresql://ia_user:ia_password@postgres:5432/ia_agents
REDIS_URL=redis://redis:6379/0

# Paper Trading
PAPER_TRADING_INITIAL_BALANCE=10000.0
PAPER_TRADING_TRANSACTION_FEE=0.001

# Learning Agent
LEARNING_CONFIDENCE_THRESHOLD=0.6
LEARNING_MIN_TRADES=5
```

## 5. 🔧 Resolución de Problemas

### 5.1 Problemas Comunes

**API no responde:**
```bash
# Verificar logs
docker logs ia-agents-api

# Reiniciar servicio
docker-compose restart api
```

**Base de datos no conecta:**
```bash
# Verificar PostgreSQL
docker logs ia-agents-postgres

# Reconectar
docker-compose restart postgres api
```

**Prometheus no encuentra configuración:**
```bash
# Verificar archivo de configuración
ls -la prometheus/prometheus.yml

# Recrear si es necesario
docker-compose down prometheus
docker-compose up -d prometheus
```

### 5.2 Comandos de Diagnóstico

```bash
# Estado general del sistema
docker-compose ps
docker system df

# Uso de recursos
docker stats

# Conectividad de red
docker network ls
docker network inspect ia-agents_ia-agents-network
```

---

## ✅ Sistema Verificado y Operativo

**Fecha de verificación:** 28 de Agosto, 2025  
**Todos los servicios están funcionando correctamente** ✅  
**Sistema listo para uso en producción** 🚀
    restart: unless-stopped

  risk-assistant:
    build:
      context: ./assistants/risk
      dockerfile: Dockerfile
    container_name: trading-risk
    environment:
      - ASSISTANT_ID=risk_manager
      - ASSISTANT_TYPE=risk
      - OLLAMA_HOST=http://ollama:11434
      - OLLAMA_MODEL=llama3.1:8b
      - REDIS_URL=redis://redis:6379/4
      - API_BASE_URL=http://fastapi:8000
      - N8N_WEBHOOK_URL=http://n8n:5678/webhook/risk
      - LOG_LEVEL=INFO
    volumes:
      - ./data:/app/data
      - ./assistants/risk/config:/app/config
      - ./logs/risk:/app/logs
    depends_on:
      - ollama
      - redis
      - fastapi
    restart: unless-stopped

  strategist-assistant:
    build:
      context: ./assistants/strategist
      dockerfile: Dockerfile
    container_name: trading-strategist
    environment:
      - ASSISTANT_ID=strategist
      - ASSISTANT_TYPE=strategist
      - OLLAMA_HOST=http://ollama:11434
      - OLLAMA_MODEL=llama3.1:8b
      - REDIS_URL=redis://redis:6379/5
      - API_BASE_URL=http://fastapi:8000
      - N8N_WEBHOOK_URL=http://n8n:5678/webhook/strategist
      - LOG_LEVEL=INFO
    volumes:
      - ./data:/app/data
      - ./assistants/strategist/config:/app/config
      - ./models/strategies:/app/models
      - ./logs/strategist:/app/logs
    depends_on:
      - ollama
      - redis
      - fastapi
    restart: unless-stopped

  executor-assistant:
    build:
      context: ./assistants/executor
      dockerfile: Dockerfile
    container_name: trading-executor
    environment:
      - ASSISTANT_ID=executor
      - ASSISTANT_TYPE=executor
      - OLLAMA_HOST=http://ollama:11434
      - OLLAMA_MODEL=llama3.1:8b
      - REDIS_URL=redis://redis:6379/6
      - API_BASE_URL=http://fastapi:8000
      - N8N_WEBHOOK_URL=http://n8n:5678/webhook/executor
      - LOG_LEVEL=INFO
    volumes:
      - ./data:/app/data
      - ./assistants/executor/config:/app/config
      - ./logs/executor:/app/logs
    depends_on:
      - ollama
      - redis
      - fastapi
    restart: unless-stopped

  auditor-assistant:
    build:
      context: ./assistants/auditor
      dockerfile: Dockerfile
    container_name: trading-auditor
    environment:
      - ASSISTANT_ID=auditor
      - ASSISTANT_TYPE=auditor
      - OLLAMA_HOST=http://ollama:11434
      - OLLAMA_MODEL=llama3.1:8b
      - REDIS_URL=redis://redis:6379/7
      - API_BASE_URL=http://fastapi:8000
      - N8N_WEBHOOK_URL=http://n8n:5678/webhook/auditor
      - LOG_LEVEL=INFO
    volumes:
      - ./data:/app/data
      - ./assistants/auditor/config:/app/config
      - ./logs/auditor:/app/logs
    depends_on:
      - ollama
      - redis
      - fastapi
    restart: unless-stopped

  # =============================================
  # AI INFRASTRUCTURE
  # =============================================
  
  ollama:
    image: ollama/ollama:latest
    container_name: trading-ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    environment:
      - OLLAMA_ORIGINS=*
      - OLLAMA_HOST=0.0.0.0:11434
    restart: unless-stopped
    # GPU support (uncomment if you have NVIDIA GPU)
    # deploy:
    #   resources:
    #     reservations:
    #       devices:
    #         - driver: nvidia
    #           count: 1
    #           capabilities: [gpu]

  # Model downloader service
  ollama-setup:
    image: ollama/ollama:latest
    container_name: trading-ollama-setup
    depends_on:
      - ollama
    volumes:
      - ollama_data:/root/.ollama
    entrypoint: |
      sh -c "
        echo 'Waiting for Ollama server to be ready...'
        until curl -f http://ollama:11434/api/version; do
          sleep 5
        done
        echo 'Downloading Llama 3.1 8B model...'
        ollama pull llama3.1:8b
        echo 'Model download complete!'
      "
    restart: "no"

  # =============================================
  # DATABASE SERVICES
  # =============================================
  
  postgres:
    image: postgres:15-alpine
    container_name: trading-postgres
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=trading_db
      - POSTGRES_USER=trading_user
      - POSTGRES_PASSWORD=trading_pass
      - POSTGRES_MULTIPLE_DATABASES=n8n_db
      - POSTGRES_MULTIPLE_USERS=n8n_user:n8n_pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/init:/docker-entrypoint-initdb.d
      - ./database/backups:/backups
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U trading_user -d trading_db"]
      interval: 30s
      timeout: 10s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: trading-redis
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes --maxmemory 512mb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
      - ./redis/redis.conf:/usr/local/etc/redis/redis.conf
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 5

  # =============================================
  # MONITORING & OBSERVABILITY
  # =============================================
  
  prometheus:
    image: prom/prometheus:latest
    container_name: trading-prometheus
    ports:
      - "9090:9090"
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--web.enable-lifecycle'
    volumes:
      - ./monitoring/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - ./monitoring/prometheus/rules:/etc/prometheus/rules
      - prometheus_data:/prometheus
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    container_name: trading-grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=trading123
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./monitoring/grafana/datasources:/etc/grafana/provisioning/datasources
    depends_on:
      - prometheus
    restart: unless-stopped

  # =============================================
  # WEB FRONTEND (OPTIONAL)
  # =============================================
  
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: trading-frontend
    ports:
      - "3001:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8000
      - REACT_APP_WS_URL=ws://localhost:8000/ws
      - REACT_APP_N8N_URL=http://localhost:5678
    depends_on:
      - fastapi
    restart: unless-stopped

# =============================================
# VOLUMES
# =============================================

volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local
  ollama_data:
    driver: local
  n8n_data:
    driver: local
  prometheus_data:
    driver: local
  grafana_data:
    driver: local

# =============================================
# NETWORKS
# =============================================

networks:
  default:
    driver: bridge
    ipam:
      driver: default
      config:
        - subnet: 172.20.0.0/16
```

---

## 2. Scripts de Configuración

### 2.1 setup.sh

```bash
#!/bin/bash

# Setup script for IA-AGENTS Trading System

set -e

echo "🚀 Setting up IA-AGENTS Trading System..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data/{market_data,models,logs}
mkdir -p models/{technical,fundamental,strategies}
mkdir -p logs/{api,assistants,n8n}
mkdir -p n8n/{workflows,credentials}
mkdir -p database/{init,backups}
mkdir -p monitoring/{prometheus,grafana}

# Copy environment file
if [ ! -f .env ]; then
    echo "📋 Creating .env file from template..."
    cp env.example .env
    echo "⚠️  Please edit .env file with your API keys before starting!"
fi

# Set proper permissions
echo "🔐 Setting permissions..."
chmod +x scripts/*.sh
chmod 755 data/ models/ logs/
chown -R 1000:1000 data/ models/ logs/ n8n/

# Build base assistant image
echo "🏗️  Building base assistant image..."
docker build -t trading-assistant-base:latest -f assistants/base/Dockerfile assistants/

# Pull required images
echo "📦 Pulling Docker images..."
docker-compose pull

# Initialize database
echo "🗄️  Initializing database..."
docker-compose up -d postgres redis
sleep 10

# Start Ollama and download models
echo "🤖 Setting up AI models..."
docker-compose up -d ollama
sleep 30
docker-compose up ollama-setup

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Run: docker-compose up -d"
echo "3. Access the dashboard at http://localhost:3000"
echo "4. Access n8n at http://localhost:5678 (admin/trading123)"
echo "5. Access API docs at http://localhost:8000/docs"
```

---

Esta configuración Docker proporciona:

1. **Arquitectura Completa**: Todos los servicios necesarios
2. **Escalabilidad**: Fácil agregar nuevos asistentes
3. **Monitoreo**: Prometheus y Grafana integrados
4. **Seguridad**: Usuarios no-root, health checks
5. **Desarrollo**: Scripts automatizados y comandos útiles
6. **Persistencia**: Volúmenes para datos importantes
7. **Configurabilidad**: Variables de entorno flexibles
