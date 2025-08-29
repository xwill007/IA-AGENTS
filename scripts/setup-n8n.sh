#!/bin/bash

# Script para configuración automática de n8n
# IA-AGENTS Trading Bot

echo "🤖 IA-AGENTS: Configurando n8n automáticamente..."

# Esperar a que n8n esté disponible
echo "⏳ Esperando a que n8n esté disponible..."
while ! curl -s http://localhost:5678 > /dev/null 2>&1; do
    sleep 2
done

echo "✅ n8n está disponible"

# URLs de los workflows
BASE_URL="http://localhost:5678"
WORKFLOWS_DIR="./n8n-workflows"

echo "📦 Importando workflows..."

# Función para importar workflow
import_workflow() {
    local file=$1
    local name=$2
    
    echo "   Importando: $name"
    
    # Aquí iría la lógica para importar via API de n8n
    # Nota: n8n requiere autenticación para la API, por lo que 
    # los workflows deben importarse manualmente por ahora
}

echo "📋 Workflows disponibles para importar manualmente:"
echo "   1. System Health Check (00-system-health-check.json)"
echo "   2. Market Monitor (01-market-monitor.json)"
echo "   3. Risk Management (02-risk-management.json)"
echo "   4. Strategy Orchestrator (03-strategy-orchestrator.json)"

echo ""
echo "📖 Instrucciones:"
echo "   1. Ve a http://localhost:5678"
echo "   2. Completa el registro de administrador"
echo "   3. Importa los workflows desde: $WORKFLOWS_DIR"
echo "   4. Activa los workflows que necesites"

echo ""
echo "🔗 URLs importantes:"
echo "   n8n Dashboard: http://localhost:5678"
echo "   API IA-Agents: http://localhost:8000"
echo "   Ollama API: http://localhost:11434"
echo "   Grafana: http://localhost:3000"

echo ""
echo "✅ Configuración completada. ¡n8n está listo para usar!"
