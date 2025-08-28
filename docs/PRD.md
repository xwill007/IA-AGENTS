# Documento de Requerimientos del Producto (PRD)
## Sistema de Trading Inteligente Multi-Asistente

### Información del Proyecto
- **Proyecto**: IA-AGENTS Trading Bot
- **Versión**: 1.0
- **Fecha**: Agosto 2025
- **Owner**: Wilber Vargas

---

## 1. Visión del Producto

### 1.1 Objetivo Principal
Desarrollar un sistema de trading automatizado que utiliza múltiples asistentes de IA especializados que colaboran, debaten y llegan a consensos para tomar decisiones de trading inteligentes y adaptativas.

### 1.2 Propuesta de Valor
- **Decisiones Colaborativas**: Múltiples perspectivas de IA reducen riesgos de decisiones unilaterales
- **Aprendizaje Continuo**: Los asistentes mejoran basándose en resultados y feedback del usuario
- **Transparencia**: Visibilidad completa del proceso de toma de decisiones
- **Flexibilidad**: Configuración personalizable de reglas y estrategias
- **Escalabilidad**: Arquitectura modular que permite agregar nuevos asistentes

---

## 2. Arquitectura del Sistema

### 2.1 Componentes Principales

#### **FastAPI Backend**
- Lógica de negocio principal
- APIs REST para configuración y monitoreo
- Gestión de datos y conexiones con exchanges
- Sistema de autenticación y autorización

#### **n8n Orchestrator**
- Coordinación de workflows entre asistentes
- Gestión de consensos y debates
- Automatización de procesos de trading
- Integración con sistemas externos

#### **Asistentes IA Especializados**
- Contenedores Docker independientes
- Modelos especializados por función
- Comunicación via APIs y webhooks
- Capacidad de aprendizaje autónomo

### 2.2 Asistentes Especializados

#### **Monitor de Mercado**
- **Función**: Vigilancia continua de mercados
- **Inputs**: Datos de precio, volumen, orderbook
- **Outputs**: Alertas de patrones, cambios significativos
- **Especialización**: Detección de oportunidades y anomalías

#### **Analista Técnico**
- **Función**: Análisis de indicadores técnicos
- **Inputs**: Datos históricos de precios, volúmenes
- **Outputs**: Señales de compra/venta, niveles de soporte/resistencia
- **Especialización**: Patrones de gráficos, indicadores matemáticos

#### **Analista Fundamental**
- **Función**: Análisis de noticias y eventos macro
- **Inputs**: Feeds de noticias, eventos económicos, métricas on-chain
- **Outputs**: Evaluación de impacto fundamental
- **Especialización**: Análisis de sentimiento, impacto de noticias

#### **Gestor de Riesgo**
- **Función**: Evaluación y gestión de riesgos
- **Inputs**: Portfolio actual, propuestas de trading
- **Outputs**: Aprobación/rechazo, límites recomendados
- **Especialización**: Cálculo de riesgos, gestión de exposición

#### **Estratega**
- **Función**: Creación y optimización de estrategias
- **Inputs**: Condiciones de mercado, histórico de performance
- **Outputs**: Estrategias adaptadas, ajustes de parámetros
- **Especialización**: Optimización de estrategias, backtesting

#### **Ejecutor**
- **Función**: Validación y ejecución de órdenes
- **Inputs**: Decisiones consensuadas, condiciones de mercado
- **Outputs**: Órdenes ejecutadas, confirmaciones
- **Especialización**: Timing de ejecución, slippage optimization

#### **Auditor**
- **Función**: Análisis post-mortem y aprendizaje
- **Inputs**: Resultados de trades, feedback del usuario
- **Outputs**: Lecciones aprendidas, recomendaciones de mejora
- **Especialización**: Análisis de performance, identificación de patrones

---

## 3. Flujo de Consenso

### 3.1 Proceso de Toma de Decisiones

#### **Fase 1: Detección**
1. Monitor de Mercado detecta oportunidad
2. Notifica a todos los asistentes relevantes
3. Se inicia workflow de análisis

#### **Fase 2: Análisis Inicial**
1. Analista Técnico evalúa señales
2. Analista Fundamental revisa contexto
3. Gestor de Riesgo analiza exposición actual

#### **Fase 3: Debate y Consenso**
1. **Ronda 1**: Cada asistente presenta su evaluación
2. **Ronda 2**: Asistentes debaten discrepancias
3. **Ronda 3**: Votación final y búsqueda de consenso

#### **Fase 4: Resolución**
- **Si hay consenso (mayoría)**: Estratega formula plan de acción
- **Si no hay consenso**: Se notifica al usuario con ambas alternativas
- **Usuario decide**: Aprueba, rechaza o modifica la propuesta

#### **Fase 5: Ejecución**
1. Ejecutor valida condiciones finales
2. Ejecuta la orden aprobada
3. Notifica resultados a todos los asistentes

#### **Fase 6: Aprendizaje**
1. Auditor monitorea resultados
2. Recopila feedback (automático y manual)
3. Actualiza modelos de asistentes relevantes

---

## 4. Sistema de Aprendizaje

### 4.1 Métricas de Evaluación

#### **Métricas Inmediatas**
- Precisión de señales de entrada/salida
- Tiempo de respuesta del sistema
- Consenso alcanzado vs rechazado

#### **Métricas a Corto Plazo (Diario)**
- ROI por trade
- Drawdown máximo
- Ratio de trades ganadores

