# Guía de Configuración de n8n para IA-AGENTS

## 1. Configuración Inicial

### Paso 1: Completar el registro de administrador
En la pantalla que tienes abierta, usa los datos del archivo `.env`:

```
Email: admin@ia-agents.local
First Name: IA-Agents
Last Name: Admin
Password: iaAgents2024!
```

**Nota importante**: 
- ✅ El email NO necesita ser real (no hay verificación)
- ✅ n8n funciona completamente offline
- ✅ Estos datos están en tu `.env` para consistencia
- ✅ Puedes marcar "I want to receive security and product updates" sin problema

### Paso 2: Acceder al dashboard principal
Una vez completado el registro, accederás al dashboard principal de n8n.

## 2. Importar Workflows Pre-configurados

He creado 3 workflows principales que puedes importar:

### Workflow 1: Market Monitor (`01-market-monitor.json`)
- **Función**: Monitoreo continuo del mercado cada minuto
- **IA Integration**: Usa Ollama (llama3.1:8b) para análisis de mercado
- **Output**: Genera señales BUY/SELL basadas en análisis AI

### Workflow 2: Risk Management (`02-risk-management.json`)
- **Función**: Gestión de riesgos cada 5 minutos
- **IA Integration**: Análisis de riesgos con IA
- **Output**: Alertas de alto riesgo y ejecución automática de stop-loss

### Workflow 3: Strategy Orchestrator (`03-strategy-orchestrator.json`)
- **Función**: Orquestador maestro de estrategias
- **IA Integration**: IA estratega principal para decisiones finales
- **Output**: Ejecución de órdenes de paper trading

## 3. Pasos para Importar Workflows

### Método 1: Importar desde archivo
1. En n8n, haz clic en el botón **"+"** (New Workflow)
2. Selecciona **"Import from File"** o usa Ctrl+O
3. Selecciona uno de los archivos JSON de `n8n-workflows/`
4. El workflow se cargará automáticamente

### Método 2: Importar desde JSON
1. Crea un nuevo workflow
2. Haz clic en el menú "..." (Settings)
3. Selecciona "Import from JSON"
4. Copia y pega el contenido de cualquier archivo .json

## 4. Configuraciones Necesarias

### Verificar Conectividad
Antes de activar los workflows, verifica que n8n puede conectarse a:

1. **API FastAPI**: `http://api:8000` (dentro del contenedor)
2. **Ollama**: `http://ollama:11434` (dentro del contenedor)

### Configurar Credenciales (si es necesario)
- Los workflows están configurados para usar las URLs internas de Docker
- No necesitas credenciales adicionales para las conexiones internas

## 5. Activar y Probar Workflows

### Activar Workflows
1. Abre cada workflow importado
2. Haz clic en el toggle "Active" en la esquina superior derecha
3. El workflow comenzará a ejecutarse según su programación

### Probar Manualmente
1. En cualquier workflow, haz clic en "Test workflow"
2. Observa la ejecución en tiempo real
3. Verifica que no hay errores en los nodos

## 6. Monitoreo de Ejecuciones

### Dashboard de Ejecuciones
- Ve a "Executions" en el menú lateral
- Observa el historial de ejecuciones
- Verifica éxitos y errores

### Logs y Debugging
- Cada nodo muestra su output en tiempo real
- Los errores se muestran en rojo
- Puedes inspeccionar los datos que fluyen entre nodos

## 7. URLs de Webhooks (para integración)

Una vez que actives el **Strategy Orchestrator**, tendrás disponible:

```
Webhook URL: http://localhost:5678/webhook/strategy-trigger
```

Esta URL puede ser usada por otros servicios para enviar datos y activar decisiones de trading.

## 8. Próximos Pasos

### Personalización
1. Ajusta los intervalos de tiempo según tus necesidades
2. Modifica los prompts de IA para mejorar el análisis
3. Añade más condiciones y filtros

### Expansión
1. Crea workflows adicionales para análisis fundamental
2. Integra más fuentes de datos
3. Añade notificaciones (email, Slack, Discord)

### Monitoreo Avanzado
1. Configura alertas para errores
2. Integra con Prometheus para métricas
3. Crea dashboards personalizados en Grafana

## ¡Configuración Completada!

Una vez que hayas seguido estos pasos, tendrás un sistema completo de trading con IA funcionando con:

- ✅ Monitoreo automático de mercado
- ✅ Gestión de riesgos con IA
- ✅ Estrategia orquestada por IA
- ✅ Paper trading automático
- ✅ Sistema de aprendizaje integrado

¿Necesitas ayuda con algún paso específico? ¡Pregunta!
