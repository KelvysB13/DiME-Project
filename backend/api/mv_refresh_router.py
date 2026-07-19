from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session
from core.database import get_db
from auth.deps import get_current_user
from models.vendedor_model import Vendedor
from schemas.mv_refresh_schema import RefreshMvResponse

router = APIRouter()

@router.post("/refresh-materialized-views", response_model=RefreshMvResponse)
def refresh_views(
    db: Session = Depends(get_db),
    current_user: Vendedor = Depends(get_current_user),
):
    try:
        db.execute(text("CALL sp_sincronizar_diagnostico_dime()"))
        db.commit()
        return RefreshMvResponse(message="Sincronización completada exitosamente")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al sincronizar: {str(e)}",
        )
