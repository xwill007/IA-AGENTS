# 📡 API Reference - IA-AGENTS
## Documentación Completa de Endpoints Operativos

---

## ✅ Estado de la API

**Base URL:** http://localhost:8000  
**Documentación Interactiva:** http://localhost:8000/docs  
**Estado:** ✅ Completamente operativo  
**Versión:** 1.0.0  

---

## 🏥 Health & Status

### GET /api/health
**Descripción:** Verifica el estado del sistema  
**Status:** ✅ Operativo  

```bash
curl http://localhost:8000/api/health
```

**Respuesta:**
```json
{
  "status": "ok",
  "timestamp": "2025-08-28 12:21:21-05",
  "timezone": "America/Bogota (COT)"
}
```

### GET /
**Descripción:** Información básica de la API  

```bash
curl http://localhost:8000/
```

**Respuesta:**
```json
{
  "name": "IA-Agents Trading API",
  "version": "0.1.0"
}
```

---

## 📈 Trading Endpoints

### GET /api/trading/klines
**Descripción:** Obtiene datos de velas (candlesticks) de Binance  
**Status:** ✅ Operativo con datos reales  

**Parámetros:**
- `symbol` (string, opcional): Símbolo de trading (default: SOLUSDT)
- `interval` (string, opcional): Intervalo de tiempo (default: 1h)
- `limit` (int, opcional): Número de velas (10-1000, default: 500)

```bash
curl "http://localhost:8000/api/trading/klines?symbol=SOLUSDT&interval=1h&limit=100"
```

**Respuesta:**
```json
{
  "symbol": "SOLUSDT",
  "interval": "1h",
  "limit": 100,
  "rows": 100,
  "data": [
    {
      "timestamp": "2025-08-28T10:00:00",
      "open": 145.23,
      "high": 147.89,
      "low": 144.12,
      "close": 146.45,
      "volume": 1234567.89
    }
    // ... más velas
  ]
}
```

### GET /api/trading/features
**Descripción:** Obtiene características técnicas calculadas  

```bash
curl "http://localhost:8000/api/trading/features?symbol=SOLUSDT"
```

### GET /api/trading/signals
**Descripción:** Obtiene señales de trading generadas por IA  

```bash
curl "http://localhost:8000/api/trading/signals?symbol=SOLUSDT"
```

---

## 💰 Paper Trading (Trading Virtual)

### GET /api/paper-trading/portfolio
**Descripción:** Obtiene el estado actual del portafolio virtual  
**Status:** ✅ Operativo  

```bash
curl http://localhost:8000/api/paper-trading/portfolio
```

**Respuesta:**
```json
{
  "balance": 10000.0,
  "positions": [
    {
      "symbol": "SOLUSDT",
      "quantity": 10.0,
      "avg_price": 146.45,
      "current_price": 147.20,
      "pnl": 7.50,
      "pnl_percentage": 0.51
    }
  ],
  "total_value": 10007.50,
  "total_pnl": 7.50,
  "total_pnl_percentage": 0.075
}
```

### POST /api/paper-trading/order
**Descripción:** Coloca una orden de trading virtual  
**Status:** ✅ Operativo  

**Body:**
```json
{
  "symbol": "SOLUSDT",
  "side": "BUY",
  "quantity": 10.0,
  "order_type": "MARKET",
  "price": null
}
```

```bash
curl -X POST http://localhost:8000/api/paper-trading/order \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "SOLUSDT",
    "side": "BUY",
    "quantity": 10,
    "order_type": "MARKET"
  }'
```

**Respuesta:**
```json
{
  "order_id": "paper_order_123456789",
  "symbol": "SOLUSDT",
  "side": "BUY",
  "quantity": 10.0,
  "price": 146.45,
  "status": "FILLED",
  "timestamp": "2025-08-28T17:30:00Z",
  "commission": 0.146
}
```

### GET /api/paper-trading/orders
**Descripción:** Obtiene historial de órdenes  

```bash
curl http://localhost:8000/api/paper-trading/orders
```

### GET /api/paper-trading/performance
**Descripción:** Obtiene métricas de rendimiento  

