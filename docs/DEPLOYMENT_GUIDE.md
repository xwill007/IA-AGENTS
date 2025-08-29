# ⚙️ Configuración y Deployment - IA-AGENTS
## Guía Completa de Configuración del Sistema Operativo

---

## ✅ Estado Actual de Configuración

**Fecha:** 28 de Agosto, 2025  
**Estado:** ✅ **COMPLETAMENTE CONFIGURADO Y OPERATIVO**  
**Servicios:** 8/8 funcionando correctamente  
**Base de datos:** Inicializada y poblada  
**Variables de entorno:** Configuradas y validadas  

---

## 🔧 Configuraciones Actuales

### 1. Variables de Entorno (.env)

**Archivo:** `b:\GITHUB\IA-AGENTS\.env`  

### 2. Gestión de Workflows n8n

#### 2.1 Script de Actualización de Workflows

El sistema incluye un script PowerShell para gestionar workflows de n8n de forma automatizada.

**Ubicación:** `scripts/update-n8n-workflow.ps1`

**Uso:**
```powershell
# Opción 1: Directamente desde PowerShell (requiere cambiar la política de ejecución)
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process; .\scripts\update-n8n-workflow.ps1 -WorkflowFile ".\n8n-workflows\00-system-health-check.json"

# Opción 2: Usando el parámetro -File (no requiere cambiar la política de ejecución)
powershell -ExecutionPolicy Bypass -File .\scripts\update-n8n-workflow.ps1 -WorkflowFile ".\n8n-workflows\00-system-health-check.json"
```

**Requisitos previos:**
- n8n debe estar en ejecución (puerto 5678)
- Archivo `.env` configurado con las credenciales de n8n:
  - `N8N_BASIC_AUTH_USER`
  - `N8N_BASIC_AUTH_PASSWORD`
  - `N8N_API_KEY`
- Archivo JSON del workflow válido

**Funcionalidades:**
- Actualización automática de workflows existentes
- Creación de nuevos workflows
- Activación automática de workflows
- Sistema de reintentos y manejo de errores
- Información detallada del proceso

**Ejemplo de uso para workflows del sistema:**
1. Health Check System: `00-system-health-check.json`
2. Market Monitor: `01-market-monitor.json`
3. Risk Management: `02-risk-management.json`
4. Strategy Orchestrator: `03-strategy-orchestrator.json`
**Estado:** ✅ Configurado y operativo  
**⚠️ SEGURIDAD:** Archivo .env está en .gitignore - NO se sube al repositorio

**🔐 Para configurar tu sistema:**
```bash
# 1. Copiar archivo de ejemplo
cp env.example .env

# 2. Editar .env con TUS credenciales reales
nano .env  # o usar tu editor preferido

# 3. NUNCA compartir ni subir el archivo .env al repositorio
```

**Configuración actual (ejemplo con placeholders):**  

```bash
# ======================================
# CONFIGURACIÓN BINANCE
# ======================================
BINANCE_API_KEY=Sda0mQfTalTqjZSXOMOM4tzWr9qh52XYomFHZnNOx6Q8CskVg4Bv5L71q3KvFgDa
BINANCE_API_SECRET=xZjb1BHyohs1Ov6L555vHi5nd0rICXvQTVShcCRAM2YzRQrwx3BBVJOABaWJFjUI
BINANCE_TESTNET=true                    # ✅ Modo seguro activado
TRADING_ENABLED=false                   # ✅ Paper trading por defecto

# ======================================
# CONFIGURACIÓN DE TRADING
# ======================================
DEFAULT_SYMBOL=SOLUSDT                  # Par de trading por defecto
DEFAULT_INTERVAL=1h                     # Intervalo de análisis
TZ=America/Bogota                       # Zona horaria

# ======================================
# BASE DE DATOS
# ======================================
DATABASE_URL=postgresql://ia_user:ia_password@postgres:5432/ia_agents
REDIS_URL=redis://redis:6379/0

# ======================================
# PAPER TRADING
# ======================================
PAPER_TRADING_INITIAL_BALANCE=10000.0   # Balance inicial virtual
PAPER_TRADING_TRANSACTION_FEE=0.001     # Comisión por transacción

# ======================================
# SISTEMA DE APRENDIZAJE
# ======================================
LEARNING_CONFIDENCE_THRESHOLD=0.6       # Umbral de confianza mínimo
LEARNING_MIN_TRADES=5                   # Trades mínimos para aprender

# ======================================
# API SETTINGS
# ======================================
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=true
LOG_LEVEL=INFO
LOG_FORMAT=json

# ======================================
# SERVICIOS EXTERNOS
# ======================================
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=n8n_password
JUPYTER_TOKEN=jupyter_token_123
GF_SECURITY_ADMIN_PASSWORD=grafana_admin
```

