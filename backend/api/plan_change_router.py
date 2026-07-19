from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from auth.deps import get_current_user
from models.vendedor_model import Vendedor
from schemas.plan_update_schema import PlanChangeRequest
from services.plan_change_service import change_plan, PlanNotFoundError

router = APIRouter()


@router.patch("/vendedor/plan")
def cambiar_plan(
    payload: PlanChangeRequest,
    db: Session = Depends(get_db),
    current_user: Vendedor = Depends(get_current_user),
):
    try:
        change_plan(db, current_user.id_vendedor, payload.tipo_plan)
        return {"message": "Plan actualizado exitosamente"}
    except PlanNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
