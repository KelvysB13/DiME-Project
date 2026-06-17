import jwt
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from config.settings import KEY_TOKEN_PASSWORD_BYTES, JWT_ALGORITHM


EXCLUDED_PATHS = {"/", "/dashboard", "/docs", "/openapi.json", "/favicon.ico", "/auth/login", "/auth/register", "/docs/oauth-redirect", "/health", "/health/integration"}


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in EXCLUDED_PATHS:
            return await call_next(request)

        if request.url.path.startswith(("/auth/", "/health", "/assets/", "/views/")):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Token de autenticación requerido", "code": "AUTH_REQUIRED"}
            )

        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(
                token,
                KEY_TOKEN_PASSWORD_BYTES,
                algorithms=[JWT_ALGORITHM],
                options={"require": ["exp", "sub", "role"]}
            )
            request.state.user = {
                "id": payload["sub"],
                "role": payload["role"],
                "email": payload.get("email", ""),
                "name": payload.get("name", ""),
            }
        except jwt.ExpiredSignatureError:
            return JSONResponse(
                status_code=401,
                content={"detail": "El token ha expirado", "code": "TOKEN_EXPIRED"}
            )
        except jwt.InvalidTokenError:
            return JSONResponse(
                status_code=401,
                content={"detail": "Token inválido o manipulado", "code": "INVALID_TOKEN"}
            )

        response = await call_next(request)
        return response
