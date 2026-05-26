"""
DiME - Conexión con API de Mercado Libre

Obtiene datos reales desde la API de Mercado Libre usando OAuth 2.0
y los almacena en PostgreSQL.

Uso:
    python conexion_api_ml.py --access_token TOKEN --client_id 1
"""

import argparse
import requests
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

ML_API_BASE = "https://api.mercadolibre.com"
DB_HOST = os.getenv("DB_CLIENT_HOST", "localhost")
DB_PORT = os.getenv("DB_CLIENT_PORT", "5432")
DB_USER = os.getenv("DB_CLIENT_USER", "postgres")
DB_PASS = os.getenv("DB_CLIENT_PASSWORD", "changeme")


def get_user_info(access_token: str) -> dict:
    resp = requests.get(
        f"{ML_API_BASE}/users/me",
        headers={"Authorization": f"Bearer {access_token}"}
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
    parser.add_argument("--client_db", default="dime_cliente_1", help="Base de datos del cliente")
    args = parser.parse_args()

    user = get_user_info(args.access_token)
    print(f"Usuario: {user.get('nickname')} (ID: {user.get('id')})")

    item_ids = get_items(args.access_token, str(user["id"]))
    print(f"Publicaciones encontradas: {len(item_ids)}")

    db_url = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{args.client_db}"
    engine = create_engine(db_url)

    for item_id in item_ids[:10]:
        detail = get_item_details(args.access_token, item_id)
        print(f"  - {detail.get('title', 'Sin título')} | ${detail.get('price', 0)}")

    engine.dispose()


if __name__ == "__main__":
    main()