#### **Métricas a Largo Plazo (Semanal/Mensual)**
- Sharpe Ratio
- Calmar Ratio
- Alpha vs benchmark

### 4.2 Retroalimentación

#### **Automática**
- Resultados de P&L inmediatos
- Métricas de performance calculadas
- Correlación entre predicciones y resultados

#### **Manual del Usuario**
- Rating de decisiones (1-5 estrellas)
- Comentarios sobre estrategias
- Ajustes de preferencias de riesgo

### 4.3 Reentrenamiento
- **Frecuencia**: Semanal por defecto (configurable)
- **Trigger**: Degradación de performance detectada
- **Proceso**: Reentrenamiento incremental con nuevos datos
- **Validación**: Backtesting antes de deployment

---

## 5. Configuración de Usuario

### 5.1 Pesos de Asistentes
```yaml
assistant_weights:
  monitor: 1.0
  technical_analyst: 1.2
  fundamental_analyst: 0.8
  risk_manager: 1.5
  strategist: 1.0
  executor: 1.0
  auditor: 0.5
```

### 5.2 Reglas Personalizadas
```yaml
custom_rules:
  max_position_size: 0.1  # 10% del portfolio
  max_daily_trades: 5
  blacklist_pairs: ["DOGE/USDT"]
  stop_loss_percentage: 0.02
  take_profit_percentage: 0.05
```

### 5.3 Templates de Estrategia

#### **Conservador**
- Bajo riesgo, señales fuertes únicamente
- Stop-loss estrictos
- Diversificación obligatoria

#### **Agresivo**
- Mayor tolerancia al riesgo
- Apalancamiento permitido
- Trades más frecuentes

#### **Swing Trading**
- Posiciones de medio plazo
- Análisis técnico prioritario
- Menor frecuencia de trades

#### **Scalping**
- Trades de muy corto plazo
- Análisis técnico de timeframes bajos
- Alta frecuencia de operaciones

---

## 6. Exchanges y Pares Soportados

### 6.1 Exchanges Inicial
- **Binance**: Exchange principal para testing
- **Extensible**: Arquitectura preparada para múltiples exchanges

### 6.2 Pares Iniciales
- SOL/USDT
- XRP/USDT
- COP/USDT
- **Configurables**: Fácil agregar/quitar pares

### 6.3 Datos Simultáneos
- Múltiples timeframes por par
- Datos en tiempo real via WebSocket
- Históricos para backtesting
- Orderbook depth para análisis avanzado

---

## 7. Requisitos No Funcionales

### 7.1 Performance
- Latencia máxima de decisión: 5 segundos
- Disponibilidad: 99.9%
- Throughput: 100 decisiones/minuto

### 7.2 Seguridad
- API Keys encriptadas
- Logs auditables
- Rate limiting
- Validación de parámetros

### 7.3 Monitoreo
- Health checks de todos los componentes
- Métricas de performance en tiempo real
- Alertas automáticas
- Dashboard de estado del sistema

---

## 8. Plan de Desarrollo por Fases

### **Fase 1: Fundamentos (4-6 semanas)**
- Setup de arquitectura Docker
- Asistentes básicos (Monitor, Técnico, Riesgo)
- Sistema de consenso simple
- Integración con Binance

### **Fase 2: Inteligencia (6-8 semanas)**
- Modelos de IA especializados
- Sistema de debate entre asistentes
- Aprendizaje básico
- Dashboard de monitoreo

### **Fase 3: Optimización (4-6 semanas)**
- Analista Fundamental con noticias
- Estratega con backtesting
- Sistema de retroalimentación completo
- Templates de estrategias

### **Fase 4: Escalabilidad (6-8 semanas)**
- Múltiples exchanges
- Auditor con análisis avanzado
- Configuración avanzada de usuario
- Optimizaciones de performance

---

## 9. Criterios de Éxito

### 9.1 Técnicos
- ✅ Sistema operativo 24/7 sin intervención
- ✅ Consenso alcanzado en >80% de decisiones
- ✅ Tiempo de respuesta <5 segundos promedio
- ✅ Todos los asistentes funcionando correctamente

### 9.2 De Negocio
- ✅ ROI positivo en testing durante 1 mes
- ✅ Sharpe ratio >1.5
- ✅ Drawdown máximo <10%
- ✅ Usuario satisfecho con transparencia de decisiones

### 9.3 De Usuario
- ✅ Interfaz intuitiva para configuración
- ✅ Visibilidad completa del proceso de decisión
- ✅ Capacidad de intervenir manualmente
- ✅ Feedback incorporado efectivamente

---

## 10. Riesgos y Mitigaciones

### 10.1 Riesgos Técnicos
- **Fallo de consenso frecuente**: Ajuste de algoritmo de votación
- **Latencia alta**: Optimización de comunicación entre servicios
- **Fallo de modelo de IA**: Fallback a reglas predeterminadas

### 10.2 Riesgos de Negocio
- **Pérdidas significativas**: Límites estrictos y stop-loss automáticos
- **Sobreoptimización**: Validación out-of-sample obligatoria
- **Deriva del modelo**: Monitoreo continuo de performance

### 10.3 Riesgos Operacionales
- **Fallo de exchange**: Múltiples exchanges y modo de emergencia
- **Problemas de conectividad**: Sistema de retry y queues
- **Pérdida de datos**: Backups automáticos y redundancia

---

*Este documento será actualizado conforme el proyecto evolucione.*
