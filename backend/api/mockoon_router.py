from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.mockoon_schema import MetricsRequest, MetricsResponse
from services.mockoon_service import save_metrics

router = APIRouter()


@router.post("/moockon-data", response_model=MetricsResponse, status_code=status.HTTP_201_CREATED)
def guardar_metricas(payload: MetricsRequest, db: Session = Depends(get_db)):

    try:
        return save_metrics(db, payload)
    
    except Exception as e:

        import traceback
        traceback.print_exc()

        raise HTTPException(
            
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
