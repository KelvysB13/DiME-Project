from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from config.settings import KEY_TOKEN_PASSWORD, JWT_ALGORITHM


def create_access_token(
    user_id: str,
    role: str,
    expires_delta: Optional[timedelta] = None,
) -> str:
    now_utc = datetime.now(timezone.utc)
    expire = now_utc + (expires_delta or timedelta(hours=1))
    payload = {
        "sub": str(user_id),
        "role": role,
        "iat": int(now_utc.timestamp()),
        "exp": int(expire.timestamp()),
    }
    token = jwt.encode(payload, KEY_TOKEN_PASSWORD, algorithm=JWT_ALGORITHM)
    return token if isinstance(token, str) else token.decode("utf-8")
