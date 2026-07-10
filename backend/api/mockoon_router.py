from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from auth.deps import get_current_user
from models.admin_model import Admin
from schemas.mockoon_schema import MetricsRequest, MetricsResponse
from services.mockoon_service import save_metrics

router = APIRouter()


def _verify_admin(current_user: Admin = Depends(get_current_user)) -> Admin:
    if not isinstance(current_user, Admin):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo administradores")
    return current_user


@router.post("/mockoon-data", response_model=MetricsResponse, status_code=status.HTTP_201_CREATED)
def guardar_metricas(payload: MetricsRequest, db: Session = Depends(get_db), _admin: Admin = Depends(_verify_admin)):

    try:
        return save_metrics(db, payload)
    
    except Exception as e:

        import traceback
        traceback.print_exc()

        raise HTTPException(
            
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
