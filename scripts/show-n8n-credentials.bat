@echo off
REM Script para mostrar credenciales de n8n desde .env
REM IA-AGENTS Trading Bot

echo 🔐 Credenciales de n8n (desde .env):
echo.

REM Leer variables del .env
for /f "tokens=1,2 delims==" %%a in ('findstr "N8N_ADMIN" .env') do (
    if "%%a"=="N8N_ADMIN_EMAIL" echo    Email: %%b
    if "%%a"=="N8N_ADMIN_FIRST_NAME" echo    First Name: %%b
    if "%%a"=="N8N_ADMIN_LAST_NAME" echo    Last Name: %%b
    if "%%a"=="N8N_ADMIN_PASSWORD" echo    Password: %%b
)

echo.
echo 📝 Instrucciones:
echo    1. Usa estos datos exactos en n8n
echo    2. Ve a: http://localhost:5678
echo    3. El email NO necesita ser real
echo    4. No hay verificación por email

echo.
echo ✅ Datos listos para usar en n8n

pause
