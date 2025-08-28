# Historias de Usuario y Criterios de Aceptación
## Sistema de Trading Inteligente Multi-Asistente

---

## Epic 1: Sistema de Asistentes IA

### Historia de Usuario 1.1: Creación de Asistentes Especializados
**Como** desarrollador del sistema  
**Quiero** que cada asistente tenga una especialización clara y definida  
**Para** que puedan aportar valor específico en el proceso de trading  

#### Criterios de Aceptación:
- [ ] Monitor de Mercado detecta cambios >3% en precio en ventanas de 15min
- [ ] Analista Técnico calcula al menos 10 indicadores técnicos estándar
- [ ] Analista Fundamental procesa feeds de noticias cada 5 minutos
- [ ] Gestor de Riesgo valida que ningún trade exceda 10% del portfolio
- [ ] Estratega mantiene biblioteca de al menos 5 estrategias base
- [ ] Ejecutor puede ejecutar órdenes market y limit en <2 segundos
- [ ] Auditor genera reportes de performance cada 24 horas

### Historia de Usuario 1.2: Comunicación entre Asistentes
**Como** sistema de trading  
**Quiero** que los asistentes se comuniquen de forma estructurada  
**Para** que puedan colaborar efectivamente en las decisiones  

#### Criterios de Aceptación:
- [ ] Protocolo de mensajería JSON definido entre asistentes
- [ ] Cada asistente puede enviar y recibir mensajes via n8n
- [ ] Log completo de todas las comunicaciones
- [ ] Timeout de 30 segundos para respuestas entre asistentes
- [ ] Sistema de retry automático en caso de fallo de comunicación

---

## Epic 2: Sistema de Consenso y Debate

### Historia de Usuario 2.1: Proceso de Debate
**Como** usuario del sistema  
**Quiero** que los asistentes puedan debatir entre ellos  
**Para** que las decisiones sean más robustas y consideradas  

#### Criterios de Aceptación:
- [ ] **Ronda 1**: Cada asistente presenta su análisis en <60 segundos
- [ ] **Ronda 2**: Asistentes pueden cuestionar análisis de otros con argumentos
- [ ] **Ronda 3**: Votación final con justificación de cada voto
- [ ] Máximo 3 rondas de debate por decisión
- [ ] Log completo del debate accesible para review
- [ ] Timestamp de cada intervención en el debate

### Historia de Usuario 2.2: Sistema de Consenso
**Como** usuario del sistema  
**Quiero** que se tome una decisión clara basada en mayoría  
**Para** que el sistema pueda actuar de forma determinística  

#### Criterios de Aceptación:
- [ ] Consenso se alcanza con >50% de votos a favor
- [ ] Pesos configurables por asistente (default 1.0 para todos)
- [ ] En caso de empate, se escala al usuario
- [ ] Decisión final documentada con reasoning de cada asistente
- [ ] Tiempo máximo total de consenso: 5 minutos

### Historia de Usuario 2.3: Escalación al Usuario
**Como** trader  
**Quiero** ser notificado cuando no hay consenso  
**Para** que pueda tomar la decisión final manualmente  

#### Criterios de Aceptación:
- [ ] Notificación inmediata via dashboard cuando no hay consenso
- [ ] Presentación clara de ambas alternativas principales
- [ ] Argumentos de cada posición mostrados de forma comprensible
- [ ] Usuario puede aprobar, rechazar o modificar propuesta
- [ ] Timeout de 15 minutos para decisión del usuario
- [ ] Si no hay respuesta del usuario, se mantiene status quo

---

## Epic 3: Sistema de Aprendizaje

### Historia de Usuario 3.1: Retroalimentación Automática
**Como** sistema de trading  
**Quiero** aprender automáticamente de los resultados  
**Para** que mejore mi performance con el tiempo  

#### Criterios de Aceptación:
- [ ] P&L de cada trade registrado y asociado a decisión original
- [ ] Métricas calculadas automáticamente (ROI, Sharpe, etc.)
- [ ] Correlación entre predicciones y resultados medida
- [ ] Base de datos de decisiones y outcomes mantenida
- [ ] Alertas cuando performance degrada significativamente

### Historia de Usuario 3.2: Retroalimentación Manual del Usuario
**Como** trader  
**Quiero** poder calificar las decisiones del sistema  
**Para** que aprenda mis preferencias y mejore según mi estilo  

