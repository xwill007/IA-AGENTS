#!/bin/bash

# Script de inicio para IA-AGENTS Trading Bot
# Este script configura e inicia todo el sistema Docker

echo "🤖 IA-AGENTS Trading Bot - Inicio del Sistema"
echo "==============================================="

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker no está instalado"
    echo "   Por favor instala Docker Desktop desde: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Verificar si Docker está corriendo
if ! docker info &> /dev/null; then
    echo "❌ Error: Docker no está corriendo"
    echo "   Por favor inicia Docker Desktop"
    exit 1
fi

echo "✅ Docker está corriendo"

# Verificar si docker-compose está disponible
if ! command -v docker-compose &> /dev/null; then
    echo "⚠️ docker-compose no encontrado, usando 'docker compose'"
    COMPOSE_CMD="docker compose"
else
    COMPOSE_CMD="docker-compose"
fi

# Crear archivo .env si no existe
if [ ! -f .env ]; then
    echo "📝 Creando archivo .env desde template..."
    cp env.example .env
    echo "✅ Archivo .env creado. Por favor configura tus API keys de Binance si deseas trading real."
fi

# Crear directorios necesarios
echo "📁 Creando directorios necesarios..."
mkdir -p data models logs notebooks grafana/dashboards grafana/datasources prometheus

# Crear archivo de configuración de Prometheus
echo "📊 Configurando Prometheus..."
mkdir -p prometheus
cat > prometheus/prometheus.yml << 'EOL'
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  # - "first_rules.yml"

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'ia-agents-api'
    static_configs:
      - targets: ['api:8000']
    metrics_path: '/metrics'
    scrape_interval: 30s

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres:5432']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
EOL

# Configurar Grafana datasources
echo "📈 Configurando Grafana..."
mkdir -p grafana/datasources
cat > grafana/datasources/prometheus.yml << 'EOL'
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true
EOL

# Detener contenedores existentes si están corriendo
echo "🛑 Deteniendo contenedores existentes..."
$COMPOSE_CMD down

# Construir imágenes actualizadas
echo "🔨 Construyendo imágenes Docker..."
$COMPOSE_CMD build --no-cache

# Iniciar servicios base primero
echo "🚀 Iniciando servicios base (PostgreSQL, Redis)..."
$COMPOSE_CMD up -d postgres redis

# Esperar a que la base de datos esté lista
echo "⏳ Esperando a que PostgreSQL esté listo..."
sleep 10

# Verificar conectividad de PostgreSQL
max_attempts=30
attempt=1
while [ $attempt -le $max_attempts ]; do
    if docker exec ia-agents-postgres pg_isready -U ia_user -d ia_agents &> /dev/null; then
        echo "✅ PostgreSQL está listo"
        break
    fi
    
    if [ $attempt -eq $max_attempts ]; then
        echo "❌ Error: PostgreSQL no respondió después de $max_attempts intentos"
        exit 1
    fi
    
    echo "  Intento $attempt/$max_attempts - Esperando PostgreSQL..."
    sleep 2
    ((attempt++))
done

# Iniciar el resto de servicios
echo "🚀 Iniciando todos los servicios..."
$COMPOSE_CMD up -d

# Esperar a que la API esté lista
echo "⏳ Esperando a que la API esté lista..."
sleep 5

max_attempts=30
attempt=1
while [ $attempt -le $max_attempts ]; do
    if curl -f http://localhost:8000/api/health &> /dev/null; then
        echo "✅ API está lista"
        break
    fi
    
    if [ $attempt -eq $max_attempts ]; then
        echo "⚠️ API no respondió después de $max_attempts intentos, pero continuando..."
        break
    fi
    
    echo "  Intento $attempt/$max_attempts - Esperando API..."
    sleep 2
    ((attempt++))
done

# Verificar estado de todos los contenedores
echo ""
echo "📋 Estado de contenedores:"
echo "--------------------------"
$COMPOSE_CMD ps

echo ""
echo "🎉 Sistema iniciado exitosamente!"
echo ""
echo "📍 URLs importantes:"
echo "   • API:           http://localhost:8000"
echo "   • Documentación: http://localhost:8000/docs"
echo "   • n8n:           http://localhost:5678 (admin/n8n_password)"
echo "   • Jupyter:       http://localhost:8888 (token: jupyter_token_123)"
echo "   • Grafana:       http://localhost:3000 (admin/grafana_admin)"
echo "   • Prometheus:    http://localhost:9090"
echo ""
echo "🔧 Comandos útiles:"
echo "   • Ver logs API:    docker logs ia-agents-api -f"
echo "   • Parar sistema:   docker-compose down"
echo "   • Ejecutar tests:  python test_docker_system.py"
echo ""
echo "⚠️ IMPORTANTE:"
echo "   • Configura tus API keys de Binance en el archivo .env"
echo "   • Por defecto está en modo TESTNET (seguro para pruebas)"
echo "   • Cambia TRADING_ENABLED=true solo cuando estés listo para trading real"
echo ""

# Ofrecer ejecutar tests automáticamente
read -p "¿Deseas ejecutar las pruebas automatizadas ahora? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🧪 Ejecutando pruebas automatizadas..."
    python test_docker_system.py
fi

echo "✅ ¡Sistema IA-AGENTS listo para usar!"
