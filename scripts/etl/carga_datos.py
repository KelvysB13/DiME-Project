import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent.parent / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")
RAIZ = Path(__file__).resolve().parent.parent.parent

# --- Carga de datos de clientes desde CSV a Base de Datos ---
def cargar_csvs():
    clientes = pd.read_csv(RAIZ / "data" / "raw" / "clientes_mock.csv")

    for _, row in clientes.iterrows():

        db_url = DATABASE_URL.rsplit("/", 1)[0] + f"/{row['db_name']}"
        engine = create_engine(db_url)

        archivos = [
            ("publicaciones_mock.csv", "metricas_publicaciones"),
            ("ventas_mock.csv", "metricas_costos"),
            ("reputacion_mock.csv", "metricas_reputacion"),
            ("envios_mock.csv", "metricas_envios"),
            ("stock_mock.csv", "metricas_stock"),
        ]

        for archivo, tabla in archivos:
            ruta = RAIZ / "data" / "raw" / archivo

            if ruta.exists():

                df = pd.read_csv(ruta)
                df.to_sql(tabla, engine, if_exists="append", index=False)
                print(f"Cargados {len(df)} registros en '{tabla}' ({row['db_name']})")

        engine.dispose()

    print("Carga completada.")

if __name__ == "__main__":
    cargar_csvs()