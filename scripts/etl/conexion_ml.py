import argparse
from pathlib import Path

import requests
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent.parent / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL no esta definida en el archivo .env")

# ML_API_BASE = "https://api.mercadolibre.com"
ML_API_BASE = "http://localhost:3001"

def get_vendedor(vendedor_id: str) -> dict:
    resp = requests.get(
        f"{ML_API_BASE}/users/vendedores",
        params={"id": vendedor_id}
    )
    resp.raise_for_status()
    return resp.json()


def get_items(access_token: str, user_id: str, limit: int = 50) -> list:
    resp = requests.get(
        f"{ML_API_BASE}/users/{user_id}/items/search",
        params={"limit": limit},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    resp.raise_for_status()
    return resp.json().get("results", [])


def get_item_details(access_token: str, item_id: str) -> dict:
    resp = requests.get(
        f"{ML_API_BASE}/items/{item_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    resp.raise_for_status()
    return resp.json()


def main():
    parser = argparse.ArgumentParser(description="Obtener datos de API Mercado Libre")
    parser.add_argument("--access_token", required=True, help="Token OAuth de ML")
    parser.add_argument("--vendedor_id", default="1", help="ID del vendedor (1-5 para el mock de Mockoon)")
    parser.add_argument("--client_db", default="dime_cliente_1", help="Base de datos del cliente")
    args = parser.parse_args()

    # --- Vendedor ---
    vendedor = get_vendedor(args.vendedor_id)

    datos_basicos = vendedor.get("datos_basicos")
    if not datos_basicos:
        print("Error: la respuesta de la API no contiene 'datos_basicos'")
        return

    id_vendedor = datos_basicos.get("id_vendedor")
    user_name = datos_basicos.get("user_name")
    if not id_vendedor or not user_name:
        print("Error: 'id_vendedor' o 'user_name' no encontrado en datos_basicos")
        return

    print(f"Vendedor: {user_name} (ID: {id_vendedor})")

    # --- Publicaciones (vienen dentro del JSON del vendedor) ---
    publicaciones = vendedor.get("publicaciones")
    if not publicaciones or not isinstance(publicaciones, list):
        print("Error: no se encontraron publicaciones en la respuesta")
        return

    print(f"Publicaciones encontradas: {len(publicaciones)}")
    for pub in publicaciones:
        item_id = pub.get("ml_item_id", "N/A")
        titulo = pub.get("titulo", "Sin titulo")
        id_pub = pub.get("id_publicacion", "N/A")
        print(f"  - [{id_pub}] {titulo} ({item_id})")

    # --- Conexion a base de datos (futura carga) ---
    db_url = DATABASE_URL.rsplit("/", 1)[0] + f"/{args.client_db}"
    engine = create_engine(db_url)
    print(f"Base de datos conectada: {args.client_db}")
    engine.dispose()


if __name__ == "__main__":
    main()