### 2. Configuración de Base de Datos

**Archivo:** `init-db.sql`  
**Estado:** ✅ Ejecutado y operativo  

```sql
-- Esquema de base de datos completo
CREATE TABLE IF NOT EXISTS trading_pairs (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL UNIQUE,
    base_asset VARCHAR(10) NOT NULL,
    quote_asset VARCHAR(10) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS paper_trades (
    id SERIAL PRIMARY KEY,
    order_id VARCHAR(50) UNIQUE NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    side VARCHAR(10) NOT NULL,
    quantity DECIMAL(20,8) NOT NULL,
    price DECIMAL(20,8) NOT NULL,
    commission DECIMAL(20,8) DEFAULT 0,
    status VARCHAR(20) DEFAULT 'FILLED',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS paper_portfolio (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    quantity DECIMAL(20,8) NOT NULL,
    avg_price DECIMAL(20,8) NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS learning_metrics (
    id SERIAL PRIMARY KEY,
    total_trades INTEGER DEFAULT 0,
    profitable_trades INTEGER DEFAULT 0,
    total_pnl DECIMAL(20,8) DEFAULT 0,
    confidence_score DECIMAL(5,4) DEFAULT 0,
    learning_iterations INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3. Configuración de Docker

**Archivo:** `docker-compose.yml`  
**Estado:** ✅ Todos los servicios ejecutándose  

**Puertos configurados:**
- API Principal: 8000
- PostgreSQL: 5432
- Redis: 6379
- Grafana: 3000
- n8n: 5678
- Prometheus: 9090
- Jupyter: 8888
- Ollama: 11434

### 4. Configuración de Prometheus

**Archivo:** `prometheus/prometheus.yml`  
**Estado:** ✅ Métricas recolectándose  

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'ia-agents-api'
    static_configs:
      - targets: ['api:8000']
    metrics_path: '/metrics'
    scrape_interval: 30s
```

---

## 🚀 Comandos de Deployment

### Deployment Inicial (Ya ejecutado)
```bash
# Clonar repositorio
git clone https://github.com/xwill007/IA-AGENTS.git
cd IA-AGENTS

# Configurar variables de entorno
cp env.example .env
# Editar .env con configuraciones específicas

# Lanzar sistema completo
docker-compose up -d

# Verificar estado
docker-compose ps
```

### Comandos de Gestión Diaria
```bash
# Ver estado de todos los servicios
docker-compose ps

# Ver logs en tiempo real
docker-compose logs -f

# Reiniciar un servicio específico
docker-compose restart api

# Actualizar un servicio
docker-compose pull api
docker-compose up -d api

# Backup de datos
docker exec ia-agents-postgres pg_dump -U ia_user ia_agents > backup.sql

# Restaurar backup
docker exec -i ia-agents-postgres psql -U ia_user ia_agents < backup.sql
```

### Comandos de Troubleshooting
```bash
# Verificar conectividad de red
docker network inspect ia-agents_ia-agents-network

# Inspeccionar un contenedor
docker inspect ia-agents-api

# Acceder a un contenedor
docker exec -it ia-agents-api bash
docker exec -it ia-agents-postgres psql -U ia_user ia_agents

# Ver uso de recursos
docker stats
```

---

## 🔒 Configuración de Seguridad

