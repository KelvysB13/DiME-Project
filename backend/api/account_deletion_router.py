from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from auth.deps import get_current_user
from models.vendedor_model import Vendedor
from schemas.account_deletion_schema import AccountDeletionResponse
from services.account_deletion_service import delete_account, AccountDeletionError

router = APIRouter()

@router.delete("/account-deletion", response_model=AccountDeletionResponse)
def account_deletion(
    db: Session = Depends(get_db),
    current_user: Vendedor = Depends(get_current_user),
):
    try:
        delete_account(db, current_user.id_vendedor)
        return AccountDeletionResponse(message="Todos los datos de la cuenta han sido eliminados permanentemente")
    except AccountDeletionError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendedor no encontrado",
        )
