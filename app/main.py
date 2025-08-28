from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routers.health import router as health_router
from app.api.routers.trading import router as trading_router


app = FastAPI(title="IA-Agents Trading API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    # Crear carpetas locales si no existen
    for path in [settings.data_dir, settings.models_dir]:
        path.mkdir(parents=True, exist_ok=True)


app.include_router(health_router, prefix="/api")
app.include_router(trading_router, prefix="/api")


@app.get("/")
def root():
    return {"name": app.title, "version": app.version}
