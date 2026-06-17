from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter(tags=["health"])


@router.get("/health", summary="Health check")
def health_check():
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "1.0.0",
    }


@router.get("/health/integration", tags=["Monitoreo"])
async def health_integration():
    components = {
        "api": "up",
        "rate_limiter": "active",
    }
    return {"status": "ok", "components": components}
