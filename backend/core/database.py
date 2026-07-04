from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine)
_client_engines = {}

#----- Conexión con Base de Datos (Maestra) -----
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

#----- Conexión con Base de Datos (Cliente) -----
def get_client_session(db_name: str):

    if db_name not in _client_engines:

        url = settings.database_url.rsplit("/", 1)[0] + f"/{db_name}"
        _client_engines[db_name] = create_engine(url, pool_pre_ping=True)

    return sessionmaker(bind=_client_engines[db_name])()
