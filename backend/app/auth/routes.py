from fastapi import APIRouter, Request
from httpx import AsyncClient
from app.config import settings

router = APIRouter()

ML_AUTH_URL = "https://auth.mercadolibre.com.ar/authorization"
ML_TOKEN_URL = "https://api.mercadolibre.com/oauth/token"


@router.get("/ml/login")
async def ml_login():
    params = {
        "client_id": settings.ml_client_id,
        "response_type": "code",
        "redirect_uri": settings.ml_redirect_uri,
    }
    url = f"{ML_AUTH_URL}?client_id={params['client_id']}&response_type=code&redirect_uri={params['redirect_uri']}"
    return {"auth_url": url}


@router.get("/ml/callback")
async def ml_callback(code: str):
    async with AsyncClient() as client:
        data = {
            "grant_type": "authorization_code",
            "client_id": settings.ml_client_id,
            "client_secret": settings.ml_client_secret,
            "code": code,
            "redirect_uri": settings.ml_redirect_uri,
        }
        resp = await client.post(ML_TOKEN_URL, data=data)
        return resp.json()
