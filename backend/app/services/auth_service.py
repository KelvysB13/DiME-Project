from sqlalchemy.orm import Session
from app.models.vendedor_model import Vendedor
from app.schemas import LoginRequest, TokenResponse
from app.auth.password_handler import verify_password
from app.auth.jwt_handler import create_access_token

class InvalidCredentialsError(Exception):
    pass

class InactiveAccountError(Exception):
    pass

def login(db: Session, payload: LoginRequest) -> TokenResponse:

    vendedor = db.query(Vendedor).filter(Vendedor.email == payload.email).first()

    if not vendedor or not verify_password(payload.password.get_secret_value(), vendedor.password):
        raise InvalidCredentialsError()

    if not vendedor.esta_activo:
        raise InactiveAccountError()

    access_token = create_access_token(data={"sub": str(vendedor.id_vendedor)})

    return TokenResponse(access_token=access_token, token_type="bearer", expires_in=3600)
