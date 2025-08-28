# 🚀 Guía de Inicio Rápido - IA-AGENTS
## Sistema de Trading Inteligente Multi-Asistente

---

## ✅ Estado Actual
**Sistema completamente operativo desde:** 28 de Agosto, 2025  
**Versión:** 1.0.0  
**Estado:** ✅ Todos los servicios funcionando  

## 🎯 Lo que tienes listo para usar

### 📊 Panel de Control del Sistema
- **🚀 API Principal:** http://localhost:8000/docs
- **📈 Dashboard de Trading:** http://localhost:3000 (Grafana)
- **🔄 Automatización:** http://localhost:5678 (n8n)
- **📓 Análisis de Datos:** http://localhost:8888 (Jupyter)
- **📊 Métricas:** http://localhost:9090 (Prometheus)

---

## 🏃‍♂️ Primeros Pasos

### 1. Verificar que Todo Funciona (2 minutos)

```bash
# Verificar estado de todos los servicios
docker-compose ps

# Probar la API principal
curl http://localhost:8000/api/health
```

**Resultado esperado:** Deberías ver 8 contenedores ejecutándose y una respuesta JSON del health check.

### 2. Explorar la API (5 minutos)

1. **Abre tu navegador** en: http://localhost:8000/docs
2. **Explora los endpoints disponibles:**
   - `/api/health` - Estado del sistema
   - `/api/trading/klines` - Datos de mercado
   - `/api/paper-trading/portfolio` - Tu portafolio virtual
   - `/api/learning/metrics` - Métricas de aprendizaje

3. **Prueba tu primera consulta:**
   - Busca "GET /api/trading/klines"
   - Haz clic en "Try it out"
   - Cambia el símbolo a "SOLUSDT" si quieres
   - Haz clic en "Execute"

### 3. Tu Primer Trade Virtual (3 minutos)

**Realiza tu primer trade sin riesgo en el sistema de paper trading:**

```bash
# Ver tu portafolio inicial (deberías tener $10,000 virtuales)
curl http://localhost:8000/api/paper-trading/portfolio

# Realizar una orden de compra virtual (ejemplo)
curl -X POST http://localhost:8000/api/paper-trading/order \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "SOLUSDT",
    "side": "BUY",
    "quantity": 10,
    "order_type": "MARKET"
  }'
```

---

## 🎮 Funcionalidades Principales

### 💰 Paper Trading (Trading Virtual)
- **💵 Balance inicial:** $10,000 USD virtuales
- **📈 Trading sin riesgo:** Prueba estrategias sin perder dinero real
- **📊 Tracking en tiempo real:** Ve tus ganancias y pérdidas
- **🔄 Simulación realista:** Incluye slippage y comisiones

### 🧠 Sistema de Aprendizaje de IA
- **📚 Aprende automáticamente:** El sistema mejora con cada trade
- **📈 Optimización continua:** Ajusta parámetros según resultados
- **📊 Métricas detalladas:** Ve cómo mejora el rendimiento
- **🎯 Predicciones más precisas:** Cada trade hace al sistema más inteligente

### 👥 Multi-Agentes IA (En desarrollo)
- **👁️ Monitor de Mercado:** Vigila constantemente los precios
- **🔍 Analista Técnico:** Identifica patrones y señales
- **📰 Analista Fundamental:** Analiza noticias y eventos
- **⚠️ Gestor de Riesgo:** Protege tu capital
- **🎯 Estratega:** Decide las mejores operaciones
- **⚡ Ejecutor:** Realiza las órdenes automáticamente
- **🔍 Auditor:** Revisa y valida todas las decisiones

---

## 🎯 Casos de Uso Inmediatos

### Para Principiantes
1. **Explorar la API** → http://localhost:8000/docs
2. **Hacer paper trades** → Practica sin riesgo
3. **Ver dashboards** → http://localhost:3000
4. **Analizar en Jupyter** → http://localhost:8888

### Para Desarrolladores
1. **Crear workflows** → http://localhost:5678 (n8n)
2. **Configurar alertas** → Prometheus + Grafana
3. **Entrenar modelos** → Jupyter notebooks
4. **Personalizar estrategias** → Modificar código Python

### Para Traders
1. **Analizar mercados** → Datos en tiempo real de Binance
2. **Backtesting** → Probar estrategias con datos históricos
3. **Paper trading** → Validar estrategias sin riesgo
4. **Automatización** → Configurar trades automáticos

---

## 🛠️ Próximos Pasos Sugeridos

### Inmediatos (Hoy)
- [ ] **Configurar tu primer modelo de IA** en Ollama
- [ ] **Realizar 5-10 paper trades** para generar datos
- [ ] **Explorar los dashboards** en Grafana

### Esta Semana
- [ ] **Crear tu primer workflow** de trading automático en n8n
- [ ] **Personalizar parámetros** de learning en la configuración
- [ ] **Configurar alertas** para oportunidades de trading

### Este Mes
- [ ] **Entrenar modelos personalizados** con tus datos
- [ ] **Implementar estrategias avanzadas** de trading
- [ ] **Conectar datos externos** (noticias, redes sociales)

---

## 📞 Soporte y Configuración

### ⚙️ Configuración Actual
- **🔑 API Keys:** Configuradas para Binance Testnet (seguro)
- **💾 Base de Datos:** PostgreSQL con todas las tablas
- **🧠 IA Local:** Ollama listo para modelos
- **📊 Monitoreo:** Prometheus + Grafana configurados

### 🔧 Si Algo No Funciona
```bash
# Reiniciar todo el sistema
docker-compose down && docker-compose up -d

# Ver logs si hay problemas
docker-compose logs -f

# Verificar estado detallado
docker-compose ps
```

### 💡 Tips Importantes
- **🔒 Seguridad:** El sistema está en modo testnet (sin dinero real)
- **📈 Datos:** Se conecta a Binance testnet para datos reales
- **💾 Persistencia:** Todos los datos se guardan automáticamente
- **🔄 Backup:** Los volúmenes Docker preservan tu información

---

## 🎉 ¡Listo para Comenzar!

**Tu sistema IA-AGENTS está completamente operativo y listo para usar.**

1. **Abre:** http://localhost:8000/docs
2. **Explora:** Los endpoints disponibles
3. **Prueba:** Tu primer paper trade
4. **Disfruta:** Del trading automatizado inteligente

**¡Bienvenido al futuro del trading con IA!** 🚀🤖📈
