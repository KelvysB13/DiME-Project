from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from auth.deps import get_current_user
from core.database import get_db
from models.vendedor_model import Vendedor
from schemas.historiales_schemas import (
    HistDiagnosticoReputacion,
    HistDiagnosticoFinanzas,
    HistDiagnosticoPublicaciones,
    HistDiagnosticoAds,
    HistDiagnosticoStock,
)
from services.historiales_service import (
    get_hist_reputacion,
    get_hist_finanzas,
    get_hist_publicaciones,
    get_hist_ads,
    get_hist_stock,
)


class HistorialCompletoResponse(BaseModel):

    id_vendedor: int
    fecha_consultada: Optional[date] = None
    reputacion: List[HistDiagnosticoReputacion] = []
    finanzas: List[HistDiagnosticoFinanzas] = []
    publicaciones: List[HistDiagnosticoPublicaciones] = []
    ads: List[HistDiagnosticoAds] = []
    stock: List[HistDiagnosticoStock] = []


router = APIRouter()


@router.get("/history", response_model=HistorialCompletoResponse)
def historial_completo(
    limite: int = Query(10, ge=1, le=100, description="Cantidad de registros por tabla"),
    db: Session = Depends(get_db),
    current_user: Vendedor = Depends(get_current_user),
):

    vendedor_id = current_user.id_vendedor

    try:
        return HistorialCompletoResponse(
            id_vendedor=vendedor_id,
            reputacion=get_hist_reputacion(db, vendedor_id, limite),
            finanzas=get_hist_finanzas(db, vendedor_id, limite),
            publicaciones=get_hist_publicaciones(db, vendedor_id, limite),
            ads=get_hist_ads(db, vendedor_id, limite),
            stock=get_hist_stock(db, vendedor_id, limite),
        )

    except Exception:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener el historial del vendedor",
        )


@router.get("/history/date", response_model=HistorialCompletoResponse)
def historial_por_fecha(
    fecha: date = Query(..., description="Fecha específica para filtrar (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
    current_user: Vendedor = Depends(get_current_user),
):

    vendedor_id = current_user.id_vendedor

    try:
        historial_reputacion = [
            r for r in get_hist_reputacion(db, vendedor_id, 1000)
            if r.fecha_captura == fecha
        ]
        historial_finanzas = [
            r for r in get_hist_finanzas(db, vendedor_id, 1000)
            if r.fecha_inicio_periodo and r.fecha_inicio_periodo <= fecha
            and r.fecha_fin_periodo and r.fecha_fin_periodo >= fecha
        ]
        historial_publicaciones = get_hist_publicaciones(db, vendedor_id, 1000)
        historial_ads = get_hist_ads(db, vendedor_id, 1000)
        historial_stock = get_hist_stock(db, vendedor_id, 1000)

        return HistorialCompletoResponse(
            id_vendedor=vendedor_id,
            fecha_consultada=fecha,
            reputacion=historial_reputacion,
            finanzas=historial_finanzas,
            publicaciones=historial_publicaciones,
            ads=historial_ads,
            stock=historial_stock,
        )

    except Exception:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al filtrar el historial por fecha",
        )
