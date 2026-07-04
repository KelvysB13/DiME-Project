from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from auth.deps import get_current_user
from models.vendedor_model import Vendedor
from schemas import PersonalDataResponse
from services import get_personal_data, UserNotFoundError

router = APIRouter()

@router.get("/personal-data", response_model=PersonalDataResponse)
def personal_data(db: Session = Depends(get_db), current_user: Vendedor = Depends(get_current_user)):

    try:
        return get_personal_data(db, current_user.id_vendedor)

    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
