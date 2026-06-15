from fastapi import APIRouter
from app.services.mercadolibre import get_login_url, exchange_code_for_token

router = APIRouter()

@router.get("/ml/login")
async def ml_login():
    return {"auth_url": get_login_url()}

@router.get("/ml/callback")
async def ml_callback(code: str):
    return await exchange_code_for_token(code)
