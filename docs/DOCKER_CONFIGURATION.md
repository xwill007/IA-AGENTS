# Configuración Docker Multi-Asistente
## Sistema de Trading Inteligente

---

## 1. Docker Compose Principal

### 1.1 docker-compose.yml

```yaml
version: '3.8'

services:
  # =============================================
  # CORE BACKEND SERVICES
  # =============================================
  
  fastapi:
    build: 
      context: .
      dockerfile: Dockerfile
    container_name: trading-api
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://trading_user:trading_pass@postgres:5432/trading_db
      - REDIS_URL=redis://redis:6379/0
      - BINANCE_API_URL=https://testnet.binance.vision/api
      - BINANCE_WS_URL=wss://testnet.binance.vision/ws
      - OLLAMA_HOST=http://ollama:11434
      - N8N_WEBHOOK_URL=http://n8n:5678/webhook
      - LOG_LEVEL=INFO
      - ENVIRONMENT=development
    volumes:
      - ./data:/app/data
      - ./models:/app/models
      - ./logs:/app/logs
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      ollama:
        condition: service_started
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # =============================================
  # WORKFLOW ORCHESTRATION
  # =============================================
  
  n8n:
    image: n8nio/n8n:latest
    container_name: trading-n8n
    ports:
      - "5678:5678"
    environment:
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=n8n_db
      - DB_POSTGRESDB_USER=n8n_user
      - DB_POSTGRESDB_PASSWORD=n8n_pass
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=trading123
      - WEBHOOK_URL=http://localhost:5678/
      - GENERIC_TIMEZONE=UTC
      - N8N_LOG_LEVEL=info
    volumes:
      - ./n8n/workflows:/home/node/.n8n/workflows
      - ./n8n/credentials:/home/node/.n8n/credentials
      - n8n_data:/home/node/.n8n
    depends_on:
      postgres:
        condition: service_healthy
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:5678/healthz"]
      interval: 30s
      timeout: 10s
      retries: 3

  # =============================================
  # AI ASSISTANTS
  # =============================================
  
  monitor-assistant:
    build:
      context: ./assistants/monitor
      dockerfile: Dockerfile
    container_name: trading-monitor
    environment:
      - ASSISTANT_ID=market_monitor
      - ASSISTANT_TYPE=monitor
      - OLLAMA_HOST=http://ollama:11434
      - OLLAMA_MODEL=llama3.1:8b
      - REDIS_URL=redis://redis:6379/1
      - API_BASE_URL=http://fastapi:8000
      - N8N_WEBHOOK_URL=http://n8n:5678/webhook/monitor
      - LOG_LEVEL=INFO
    volumes:
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
      retries: 3

  technical-assistant:
    build:
      context: ./assistants/technical
      dockerfile: Dockerfile
    container_name: trading-technical
    environment:
      - ASSISTANT_ID=technical_analyst
      - ASSISTANT_TYPE=technical
      - OLLAMA_HOST=http://ollama:11434
      - OLLAMA_MODEL=llama3.1:8b
      - REDIS_URL=redis://redis:6379/2
      - API_BASE_URL=http://fastapi:8000
      - N8N_WEBHOOK_URL=http://n8n:5678/webhook/technical
      - LOG_LEVEL=INFO
    volumes:
      - ./data:/app/data
      - ./assistants/technical/config:/app/config
      - ./models/technical:/app/models
      - ./logs/technical:/app/logs
    depends_on:
      - ollama
      - redis
      - fastapi
    restart: unless-stopped

  fundamental-assistant:
    build:
      context: ./assistants/fundamental
      dockerfile: Dockerfile
    container_name: trading-fundamental
    environment:
      - ASSISTANT_ID=fundamental_analyst
      - ASSISTANT_TYPE=fundamental
      - OLLAMA_HOST=http://ollama:11434
      - OLLAMA_MODEL=llama3.1:8b
      - REDIS_URL=redis://redis:6379/3
      - API_BASE_URL=http://fastapi:8000
      - N8N_WEBHOOK_URL=http://n8n:5678/webhook/fundamental
      - NEWS_API_KEY=${NEWS_API_KEY:-demo_key}
      - TWITTER_BEARER_TOKEN=${TWITTER_BEARER_TOKEN:-demo_token}
      - LOG_LEVEL=INFO
    volumes:
      - ./data:/app/data
      - ./assistants/fundamental/config:/app/config
      - ./logs/fundamental:/app/logs
    depends_on:
      - ollama
      - redis
      - fastapi
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
