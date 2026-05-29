import os
import psycopg2
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent.parent / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

def get_maestra_connection():
    if not DATABASE_URL:
        raise ValueError(
            "DATABASE_URL no está definida en el archivo .env. "
            "Copia la cadena de conexión desde Supabase Dashboard -> Project Settings -> Database -> Connection string"
        )
    return psycopg2.connect(DATABASE_URL)

def get_client_connection(db_name: str):
    if not DATABASE_URL:
        raise ValueError(
            "DATABASE_URL no está definida en el archivo .env. "
            "Copia la cadena de conexión desde Supabase Dashboard -> Project Settings -> Database -> Connection string"
        )
    return psycopg2.connect(DATABASE_URL, dbname=db_name)

def get_db():
    conn = get_maestra_connection()
    try:
        yield conn
    finally:
        conn.close()
