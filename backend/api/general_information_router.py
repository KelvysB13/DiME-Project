from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from auth.deps import get_current_user
from models.vendedor_model import Vendedor
from schemas import UserInfo
from services.general_information_service import get_user_info, UserNotFoundError

router = APIRouter()

@router.get("/general-information", response_model=UserInfo)
def user_info(
    db: Session = Depends(get_db),
    current_user: Vendedor = Depends(get_current_user),
):
    try:
        return get_user_info(db, current_user.id_vendedor)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
