from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.deps import get_current_user
from app.models.vendedor_model import Vendedor
from app.services.dashboard_service import get_dashboard
from app.schemas import DashboardResponse

router = APIRouter()


@router.get("", response_model=DashboardResponse)
def dashboard(
    db: Session = Depends(get_db),
    current_user: Vendedor = Depends(get_current_user),
):
    try:
        return get_dashboard(db, current_user.id_vendedor)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener datos del dashboard",
        )
