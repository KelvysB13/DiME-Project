from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from schemas import RegisterRequest, PreRegisterResponse
from services import register, EmailAlreadyExistsError
from auth.jwt_handler import PRE_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=PreRegisterResponse)
def register_user(payload: RegisterRequest, db: Session = Depends(get_db)):

    try:
        pre_token = register(db, payload)
        return PreRegisterResponse(
            message="Datos verificados. Complete el pago para activar su cuenta.",
            pre_token=pre_token,
            expires_in_minutes=PRE_TOKEN_EXPIRE_MINUTES,
        )

    except EmailAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El correo electrónico ya está registrado",
        )
