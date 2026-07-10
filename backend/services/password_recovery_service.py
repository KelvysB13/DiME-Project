import logging
import jwt
from datetime import timedelta
from sqlalchemy.orm import Session
from models.vendedor_model import Vendedor
from models.admin_model import Admin
from auth.hash_handler import hash_data
from auth.jwt_handler import create_access_token, ALGORITHM
from core.config import settings

logger = logging.getLogger(__name__)

RESET_TOKEN_EXPIRE_MINUTES = 15

class EmailNotFoundError(Exception):
    pass

class InvalidResetTokenError(Exception):
    pass

def request_password_recovery(db: Session, email: str) -> str | None:

    vendedor = db.query(Vendedor).filter(Vendedor.email == email).first()

    if not vendedor:
        return None

    token = create_access_token(

        data={"sub": email, "type": "password_recovery"},
        expires_delta=timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES),
    )

    return token

def reset_password(db: Session, token: str, new_password: str) -> None:

    try:
        payload = jwt.decode(token, settings.app_secret_key, algorithms=[ALGORITHM])
    
    except jwt.PyJWTError:
        raise InvalidResetTokenError()
    
    if payload.get("type") != "password_recovery":
        raise InvalidResetTokenError()
    
    email = payload.get("sub")

    if not email:
        raise InvalidResetTokenError()
    
    vendedor = db.query(Vendedor).filter(Vendedor.email == email).first()

    if not vendedor:
        raise InvalidResetTokenError()
    
    vendedor.password = hash_data(new_password)
    db.commit()
