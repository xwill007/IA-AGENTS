@echo off
REM Script para configuración automática de n8n
REM IA-AGENTS Trading Bot

echo 🤖 IA-AGENTS: Configurando n8n automáticamente...

REM Esperar a que n8n esté disponible
echo ⏳ Esperando a que n8n esté disponible...
:WAIT_N8N
powershell -Command "try { Invoke-WebRequest -Uri 'http://localhost:5678' -TimeoutSec 5 | Out-Null; exit 0 } catch { exit 1 }"
if %ERRORLEVEL% NEQ 0 (
    timeout /t 2 /nobreak >nul
    goto WAIT_N8N
)

echo ✅ n8n está disponible

echo 📋 Workflows disponibles para importar manualmente:
echo    1. System Health Check (00-system-health-check.json)
echo    2. Market Monitor (01-market-monitor.json)
echo    3. Risk Management (02-risk-management.json)
echo    4. Strategy Orchestrator (03-strategy-orchestrator.json)

echo.
echo 📖 Instrucciones:
echo    1. Ve a http://localhost:5678
echo    2. Completa el registro de administrador
echo    3. Importa los workflows desde: n8n-workflows\
echo    4. Activa los workflows que necesites

echo.
echo 🔗 URLs importantes:
echo    n8n Dashboard: http://localhost:5678
echo    API IA-Agents: http://localhost:8000
echo    Ollama API: http://localhost:11434
echo    Grafana: http://localhost:3000

echo.
echo ✅ Configuración completada. ¡n8n está listo para usar!

pause
