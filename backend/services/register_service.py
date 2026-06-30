import re
import unicodedata
from sqlalchemy.orm import Session
from models.vendedor_model import Vendedor
from schemas import RegisterRequest
from auth.password_handler import hash_password


class EmailAlreadyExistsError(Exception):
    pass


def _generate_user_name(nombre_tienda: str) -> str:
    name = unicodedata.normalize("NFKD", nombre_tienda)
    name = name.encode("ascii", "ignore").decode("ascii")
    name = re.sub(r"[^a-zA-Z0-9\s]", "", name)
    name = re.sub(r"\s+", "_", name.strip().lower())
    return name[:50]


def register(db: Session, payload: RegisterRequest) -> Vendedor:

    existing = db.query(Vendedor).filter(Vendedor.email == payload.email).first()

    if existing:
        raise EmailAlreadyExistsError()

    user_name = _generate_user_name(payload.nombre_tienda)

    base_name = user_name
    counter = 1
    while db.query(Vendedor).filter(Vendedor.user_name == user_name).first():
        suffix = f"_{counter}"
        user_name = f"{base_name[:50 - len(suffix)]}{suffix}"
        counter += 1

    vendedor = Vendedor(
        user_name=user_name,
        nombre_tienda=payload.nombre_tienda,
        email=payload.email,
        password=hash_password(payload.password.get_secret_value()),
        codigo_pais="MX",
        moneda_local="MXN",
        tipo_plan=1,
    )

    db.add(vendedor)
    db.commit()
    db.refresh(vendedor)

    return vendedor
