from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from auth.deps import get_current_user
from models.vendedor_model import Vendedor
from schemas.diagnostico_schema import (
    MvDiagnosticoReputacion,
    MvDiagnosticoFinanzas,
    MvDiagnosticoAds,
    MvDiagnosticoStock,
    MvDiagnosticoPublicaciones,
    MetricaCalidadPublicacion,
)
from services.diagnostico_service import (
    get_diagnostico_reputacion,
    get_diagnostico_finanzas,
    get_diagnostico_ads,
    get_diagnostico_stock,
    get_diagnostico_publicaciones,
    get_metricas_calidad_publicacion,
)
from pydantic import BaseModel
from typing import List, Optional


class DiagnosticoResponse(BaseModel):

    id_vendedor: int
    mv_diagnostico_reputacion: Optional[MvDiagnosticoReputacion] = None
    mv_diagnostico_finanzas: Optional[MvDiagnosticoFinanzas] = None
    mv_diagnostico_ads: Optional[MvDiagnosticoAds] = None
    mv_diagnostico_stock: Optional[MvDiagnosticoStock] = None
    mv_diagnostico_publicaciones: Optional[MvDiagnosticoPublicaciones] = None
    metrica_calidad_publicacion: List[MetricaCalidadPublicacion] = []


router = APIRouter()


@router.get("/diagnostic", response_model=DiagnosticoResponse)
def diagnostic(db: Session = Depends(get_db), current_user: Vendedor = Depends(get_current_user)):

    vendedor_id = current_user.id_vendedor

    try:
        return DiagnosticoResponse(
            id_vendedor=vendedor_id,
            mv_diagnostico_reputacion=get_diagnostico_reputacion(db, vendedor_id),
            mv_diagnostico_finanzas=get_diagnostico_finanzas(db, vendedor_id),
            mv_diagnostico_ads=get_diagnostico_ads(db, vendedor_id),
            mv_diagnostico_stock=get_diagnostico_stock(db, vendedor_id),
            mv_diagnostico_publicaciones=get_diagnostico_publicaciones(db, vendedor_id),
            metrica_calidad_publicacion=get_metricas_calidad_publicacion(db, vendedor_id),
        )

    except Exception:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener datos del diagnóstico",
        )
