from datetime import datetime, timedelta, timezone
import hashlib
import jwt
from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config.settings import (
    KEY_TOKEN_PASSWORD, KEY_REFRESH_TOKEN, JWT_ALGORITHM,
    JWT_EXPIRATION_HOURS, JWT_REFRESH_EXPIRATION_DAYS,
    MAX_LOGIN_ATTEMPTS, LOGIN_LOCKOUT_MINUTES,
)

security_scheme = HTTPBearer(auto_error=False)


def create_access_token(
    user_id: str,
    role: str,
    email: str = "",
    name: str = "",
    expires_delta: timedelta | None = None,
) -> str:
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(hours=JWT_EXPIRATION_HOURS))
    payload = {
        "sub": str(user_id),
        "role": role,
        "email": email,
        "name": name,
        "type": "access",
        "iat": int(datetime.now(timezone.utc).timestamp()),
        "exp": int(expire.timestamp()),
    }
    return jwt.encode(payload, KEY_TOKEN_PASSWORD, algorithm=JWT_ALGORITHM)


def create_refresh_token(
    user_id: str,
    role: str,
    email: str = "",
    expires_delta: timedelta | None = None,
) -> str:
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=JWT_REFRESH_EXPIRATION_DAYS))
    payload = {
        "sub": str(user_id),
        "role": role,
        "email": email,
        "type": "refresh",
        "jti": hashlib.sha256(f"{user_id}:{datetime.now().timestamp()}".encode()).hexdigest()[:16],
        "iat": int(datetime.now(timezone.utc).timestamp()),
        "exp": int(expire.timestamp()),
    }
    return jwt.encode(payload, KEY_REFRESH_TOKEN or KEY_TOKEN_PASSWORD, algorithm=JWT_ALGORITHM)


def decode_token(token: str, secret: str | None = None) -> dict:
    return jwt.decode(
        token,
        secret or KEY_TOKEN_PASSWORD,
        algorithms=[JWT_ALGORITHM],
        options={"require": ["exp", "sub"]},
    )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security_scheme),
) -> dict:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token requerido")
    token = credentials.credentials
    try:
        payload = decode_token(token)
        if payload.get("type") == "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token de refresco no válido para esta operación")
        return {
            "id": payload["sub"],
            "role": payload.get("role", "user"),
            "email": payload.get("email", ""),
            "name": payload.get("name", ""),
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")


failed_attempts: dict[str, list[float]] = {}


async def login_rate_limit(request: Request):
    client_ip = request.client.host if request.client else "unknown"
    now = datetime.now().timestamp()
    if client_ip in failed_attempts:
        failed_attempts[client_ip] = [t for t in failed_attempts[client_ip] if now - t < LOGIN_LOCKOUT_MINUTES * 60]
        if len(failed_attempts[client_ip]) >= MAX_LOGIN_ATTEMPTS:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Demasiados intentos. Espere {LOGIN_LOCKOUT_MINUTES} minutos",
            )
