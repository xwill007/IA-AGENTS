@echo off
echo Starting IA-AGENTS containers...

REM Check if .env file exists
if not exist .env (
    echo ERROR: .env file not found. Please create it from env.example
    pause
    exit /b 1
)

REM Start all containers
docker-compose up -d

echo.
echo Containers are starting up. You can access the services at:
echo - n8n: http://localhost:5678
echo - FastAPI docs: http://localhost:8000/docs
echo - Grafana: http://localhost:3000
echo - Jupyter Notebook: http://localhost:8888
echo.
echo To check container status, run: docker ps
echo To view logs, run: docker-compose logs -f
echo To stop containers, run: docker-compose down

pause
