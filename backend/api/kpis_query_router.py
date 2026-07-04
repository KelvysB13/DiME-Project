from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from core.database import get_db
from auth.deps import get_current_user
from models.vendedor_model import Vendedor
from schemas.kpis_query_schema import KpiQueryItem, KpiQueryResponse
from services.kpis_query_service import query_kpis, get_kpi_by_name

router = APIRouter()


@router.get("/kpis-query", response_model=KpiQueryResponse)
def kpis_query(
    vendedor_id: int = Query(..., description="ID del vendedor"),
    dimension: Optional[str] = Query(None, description="Filtrar por dimensión"),
    estado: Optional[str] = Query(None, description="Filtrar por estado del semáforo (VERDE, AMARILLO, ROJO, GRIS)"),
    prioridad: Optional[str] = Query(None, description="Filtrar por prioridad"),
    db: Session = Depends(get_db),
    current_user: Vendedor = Depends(get_current_user),
):
    try:
        return query_kpis(
            db,
            vendedor_id=vendedor_id,
            dimension=dimension,
            estado=estado,
            prioridad=prioridad,
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener KPIs del diagnóstico",
        )


@router.get("/kpis-query/item", response_model=KpiQueryItem)
def kpis_query_item(
    vendedor_id: int = Query(..., description="ID del vendedor"),
    nombre_kpi: str = Query(..., description="Nombre del KPI"),
    db: Session = Depends(get_db),
    current_user: Vendedor = Depends(get_current_user),
):
    try:
        kpi = get_kpi_by_name(db, vendedor_id, nombre_kpi)
        if not kpi:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"KPI '{nombre_kpi}' no encontrado para el vendedor {vendedor_id}",
            )
        return kpi
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener KPI del diagnóstico",
        )
