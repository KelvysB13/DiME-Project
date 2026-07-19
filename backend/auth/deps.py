import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from core.config import settings
from core.database import get_db
from models.vendedor_model import Vendedor
from models.admin_model import Admin
from auth.jwt_handler import ALGORITHM

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)) -> Vendedor | Admin:

    token = credentials.credentials

    try:

        payload = jwt.decode(token, settings.app_secret_key, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        role = payload.get("role", "vendedor")

        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado")

    if role == "admin":
        user = db.query(Admin).filter(Admin.id_admin == int(user_id)).first()
    else:
        user = db.query(Vendedor).filter(Vendedor.id_vendedor == int(user_id)).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")

    if not user.esta_activo:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cuenta desactivada")

    return user
