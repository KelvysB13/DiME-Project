from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from core.config import settings

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    
    return jwt.encode(to_encode, settings.app_secret_key, algorithm=ALGORITHM)
