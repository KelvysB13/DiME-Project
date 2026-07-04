from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from auth.deps import get_current_user
from models.vendedor_model import Vendedor
from schemas.kpis_maestro_schema import KpiMaestroUpdate, KpiMaestroResponse
from services.kpis_maestro_service import (
    get_all_kpis,
    get_kpi_by_id,
    update_kpi,
)

router = APIRouter()


@router.get("/master-kpis", response_model=List[KpiMaestroResponse])
def list_kpis(db: Session = Depends(get_db), current_user: Vendedor = Depends(get_current_user)):
    return get_all_kpis(db)


@router.get("/master-kpis/{kpi_id}", response_model=KpiMaestroResponse)
def get_kpi(kpi_id: int, db: Session = Depends(get_db), current_user: Vendedor = Depends(get_current_user)):
    kpi = get_kpi_by_id(db, kpi_id)
    if not kpi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="KPI no encontrado")
    return kpi


@router.put("/master-kpis/{kpi_id}", response_model=KpiMaestroResponse)
def update_kpi_endpoint(kpi_id: int, data: KpiMaestroUpdate, db: Session = Depends(get_db), current_user: Vendedor = Depends(get_current_user)):
    kpi = update_kpi(db, kpi_id, data)
    if not kpi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="KPI no encontrado")
    return kpi
