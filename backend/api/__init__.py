from fastapi import APIRouter
from api.auth_router import router as auth_router
from api.dashboard_router import router as dashboard_router
from api.personal_data_router import router as personal_data_router
from api.register_router import router as register_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["Autenticacion"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(personal_data_router, prefix="/auth", tags=["Autenticacion"])
api_router.include_router(register_router, prefix="/auth", tags=["Autenticacion"])
