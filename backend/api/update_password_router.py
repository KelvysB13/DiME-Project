from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.update_password_schema import UpdatePasswordRequest
from services.update_password_service import update_password, InvalidCurrentPasswordError
from auth.deps import get_current_user
from models.vendedor_model import Vendedor

router = APIRouter()


@router.patch("/update-password")
def update_user_password(
    payload: UpdatePasswordRequest,
    db: Session = Depends(get_db),
    current_user: Vendedor = Depends(get_current_user),
):
    try:
        update_password(db, current_user, payload)
        return {"message": "Contraseña actualizada exitosamente"}
    except InvalidCurrentPasswordError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña actual no es correcta",
        )