#### Criterios de Aceptación:
- [ ] Interface para rating de decisiones (1-5 estrellas)
- [ ] Campo de comentarios para feedback cualitativo
- [ ] Rating puede hacerse durante o después del trade
- [ ] Historial de ratings accesible y searchable
- [ ] Sistema peso rating del usuario en futuras decisiones

### Historia de Usuario 3.3: Reentrenamiento de Modelos
**Como** sistema de trading  
**Quiero** que los modelos se actualicen periódicamente  
**Para** que se adapten a cambios en el mercado  

#### Criterios de Aceptación:
- [ ] Reentrenamiento automático semanal por default
- [ ] Usuario puede configurar frecuencia (diario, semanal, mensual)
- [ ] Usuario puede desactivar reentrenamiento automático
- [ ] Validación de modelos nuevos antes de deployment
- [ ] Rollback automático si performance degrada post-reentrenamiento
- [ ] Notificación al usuario cuando ocurre reentrenamiento

---

## Epic 4: Configuración y Personalización

### Historia de Usuario 4.1: Ajuste de Pesos de Asistentes
**Como** trader  
**Quiero** poder ajustar la influencia de cada asistente  
**Para** que el sistema refleje mis preferencias de trading  

#### Criterios de Aceptación:
- [ ] Interface para ajustar peso de cada asistente (0.1 - 2.0)
- [ ] Cambios de peso aplicados inmediatamente
- [ ] Presets predefinidos (Conservador, Agresivo, Balanceado)
- [ ] Validación que suma de pesos sea coherente
- [ ] Historial de cambios de configuración mantenido

### Historia de Usuario 4.2: Reglas Personalizadas
**Como** trader  
**Quiero** poder definir reglas que el sistema debe respetar  
**Para** que opere dentro de mis límites de riesgo y preferencias  

#### Criterios de Aceptación:
- [ ] Configuración de límites máximos (posición, drawdown, trades/día)
- [ ] Lista negra de pares de trading
- [ ] Horarios de trading permitidos
- [ ] Stop-loss y take-profit automáticos configurables
- [ ] Validación de reglas antes de cada trade
- [ ] Override manual de reglas con confirmación explícita

### Historia de Usuario 4.3: Templates de Estrategia
**Como** trader nuevo  
**Quiero** poder elegir entre estrategias predefinidas  
**Para** que pueda empezar a usar el sistema sin configuración compleja  

#### Criterios de Aceptación:
- [ ] Al menos 4 templates: Conservador, Agresivo, Swing, Scalping
- [ ] Cada template configura pesos, reglas y parámetros automáticamente
- [ ] Descripción clara de cada estrategia y su perfil de riesgo
- [ ] Usuario puede modificar template después de aplicarlo
- [ ] Posibilidad de guardar configuración actual como template custom

---

## Epic 5: Integración con Exchanges

### Historia de Usuario 5.1: Configuración de Exchange
**Como** trader  
**Quiero** configurar mis credenciales de exchange de forma segura  
**Para** que el sistema pueda operar en mi cuenta  

#### Criterios de Aceptación:
- [ ] Interface segura para API keys (no mostrar claves en texto plano)
- [ ] Validación de credenciales antes de guardar
- [ ] Soporte para testnet y mainnet de Binance
- [ ] Encriptación de credenciales en base de datos
- [ ] Test de conexión automático cada hora

### Historia de Usuario 5.2: Gestión de Pares de Trading
**Como** trader  
**Quiero** poder seleccionar qué pares quiero tradear  
**Para** que el sistema se enfoque en mis mercados de interés  

#### Criterios de Aceptación:
- [ ] Lista inicial: SOL/USDT, XRP/USDT, COP/USDT
- [ ] Interface para agregar/quitar pares
- [ ] Validación que el par existe en el exchange
- [ ] Configuración individual por par (límites, estrategia)
- [ ] Posibilidad de pausar trading en pares específicos

### Historia de Usuario 5.3: Monitoreo de Datos de Mercado
**Como** sistema de trading  
**Quiero** recibir datos de mercado en tiempo real  
**Para** que pueda tomar decisiones basadas en información actual  

#### Criterios de Aceptación:
- [ ] WebSocket connection para datos en tiempo real
- [ ] Múltiples timeframes simultáneos (1m, 5m, 15m, 1h, 4h, 1d)
- [ ] Backup via REST API si WebSocket falla
- [ ] Buffer de datos para análisis histórico
- [ ] Alertas si hay pérdida de datos por >1 minuto

