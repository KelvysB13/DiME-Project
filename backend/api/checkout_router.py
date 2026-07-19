from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from schemas import CheckoutRequest, CheckoutResponse, SyncMockoonRequest, SyncMockoonResponse
from services import checkout as checkout_service, CheckoutError
from services.checkout_service import sync_with_mockoon
from auth.deps import get_current_user
from models.vendedor_model import Vendedor

router = APIRouter()

@router.post("/checkout", response_model=CheckoutResponse)
def checkout(payload: CheckoutRequest, db: Session = Depends(get_db)):

    try:
        return checkout_service(db, payload)

    except CheckoutError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/sync-mockoon", response_model=SyncMockoonResponse)
def sync_mockoon(
    payload: SyncMockoonRequest,
    db: Session = Depends(get_db),
    current_user: Vendedor = Depends(get_current_user),
):

    if not isinstance(current_user, Vendedor):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo vendedores")

    try:
        result = sync_with_mockoon(db, current_user, payload.usuario_ml)
        return SyncMockoonResponse(success=True, message=result["message"])
    except CheckoutError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
