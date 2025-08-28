from datetime import datetime
import pytz
from fastapi import APIRouter


router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    # Zona horaria de Bogotá
    bogota_tz = pytz.timezone('America/Bogota')
    now_bogota = datetime.now(bogota_tz)
    
    return {
        "status": "ok",
        "timestamp": now_bogota.strftime("%Y-%m-%d %H:%M:%S %Z"),
        "timezone": "America/Bogota (COT)"
    }



