"""
Módulo de Configuración Global del Sistema.
Carga y valida las variables de entorno requeridas.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:password@localhost:5432/dbname")
SCHEMA = os.getenv("SCHEMA", "public")
APP_TITLE = os.getenv("APP_TITLE", "FastAPI App")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
MAX_REQUEST_SIZE = int(os.getenv("MAX_REQUEST_SIZE", str(10 * 1024 * 1024)))
DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "10"))
DB_MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "20"))
DB_POOL_TIMEOUT = int(os.getenv("DB_POOL_TIMEOUT", "30"))
DB_POOL_RECYCLE = int(os.getenv("DB_POOL_RECYCLE", "1800"))
PASSWORD_MIN_LENGTH = int(os.getenv("PASSWORD_MIN_LENGTH", "8"))
MAX_LOGIN_ATTEMPTS = int(os.getenv("MAX_LOGIN_ATTEMPTS", "5"))
LOGIN_LOCKOUT_MINUTES = int(os.getenv("LOGIN_LOCKOUT_MINUTES", "15"))
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", "1"))
JWT_REFRESH_EXPIRATION_DAYS = int(os.getenv("JWT_REFRESH_EXPIRATION_DAYS", "7"))

KEY_TOKEN_PASSWORD: str = os.getenv("KEY_TOKEN_PASSWORD", "")
if not KEY_TOKEN_PASSWORD or KEY_TOKEN_PASSWORD.strip() == "":
    raise ValueError(
        "CRITICAL: La variable 'KEY_TOKEN_PASSWORD' no está configurada en el archivo .env"
    )

KEY_REFRESH_TOKEN: str = os.getenv("KEY_REFRESH_TOKEN", "")

KEY_TOKEN_PASSWORD_BYTES = KEY_TOKEN_PASSWORD.encode("utf-8")
if len(KEY_TOKEN_PASSWORD) < 32:
    raise ValueError(
        "CRITICAL: 'KEY_TOKEN_PASSWORD' debe tener al menos 32 caracteres."
    )

from domain.enums.user_role import UserRole
ALLOWED_ROLES = {member.value for member in UserRole}
