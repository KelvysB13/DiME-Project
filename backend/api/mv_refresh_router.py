from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from auth.deps import get_current_user
from models.vendedor_model import Vendedor
from schemas.mv_refresh_schema import RefreshMvResponse
from services.mv_refresh_service import refresh_materialized_views

router = APIRouter()

@router.post("/refresh-materialized-views", response_model=RefreshMvResponse)
def refresh_views(
    db: Session = Depends(get_db),
    current_user: Vendedor = Depends(get_current_user),
):
    try:
        refreshed = refresh_materialized_views(db)
        names = ", ".join(refreshed)
        return RefreshMvResponse(message=f"Vistas materializadas actualizadas: {names}")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al refrescar vistas materializadas: {str(e)}",
        )
