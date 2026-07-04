from typing import List, Optional
from sqlalchemy.orm import Session
from models.kpis_maestro_model import KpiMaestro
from schemas.kpis_maestro_schema import KpiMaestroCreate, KpiMaestroUpdate, KpiMaestroResponse


def get_all_kpis(db: Session) -> List[KpiMaestroResponse]:
    rows = db.query(KpiMaestro).order_by(KpiMaestro.id_kpi).all()
    return [_row_to_response(r) for r in rows]


def get_kpi_by_id(db: Session, kpi_id: int) -> Optional[KpiMaestroResponse]:
    row = db.query(KpiMaestro).filter(KpiMaestro.id_kpi == kpi_id).first()
    if not row:
        return None
    return _row_to_response(row)


def create_kpi(db: Session, data: KpiMaestroCreate) -> KpiMaestroResponse:
    row = KpiMaestro(**data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return _row_to_response(row)


def update_kpi(db: Session, kpi_id: int, data: KpiMaestroUpdate) -> Optional[KpiMaestroResponse]:
    row = db.query(KpiMaestro).filter(KpiMaestro.id_kpi == kpi_id).first()
    if not row:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(row, field, value)
    db.commit()
    db.refresh(row)
    return _row_to_response(row)


def delete_kpi(db: Session, kpi_id: int) -> bool:
    row = db.query(KpiMaestro).filter(KpiMaestro.id_kpi == kpi_id).first()
    if not row:
        return False
    db.delete(row)
    db.commit()
    return True


def _row_to_response(row: KpiMaestro) -> KpiMaestroResponse:
    return KpiMaestroResponse(
        id_kpi=row.id_kpi,
        dimension=row.dimension,
        nombre_kpi=row.nombre_kpi,
        operador_logico=row.operador_logico,
        umbral_verde_inf=row.umbral_verde_inf,
        umbral_verde_sup=row.umbral_verde_sup,
        umbral_amarillo_inf=row.umbral_amarillo_inf,
        umbral_amarillo_sup=row.umbral_amarillo_sup,
        texto_ideal=row.texto_ideal,
        texto_alerta=row.texto_alerta,
        texto_peligro=row.texto_peligro,
        prioridad=row.prioridad,
    )
