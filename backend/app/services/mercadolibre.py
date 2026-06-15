from httpx import AsyncClient
from app.core.config import settings

ML_AUTH_URL = "https://auth.mercadolibre.com.ar/authorization"
ML_TOKEN_URL = "https://api.mercadolibre.com/oauth/token"

def get_login_url() -> str:
    return (
        f"{ML_AUTH_URL}?client_id={settings.ml_client_id}"
        f"&response_type=code&redirect_uri={settings.ml_redirect_uri}"
    )

async def exchange_code_for_token(code: str) -> dict:
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
