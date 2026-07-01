from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from schemas import RegisterRequest
from services import register, EmailAlreadyExistsError

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(payload: RegisterRequest, db: Session = Depends(get_db)):

    try:
        register(db, payload)
        return {"message": "Usuario registrado exitosamente"}

    except EmailAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El correo electrónico ya está registrado",
        )
