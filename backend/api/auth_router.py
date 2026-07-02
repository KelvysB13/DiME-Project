from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from auth.deps import get_current_user
from models.vendedor_model import Vendedor
from schemas import LoginRequest, TokenResponse
from schemas.logout_schema import LogoutResponse
from services import login as login_service, InvalidCredentialsError, InactiveAccountError
from services.auth_service import logout as logout_service

router = APIRouter()

@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(payload: LoginRequest, db: Session = Depends(get_db)):

    try:
        return login_service(db, payload)

    except InvalidCredentialsError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

    except InactiveAccountError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cuenta desactivada")

@router.post("/logout", response_model=LogoutResponse, status_code=status.HTTP_200_OK)
def logout(db: Session = Depends(get_db), current_user: Vendedor = Depends(get_current_user)):

    logout_service(db, current_user)
    return LogoutResponse()
