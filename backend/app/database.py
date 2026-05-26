import psycopg2
from app.config import settings


def get_maestra_connection():
    return psycopg2.connect(
        host=settings.db_maestra_host,
        port=settings.db_maestra_port,
        dbname=settings.db_maestra_name,
        user=settings.db_maestra_user,
        password=settings.db_maestra_password,
    )


def get_client_connection(db_name: str):
    return psycopg2.connect(
        host=settings.db_client_host,
        port=settings.db_client_port,
        dbname=db_name,
        user=settings.db_client_user,
        password=settings.db_client_password,
    )


def get_db():
    conn = get_maestra_connection()
    try:
        yield conn
    finally:
        conn.close()
