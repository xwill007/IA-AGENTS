# IA-AGENTS

API de trading con IA local (FastAPI) integrada con Binance y lista para ejecutarse en Docker.

## Requisitos
- Docker y Docker Compose
- Claves de API de Binance (usa testnet al inicio)

## Primeros pasos
1) Copia variables de entorno:

```bash
cp env.example .env
```

2) Edita `.env` y coloca tus claves de Binance. Mantén `BINANCE_TESTNET=true` y `TRADING_ENABLED=false` en desarrollo.

3) Levanta el servicio:

```bash
docker compose up --build -d
```

4) Abre la documentación interactiva:

`http://localhost:8000/docs`

## Endpoints principales
- GET `/api/health` – estado
- GET `/api/trading/klines` – descarga velas
- POST `/api/trading/train` – entrena un modelo simple local
- POST `/api/trading/predict` – predice señal en la última vela
- GET `/api/trading/backtest` – backtest rápido sobre histórico
- POST `/api/trading/order` – envía orden (por defecto test order)

## Estructura
- `app/` código de la API y servicios
- `data/` y `models/` se montan como volúmenes

## Advertencia
Esto es un ejemplo educativo. No es asesoría financiera. Opera bajo tu propio riesgo. Mantén `TRADING_ENABLED=false` hasta validar exhaustivamente.