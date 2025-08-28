from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        case_sensitive=False,
        extra="ignore"  # Ignora variables extra como TZ
    )

    # Binance
    binance_api_key: str | None = None
    binance_api_secret: str | None = None
    binance_testnet: bool = True

    # Seguridad de órdenes
    trading_enabled: bool = False

    # Defaults
    default_symbol: str = "BTCUSDT"
    default_interval: str = "1h"

    # Rutas locales
    base_dir: Path = Path("/app")
    data_dir: Path = base_dir / "data"
    models_dir: Path = base_dir / "models"


settings = Settings()
