from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from schemas import PaymentMethodRequest, PaymentMethodResponse
from services import update_payment_method, PaymentMethodError
from auth.deps import get_current_user
from models.vendedor_model import Vendedor

router = APIRouter()

@router.put("/method", response_model=PaymentMethodResponse)
def update_method(payload: PaymentMethodRequest, db: Session = Depends(get_db), current_user: Vendedor = Depends(get_current_user)):

    try:
        return update_payment_method(db, payload, current_user.id_vendedor)

    except PaymentMethodError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
