"""
DiME - Cargador de Datos de Contingencia (CSV a PostgreSQL)

Uso:
    python cargar_datos_contingencia.py

Requisitos:
    - PostgreSQL corriendo localmente
    - Archivos CSV en ./data/raw/
"""

import os
from pathlib import Path

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent.parent / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")
DB_MAESTRA_NAME = os.getenv("DB_MAESTRA_NAME", "dime_maestra")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL no esta definida en el archivo .env")

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")
CLIENTES_CSV = os.path.join(DATA_DIR, "clientes_mock.csv")


def conectar_bd(db_name: str):
    return psycopg2.connect(DATABASE_URL, dbname=db_name)


def crear_bd_si_no_existe(conn, db_name: str):
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        if not cur.fetchone():
            cur.execute(f"CREATE DATABASE {db_name} WITH OWNER dime_user")
            print(f"Base de datos '{db_name}' creada.")


def crear_tablas_si_no_existen(conn):
    statements = [
        """
        CREATE TABLE IF NOT EXISTS metricas_publicaciones (
            id_publicacion SERIAL PRIMARY KEY,
            titulo VARCHAR(500),
            puntaje_seo INT,
            fotos_calidad INT,
            atributos_completos INT,
            visitas INT,
            conversion DECIMAL(5, 2)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS metricas_reputacion (
            id SERIAL PRIMARY KEY,
            fecha DATE,
            insignia VARCHAR(100),
            reclamos INT,
            mediaciones INT,
            devoluciones INT,
            logistica_puntaje INT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS metricas_costos (
            id_venta SERIAL PRIMARY KEY,
            monto_bruto DECIMAL(10, 2),
            comision DECIMAL(10, 2),
            cargo_envio DECIMAL(10, 2),
            monto_neto DECIMAL(10, 2),
            margen_ganancia DECIMAL(5, 2)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS metricas_envios (
            id_venta SERIAL PRIMARY KEY,
            fecha_despacho DATE,
            fecha_entrega DATE,
            demora_dias INT,
            expuesto_penalizacion BOOLEAN
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS metricas_stock (
            sku VARCHAR(100) PRIMARY KEY,
            stock_total INT,
            stock_antiguo_dias INT,
            sobrestock_cargos DECIMAL(10, 2),
            calidad_puntaje INT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS diagnosticos (
            id_diagnostico SERIAL PRIMARY KEY,
            fecha DATE,
            area VARCHAR(100),
            problema TEXT,
            severidad VARCHAR(50),
            solucion_sugerida TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS planes_accion (
            id_accion SERIAL PRIMARY KEY,
            id_diagnostico INT REFERENCES diagnosticos(id_diagnostico),
            tarea TEXT,
            prioridad INT,
            completado BOOLEAN DEFAULT FALSE
        )
        """,
    ]
    with conn.cursor() as cur:
        for sql in statements:
            cur.execute(sql)
    conn.commit()


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
    conn_maestra = conectar_bd(DB_MAESTRA_NAME)
    clientes_df = pd.read_csv(CLIENTES_CSV)

    for _, row in clientes_df.iterrows():
        db_name = row["db_name"]
        crear_bd_si_no_existe(conn_maestra, db_name)
        conn_cliente = conectar_bd(db_name)
        crear_tablas_si_no_existen(conn_cliente)

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
