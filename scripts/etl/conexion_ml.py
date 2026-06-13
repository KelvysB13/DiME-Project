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

    db_url = DATABASE_URL.rsplit("/", 1)[0] + f"/{args.client_db}"
    engine = create_engine(db_url)

    for item_id in item_ids[:10]:
        detail = get_item_details(args.access_token, item_id)
        print(f"  - {detail.get('title', 'Sin titulo')} | ${detail.get('price', 0)}")

    engine.dispose()


if __name__ == "__main__":
    main()
