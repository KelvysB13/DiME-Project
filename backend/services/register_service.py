from sqlalchemy.orm import Session
from models.vendedor_model import Vendedor
from models.admin_model import Admin
from schemas import RegisterRequest
from auth.jwt_handler import create_pre_token


class EmailAlreadyExistsError(Exception):
    pass


def register(db: Session, payload: RegisterRequest) -> str:

    existing = db.query(Vendedor).filter(Vendedor.email == payload.email).first()
    if existing:
        raise EmailAlreadyExistsError()

    existing_admin = db.query(Admin).filter(Admin.email == payload.email).first()
    if existing_admin:
        raise EmailAlreadyExistsError()

    pre_token = create_pre_token({
        "email": payload.email,
        "password": payload.password.get_secret_value(),
        "nombre_tienda": payload.nombre_tienda,
    })

    return pre_token
