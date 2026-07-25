import time
import jwt
from core.config import settings

ALGORITHM = "HS256"

# ID numérico de cada dashboard en Metabase (Admin -> dashboard -> URL).
METABASE_DASHBOARD_IDS = {
    "reputacion": 2,
    "ventas": 3,
    "calidad": 4,
    "inventario": 5,
    "publicidad": 6,
}


def _build_embed_url(dashboard_id: int, id_vendedor: int) -> str:
    payload = {
        "resource": {"dashboard": dashboard_id},
        "params": {"n%C3%BAmero": id_vendedor},
        "exp": round(time.time()) + (10 * 60),
    }
    token = jwt.encode(payload, settings.metabase_embedding_secret, algorithm=ALGORITHM)
    base = settings.metabase_url.rstrip("/")
    return f"{base}/embed/dashboard/{token}#bordered=true&titled=true&theme=night"


def get_diagnostico_embed_urls(id_vendedor: int) -> dict:
    return {
        key: _build_embed_url(dashboard_id, id_vendedor)
        for key, dashboard_id in METABASE_DASHBOARD_IDS.items()
    }