```bash
curl http://localhost:8000/api/paper-trading/performance
```

### POST /api/paper-trading/reset
**Descripción:** Reinicia el portafolio virtual  

```bash
curl -X POST http://localhost:8000/api/paper-trading/reset \
  -H "Content-Type: application/json" \
  -d '{"new_balance": 10000.0}'
```

---

## 🧠 Learning System (Sistema de Aprendizaje)

### GET /api/learning/metrics
**Descripción:** Obtiene métricas del sistema de aprendizaje  
**Status:** ✅ Operativo  

```bash
curl http://localhost:8000/api/learning/metrics
```

**Respuesta:**
```json
{
  "total_trades": 25,
  "profitable_trades": 15,
  "win_rate": 0.60,
  "total_pnl": 125.75,
  "average_trade_pnl": 5.03,
  "confidence_score": 0.67,
  "learning_iterations": 10,
  "model_accuracy": 0.73
}
```

### POST /api/learning/train
**Descripción:** Entrena el modelo con nuevos datos  

```bash
curl -X POST http://localhost:8000/api/learning/train \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "SOLUSDT",
    "use_recent_data": true,
    "epochs": 10
  }'
```

### GET /api/learning/predictions
**Descripción:** Obtiene predicciones del modelo  

```bash
curl "http://localhost:8000/api/learning/predictions?symbol=SOLUSDT"
```

### POST /api/learning/feedback
**Descripción:** Proporciona feedback al sistema de aprendizaje  

```bash
curl -X POST http://localhost:8000/api/learning/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "trade_id": "paper_order_123456789",
    "actual_outcome": "profitable",
    "confidence": 0.8
  }'
```

---

## 📊 Logging & Monitoring

### GET /api/logs
**Descripción:** Obtiene logs del sistema  

```bash
curl "http://localhost:8000/api/logs?level=INFO&limit=100"
```

### GET /metrics
**Descripción:** Métricas de Prometheus (endpoint futuro)  

```bash
curl http://localhost:8000/metrics
```

---

## 🔍 Ejemplo de Flujo Completo

### 1. Verificar Sistema
```bash
curl http://localhost:8000/api/health
```

### 2. Ver Portafolio Inicial
```bash
curl http://localhost:8000/api/paper-trading/portfolio
```

### 3. Obtener Datos de Mercado
```bash
curl "http://localhost:8000/api/trading/klines?symbol=SOLUSDT&limit=10"
```

### 4. Realizar Trade Virtual
```bash
curl -X POST http://localhost:8000/api/paper-trading/order \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "SOLUSDT",
    "side": "BUY",
    "quantity": 5,
    "order_type": "MARKET"
  }'
```

### 5. Ver Resultados
```bash
curl http://localhost:8000/api/paper-trading/portfolio
```

### 6. Verificar Aprendizaje
```bash
curl http://localhost:8000/api/learning/metrics
```

---

## ⚠️ Códigos de Error

| Código | Descripción | Solución |
|--------|-------------|----------|
| **200** | ✅ Éxito | Todo funcionando correctamente |
| **404** | ❌ Endpoint no encontrado | Verificar URL y prefijo `/api/` |
| **422** | ❌ Error de validación | Revisar formato de datos enviados |
| **500** | ❌ Error interno | Revisar logs del servidor |

---

## 🚀 Testing Rápido

**Script de testing completo:**
```bash
#!/bin/bash
echo "🏥 Testing Health..."
curl -s http://localhost:8000/api/health | jq

echo "📊 Testing Portfolio..."
curl -s http://localhost:8000/api/paper-trading/portfolio | jq

echo "📈 Testing Market Data..."
curl -s "http://localhost:8000/api/trading/klines?symbol=SOLUSDT&limit=5" | jq '.rows'

echo "🧠 Testing Learning Metrics..."
curl -s http://localhost:8000/api/learning/metrics | jq

echo "✅ All tests completed!"
```

---

## 📞 Support

**Documentación interactiva:** http://localhost:8000/docs  
**Status de servicios:** `docker-compose ps`  
**Logs en vivo:** `docker-compose logs -f api`  

**¡La API está completamente operativa y lista para usar!** 🚀
