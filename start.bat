@echo off
REM Script de inicio para IA-AGENTS Trading Bot en Windows
REM Este script configura e inicia todo el sistema Docker

echo 🤖 IA-AGENTS Trading Bot - Inicio del Sistema
echo ===============================================

REM Verificar si Docker está instalado
docker --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ Error: Docker no está instalado
    echo    Por favor instala Docker Desktop desde: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

REM Verificar si Docker está corriendo
docker info >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ Error: Docker no está corriendo
    echo    Por favor inicia Docker Desktop
    pause
    exit /b 1
)

echo ✅ Docker está corriendo

REM Determinar comando de compose
docker-compose --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ⚠️ docker-compose no encontrado, usando 'docker compose'
    set COMPOSE_CMD=docker compose
) else (
    set COMPOSE_CMD=docker-compose
)

REM Crear archivo .env si no existe
if not exist .env (
    echo 📝 Creando archivo .env desde template...
    copy env.example .env
    echo ✅ Archivo .env creado. Por favor configura tus API keys de Binance si deseas trading real.
)

REM Crear directorios necesarios
echo 📁 Creando directorios necesarios...
if not exist data mkdir data
if not exist models mkdir models
if not exist logs mkdir logs
if not exist notebooks mkdir notebooks
if not exist grafana mkdir grafana
if not exist grafana\dashboards mkdir grafana\dashboards
if not exist grafana\datasources mkdir grafana\datasources
if not exist prometheus mkdir prometheus

REM Crear archivo de configuración de Prometheus
echo 📊 Configurando Prometheus...
(
echo global:
echo   scrape_interval: 15s
echo   evaluation_interval: 15s
echo.
echo rule_files:
echo   # - "first_rules.yml"
echo.
echo scrape_configs:
echo   - job_name: 'prometheus'
echo     static_configs:
echo       - targets: ['localhost:9090']
echo.
echo   - job_name: 'ia-agents-api'
echo     static_configs:
echo       - targets: ['api:8000']
echo     metrics_path: '/metrics'
echo     scrape_interval: 30s
echo.
echo   - job_name: 'postgres'
echo     static_configs:
echo       - targets: ['postgres:5432']
echo.
echo   - job_name: 'redis'
echo     static_configs:
echo       - targets: ['redis:6379']
) > prometheus\prometheus.yml

REM Configurar Grafana datasources
echo 📈 Configurando Grafana...
(
echo apiVersion: 1
echo.
echo datasources:
echo   - name: Prometheus
echo     type: prometheus
echo     access: proxy
echo     url: http://prometheus:9090
echo     isDefault: true
echo     editable: true
) > grafana\datasources\prometheus.yml

REM Detener contenedores existentes si están corriendo
echo 🛑 Deteniendo contenedores existentes...
%COMPOSE_CMD% down

REM Construir imágenes actualizadas
echo 🔨 Construyendo imágenes Docker...
%COMPOSE_CMD% build --no-cache

REM Iniciar servicios base primero
echo 🚀 Iniciando servicios base (PostgreSQL, Redis)...
%COMPOSE_CMD% up -d postgres redis

REM Esperar a que la base de datos esté lista
echo ⏳ Esperando a que PostgreSQL esté listo...
timeout /t 10 /nobreak >nul

REM Verificar conectividad de PostgreSQL
set max_attempts=30
set attempt=1

:wait_postgres
docker exec ia-agents-postgres pg_isready -U ia_user -d ia_agents >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo ✅ PostgreSQL está listo
    goto postgres_ready
)

if %attempt% geq %max_attempts% (
    echo ❌ Error: PostgreSQL no respondió después de %max_attempts% intentos
    pause
    exit /b 1
)

echo   Intento %attempt%/%max_attempts% - Esperando PostgreSQL...
timeout /t 2 /nobreak >nul
set /a attempt+=1
goto wait_postgres

:postgres_ready

REM Iniciar el resto de servicios
echo 🚀 Iniciando todos los servicios...
%COMPOSE_CMD% up -d

REM Esperar a que la API esté lista
echo ⏳ Esperando a que la API esté lista...
timeout /t 5 /nobreak >nul

set max_attempts=30
set attempt=1

:wait_api
curl -f http://localhost:8000/api/health >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo ✅ API está lista
    goto api_ready
)

if %attempt% geq %max_attempts% (
    echo ⚠️ API no respondió después de %max_attempts% intentos, pero continuando...
    goto api_ready
)

echo   Intento %attempt%/%max_attempts% - Esperando API...
timeout /t 2 /nobreak >nul
set /a attempt+=1
goto wait_api

:api_ready

REM Verificar estado de todos los contenedores
echo.
echo 📋 Estado de contenedores:
echo --------------------------
%COMPOSE_CMD% ps

echo.
echo 🎉 Sistema iniciado exitosamente!
echo.
echo 📍 URLs importantes:
echo    • API:           http://localhost:8000
echo    • Documentación: http://localhost:8000/docs
echo    • n8n:           http://localhost:5678 (admin/n8n_password)
echo    • Jupyter:       http://localhost:8888 (token: jupyter_token_123)
echo    • Grafana:       http://localhost:3000 (admin/grafana_admin)
echo    • Prometheus:    http://localhost:9090
echo.
echo 🔧 Comandos útiles:
echo    • Ver logs API:    docker logs ia-agents-api -f
echo    • Parar sistema:   docker-compose down
echo    • Ejecutar tests:  python test_docker_system.py
echo.
echo ⚠️ IMPORTANTE:
echo    • Configura tus API keys de Binance en el archivo .env
echo    • Por defecto está en modo TESTNET (seguro para pruebas)
echo    • Cambia TRADING_ENABLED=true solo cuando estés listo para trading real
echo.

REM Ofrecer ejecutar tests automáticamente
set /p run_tests="¿Deseas ejecutar las pruebas automatizadas ahora? (y/n): "
if /i "%run_tests%"=="y" (
    echo 🧪 Ejecutando pruebas automatizadas...
    python test_docker_system.py
)

echo ✅ ¡Sistema IA-AGENTS listo para usar!
pause
