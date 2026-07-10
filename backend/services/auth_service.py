import jwt
from sqlalchemy.orm import Session
from models.vendedor_model import Vendedor
from models.admin_model import Admin
from schemas import LoginRequest, TokenResponse, LogoutRequest
from auth.hash_handler import verify_hash
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
    print(f"[DEBUG] Vendedor query: {vendedor}")

    if vendedor:
        if not verify_hash(payload.password.get_secret_value(), vendedor.password):
            raise InvalidCredentialsError()

        if not vendedor.esta_activo:
            raise InactiveAccountError()

        access_token = create_access_token(data={"sub": str(vendedor.id_vendedor), "role": "vendedor"})
        return TokenResponse(id_vendedor=vendedor.id_vendedor, access_token=access_token, token_type="bearer", expires_in=3600, role="vendedor")

    admin = db.query(Admin).filter(Admin.email == payload.email).first()
    print(f"[DEBUG] Admin query: {admin}")

    if not admin or not verify_hash(payload.password.get_secret_value(), admin.password):
        print(f"[DEBUG] Admin password check failed. Stored hash: {admin.password if admin else 'N/A'}")
        raise InvalidCredentialsError()

    if not admin.esta_activo:
        raise InactiveAccountError()

    access_token = create_access_token(data={"sub": str(admin.id_admin), "role": "admin"})
    return TokenResponse(id_vendedor=admin.id_admin, access_token=access_token, token_type="bearer", expires_in=3600, role="admin")

def logout(db: Session, payload: LogoutRequest) -> None:

    try:
        token_data = jwt.decode(payload.access_token, settings.app_secret_key, algorithms=[ALGORITHM])

    except jwt.PyJWTError:
        raise InvalidTokenError()

    user_id = token_data.get("sub")
    role = token_data.get("role", "vendedor")

    if user_id is None:
        raise InvalidTokenError()

    if role == "admin":
        user = db.query(Admin).filter(Admin.id_admin == int(user_id)).first()
    else:
        user = db.query(Vendedor).filter(Vendedor.id_vendedor == int(user_id)).first()

    if user is None:
        raise InvalidTokenError()

    if not user.esta_activo:
        raise InactiveAccountError()

    user.access_token = None
    user.refresh_token = None
    user.tiempo_token = None
    
    db.commit()
