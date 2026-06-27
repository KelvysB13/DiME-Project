from fastapi import APIRouter
from api.auth import router as auth_router
from api.dashboard import router as dashboard_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["Autenticacion"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