---

## Epic 6: Dashboard y Monitoreo

### Historia de Usuario 6.1: Dashboard en Tiempo Real
**Como** trader  
**Quiero** ver el estado del sistema en tiempo real  
**Para** que pueda monitorear su funcionamiento y performance  

#### Criterios de Aceptación:
- [ ] Estado de cada asistente (activo, error, procesando)
- [ ] Últimas decisiones tomadas con timestamp
- [ ] P&L en tiempo real del portfolio
- [ ] Gráficos de performance (ROI, drawdown)
- [ ] Log de actividad reciente
- [ ] Indicadores de salud del sistema

### Historia de Usuario 6.2: Visualización de Debates
**Como** trader  
**Quiero** ver cómo los asistentes llegaron a una decisión  
**Para** que pueda entender y confiar en el proceso  

#### Criterios de Aceptación:
- [ ] Timeline visual del proceso de debate
- [ ] Argumentos de cada asistente mostrados claramente
- [ ] Votos finales y reasoning highlighted
- [ ] Posibilidad de expandir/colapsar detalles
- [ ] Búsqueda y filtrado de debates históricos

### Historia de Usuario 6.3: Reportes de Performance
**Como** trader  
**Quiero** recibir reportes periódicos de performance  
**Para** que pueda evaluar si el sistema está cumpliendo mis objetivos  

#### Criterios de Aceptación:
- [ ] Reporte diario automático con métricas clave
- [ ] Reporte semanal con análisis más profundo
- [ ] Reporte mensual con comparación vs benchmarks
- [ ] Exportación de reportes en PDF y CSV
- [ ] Configuración de frecuencia y contenido de reportes

---

## Epic 7: Gestión de Riesgos y Seguridad

### Historia de Usuario 7.1: Límites de Riesgo Automáticos
**Como** trader  
**Quiero** que el sistema respete límites de riesgo estrictos  
**Para** que no pueda perder más de lo que estoy dispuesto  

#### Criterios de Aceptación:
- [ ] Stop-loss automático en todas las posiciones
- [ ] Límite máximo de exposición por trade (% del portfolio)
- [ ] Límite de drawdown máximo (pausar trading si se alcanza)
- [ ] Límite de trades por día/semana
- [ ] Circuit breaker en caso de pérdidas excepcionales

### Historia de Usuario 7.2: Modo de Emergencia
**Como** trader  
**Quiero** poder parar el sistema inmediatamente  
**Para** que pueda intervenir en situaciones de emergencia  

#### Criterios de Aceptación:
- [ ] Botón de "PARAR TODO" prominente en dashboard
- [ ] Cierre de todas las posiciones abiertas opcional
- [ ] Cancelación de órdenes pendientes
- [ ] Pausa de nuevos trades hasta reactivación manual
- [ ] Log detallado de activación de modo emergencia

### Historia de Usuario 7.3: Auditabilidad Completa
**Como** usuario responsable  
**Quiero** que todas las acciones sean auditables  
**Para** que pueda cumplir con regulaciones y entender el comportamiento del sistema  

#### Criterios de Aceptación:
- [ ] Log de todas las decisiones con timestamp y reasoning
- [ ] Registro de todas las comunicaciones entre asistentes
- [ ] Historial de cambios de configuración
- [ ] Registro de todas las órdenes ejecutadas
- [ ] Backup diario de logs y base de datos
- [ ] Retención de logs por al menos 1 año

---

## Definición de Terminado (Definition of Done)

Para que una historia de usuario se considere completada, debe cumplir:

### Desarrollo:
- [ ] Código implementado y testeado unitariamente
- [ ] Integración con n8n workflows funcional
- [ ] Documentación técnica actualizada
- [ ] Code review aprobado por al menos 1 revisor

### Testing:
- [ ] Tests unitarios con >80% cobertura
- [ ] Tests de integración pasando
- [ ] Testing manual de casos felices y edge cases
- [ ] Performance testing si aplica

### Deploy:
- [ ] Deployable via Docker Compose
- [ ] Variables de entorno documentadas
- [ ] Health checks implementados
- [ ] Rollback plan documentado

### Usuario:
- [ ] UI/UX review completado
- [ ] Documentación de usuario actualizada
- [ ] Training materials creados si es necesario
- [ ] Feedback del usuario incorporado

---

*Este documento será actualizado conforme se completen las historias y se identifiquen nuevos requerimientos.*
