#!/usr/bin/env python3
"""Genera un token JWT para probar endpoints protegidos.

Uso:
    python gen_token.py <id_vendedor>
    python gen_token.py 1

Por defecto genera token para el vendedor 1.
"""
import sys
from datetime import datetime, timedelta, timezone

try:
    import jwt
except ImportError:
    print("Error: ejecutá 'pip install pyjwt'")
    sys.exit(1)

SECRET_KEY = "supersecretkey_DiME_2026_change_in_production"
ALGORITHM = "HS256"
EXPIRATION_HOURS = 2

vendedor_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1

payload = {
    "sub": str(vendedor_id),
    "exp": datetime.now(timezone.utc) + timedelta(hours=EXPIRATION_HOURS),
}

token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
print(token)
