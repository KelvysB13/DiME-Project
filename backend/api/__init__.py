from fastapi import APIRouter
from api.auth_router import router as auth_router
from api.dashboard_router import router as dashboard_router
from api.personal_data_router import router as personal_data_router
from api.register_router import router as register_router
from api.diagnostico_router import router as diagnostico_router
from api.general_information_router import router as general_information_router
from api.account_deletion_router import router as account_deletion_router

api_router = APIRouter()
api_router.include_router(register_router, prefix="/auth", tags=["Autenticacion"])
api_router.include_router(auth_router, prefix="/auth", tags=["Autenticacion"])
api_router.include_router(dashboard_router, prefix="", tags=["Dashboard"])
api_router.include_router(personal_data_router, prefix="", tags=["Datos Personales"])
api_router.include_router(diagnostico_router, prefix="", tags=["Diagnostico"])
api_router.include_router(general_information_router, prefix="", tags=["Informacion General"])
api_router.include_router(account_deletion_router, prefix="", tags=["Cuenta"])
