from sqlalchemy.orm import Session
from models.vendedor_model import Vendedor
from schemas.update_password_schema import UpdatePasswordRequest
from auth.hash_handler import hash_data, verify_hash


class InvalidCurrentPasswordError(Exception):
    pass


def update_password(db: Session, current_user: Vendedor, payload: UpdatePasswordRequest) -> None:
    if not verify_hash(payload.current_password.get_secret_value(), current_user.password):
        raise InvalidCurrentPasswordError()
    current_user.password = hash_data(payload.new_password.get_secret_value())
    db.commit()
