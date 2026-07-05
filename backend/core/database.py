import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings

os.environ.setdefault("PGPREFER_IP_VERSION", "4")

engine = create_engine(settings.supabase_url, pool_pre_ping=True, pool_size=5, max_overflow=10)
SessionLocal = sessionmaker(bind=engine)
_client_engines = {}

#----- Conexión con Base de Datos (Pooler Supabase) -----
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#----- Conexión con Base de Datos (Cliente) -----
def get_client_session(db_name: str):
    if db_name not in _client_engines:
        url = settings.supabase_url.rsplit("/", 1)[0] + f"/{db_name}"
        _client_engines[db_name] = create_engine(url, pool_pre_ping=True)
    return sessionmaker(bind=_client_engines[db_name])()