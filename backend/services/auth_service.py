import jwt
from sqlalchemy.orm import Session
from models.vendedor_model import Vendedor
from schemas import LoginRequest, TokenResponse, LogoutRequest
from auth.password_handler import verify_password
from auth.jwt_handler import create_access_token, ALGORITHM
from core.config import settings

class InvalidCredentialsError(Exception):
    pass

class InactiveAccountError(Exception):
    pass

class InvalidTokenError(Exception):
    pass

def login(db: Session, payload: LoginRequest) -> TokenResponse:

    vendedor = db.query(Vendedor).filter(Vendedor.email == payload.email).first()

    if not vendedor or not verify_password(payload.password.get_secret_value(), vendedor.password):
        raise InvalidCredentialsError()

    if not vendedor.esta_activo:
        raise InactiveAccountError()

    access_token = create_access_token(data={"sub": str(vendedor.id_vendedor)})
    return TokenResponse(access_token=access_token, token_type="bearer", expires_in=3600)

def logout(db: Session, payload: LogoutRequest) -> None:

    try:
        token_data = jwt.decode(payload.access_token, settings.app_secret_key, algorithms=[ALGORITHM])

    except jwt.PyJWTError:
        raise InvalidTokenError()

    user_id = token_data.get("sub")

    if user_id is None:
        raise InvalidTokenError()

    vendedor = db.query(Vendedor).filter(Vendedor.id_vendedor == int(user_id)).first()

    if vendedor is None:
        raise InvalidTokenError()

    if not vendedor.esta_activo:
        raise InactiveAccountError()

    vendedor.access_token = None
    vendedor.refresh_token = None
    vendedor.tiempo_token = None
    
    db.commit()
