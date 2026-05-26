"""
DiME - Cargador de Datos de Contingencia (CSV a PostgreSQL)

Uso:
    python cargar_datos_contingencia.py

Requisitos:
    - PostgreSQL corriendo con la base maestra creada
    - Archivos CSV en ./data/raw/
"""

import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_MAESTRA_HOST", "localhost")
DB_PORT = os.getenv("DB_MAESTRA_PORT", "5432")
DB_USER = os.getenv("DB_MAESTRA_USER", "postgres")
DB_PASS = os.getenv("DB_MAESTRA_PASSWORD", "changeme")
DB_NAME = os.getenv("DB_MAESTRA_NAME", "dime_maestra")

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")
CLIENTES_CSV = os.path.join(DATA_DIR, "clientes_mock.csv")


def conectar_bd(db_name: str):
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=db_name,
        user=DB_USER, password=DB_PASS,
    )


def crear_bd_si_no_existe(conn, db_name: str):
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        if not cur.fetchone():
            cur.execute(f"CREATE DATABASE {db_name}")
            print(f"Base de datos '{db_name}' creada.")


def cargar_csv_a_tabla(conn, csv_path: str, tabla: str):
    if not os.path.exists(csv_path):
        print(f"Archivo no encontrado: {csv_path}")
        return
    df = pd.read_csv(csv_path)
    cols = list(df.columns)
    values = [tuple(row) for row in df.to_numpy()]
    query = f"INSERT INTO {tabla} ({','.join(cols)}) VALUES %s"
    with conn.cursor() as cur:
        execute_values(cur, query, values)
    conn.commit()
    print(f"Cargados {len(df)} registros en '{tabla}'.")


def main():
    conn_maestra = conectar_bd(DB_NAME)
    clientes_df = pd.read_csv(CLIENTES_CSV)

    for _, row in clientes_df.iterrows():
        db_name = row["db_name"]
        crear_bd_si_no_existe(conn_maestra, db_name)
        conn_cliente = conectar_bd(db_name)

        archivos = {
            "publicaciones_mock.csv": "metricas_publicaciones",
            "ventas_mock.csv": "metricas_costos",
            "reputacion_mock.csv": "metricas_reputacion",
            "envios_mock.csv": "metricas_envios",
            "stock_mock.csv": "metricas_stock",
        }

        for archivo, tabla in archivos.items():
            ruta = os.path.join(DATA_DIR, archivo)
            if os.path.exists(ruta):
                cargar_csv_a_tabla(conn_cliente, ruta, tabla)

        conn_cliente.close()

    conn_maestra.close()
    print("Carga de contingencia completada.")


if __name__ == "__main__":
    main()