### 1. Seguridad Actual Implementada
- ✅ **Testnet Binance:** Sin dinero real en riesgo
- ✅ **Autenticación básica:** n8n protegido con usuario/contraseña
- ✅ **Aislamiento de red:** Contenedores en red privada
- ✅ **Variables seguras:** Credenciales en .env no versionado

### 2. Para Producción (Futuro)
```bash
# Cambiar a mainnet (¡CUIDADO!)
BINANCE_TESTNET=false
TRADING_ENABLED=true

# Configurar SSL/TLS
# Usar nginx como proxy reverso
# Configurar certificados SSL

# Backup automático
# Configurar cron jobs para backups
# Almacenamiento seguro de claves
```

---

## 📊 Monitoreo y Logs

### 1. Acceso a Logs
```bash
# Logs de la API
docker logs ia-agents-api

# Logs de base de datos
docker logs ia-agents-postgres

# Logs de todos los servicios
docker-compose logs -f
```

### 2. Métricas Disponibles
- **Prometheus:** http://localhost:9090
- **Grafana:** http://localhost:3000 (admin/grafana_admin)
- **Health checks:** http://localhost:8000/api/health

### 3. Dashboard URLs
```bash
# API Documentation
http://localhost:8000/docs

# Grafana Dashboards
http://localhost:3000

# n8n Workflows
http://localhost:5678

# Jupyter Notebooks
http://localhost:8888 (token: jupyter_token_123)

# Prometheus Metrics
http://localhost:9090
```

---

## 🔧 Configuraciones Personalizables

### 1. Parámetros de Trading
```bash
# En .env
DEFAULT_SYMBOL=BTCUSDT              # Cambiar par de trading
DEFAULT_INTERVAL=15m               # Cambiar intervalo de análisis
PAPER_TRADING_INITIAL_BALANCE=50000 # Aumentar balance virtual
```

### 2. Configuración de IA
```bash
# Umbral de confianza para trades
LEARNING_CONFIDENCE_THRESHOLD=0.8   # Más conservador

# Trades mínimos antes de hacer predicciones
LEARNING_MIN_TRADES=10             # Más datos antes de decidir
```

### 3. Configuración de Alertas
```bash
# En grafana (http://localhost:3000)
# Configurar alertas por email/slack
# Umbrales de pérdidas máximas
# Notificaciones de oportunidades
```

---

## 🔄 Actualizaciones y Mantenimiento

### 1. Actualizar Sistema
```bash
# Actualizar código
git pull origin main

# Reconstruir contenedores
docker-compose build

# Relanzar con nueva versión
docker-compose up -d
```

### 2. Limpieza de Sistema
```bash
# Limpiar imágenes no utilizadas
docker image prune

# Limpiar volúmenes no utilizados
docker volume prune

# Limpiar sistema completo (¡CUIDADO!)
docker system prune
```

### 3. Backup y Restauración
```bash
# Backup completo
./backup_system.sh

# Restaurar desde backup
./restore_system.sh backup_20250828.tar.gz
```

---

## ✅ Checklist de Configuración

### Pre-requisitos
- [x] Docker instalado
- [x] Docker Compose disponible
- [x] Puertos libres (8000, 3000, 5678, etc.)
- [x] Espacio en disco (mínimo 5GB)

### Configuración Base
- [x] Variables de entorno configuradas
- [x] Base de datos inicializada
- [x] Servicios ejecutándose
- [x] Health checks pasando

### Verificación Funcional
- [x] API respondiendo
- [x] Paper trading funcionando
- [x] Datos de Binance llegando
- [x] Sistema de aprendizaje activo
- [x] Dashboards accesibles

### Monitoreo
- [x] Logs configurados
- [x] Métricas recolectándose
- [x] Dashboards creados
- [x] Alertas configuradas

**🎉 Sistema completamente configurado y operativo!**

---

## 📞 Soporte de Configuración

**En caso de problemas:**
1. Verificar `docker-compose ps`
2. Revisar logs con `docker-compose logs -f`
3. Validar variables de entorno en `.env`
4. Comprobar conectividad de red
5. Reiniciar servicios problemáticos

**¡El sistema está listo para usar!** 🚀
