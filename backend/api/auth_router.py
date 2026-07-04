from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from schemas import LoginRequest, TokenResponse, LogoutRequest, LogoutResponse
from schemas import PasswordRecoveryRequest, PasswordRecoveryResponse, ResetPasswordRequest, ResetPasswordResponse
from services import login as login_service, InvalidCredentialsError, InactiveAccountError
from services import logout as logout_service, InvalidTokenError
from services import request_password_recovery, InvalidResetTokenError
from services.password_recovery_service import reset_password as reset_password_service

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
def logout(payload: LogoutRequest, db: Session = Depends(get_db)):

    try:
        logout_service(db, payload)
        return LogoutResponse()

    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado")

    except InactiveAccountError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cuenta desactivada")

@router.post("/password-recovery", response_model=PasswordRecoveryResponse, status_code=status.HTTP_200_OK)
def password_recovery(payload: PasswordRecoveryRequest, db: Session = Depends(get_db)):

    token = request_password_recovery(db, payload.email)
    return PasswordRecoveryResponse(reset_token=token)

@router.post("/reset-password", response_model=ResetPasswordResponse, status_code=status.HTTP_200_OK)
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):

    try:
        reset_password_service(db, payload.token, payload.new_password.get_secret_value())
        return ResetPasswordResponse()
    
    except InvalidResetTokenError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token inválido o expirado")
