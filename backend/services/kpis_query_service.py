from typing import Optional
from sqlalchemy.orm import Session
from models.v_diagnostico_vendedores_semaforo import DiagnosticoVendedoresSemaforo
from schemas.kpis_query_schema import KpiQueryItem, KpiQueryResponse


def get_kpi_by_name(
    db: Session,
    vendedor_id: int,
    nombre_kpi: str,
) -> Optional[KpiQueryItem]:
    row = (
        db.query(DiagnosticoVendedoresSemaforo)
        .filter(
            DiagnosticoVendedoresSemaforo.id_vendedor == vendedor_id,
            DiagnosticoVendedoresSemaforo.nombre_kpi == nombre_kpi,
        )
        .first()
    )
    if not row:
        return None
    return KpiQueryItem(
        dimension=row.dimension,
        nombre_kpi=row.nombre_kpi,
        prioridad=row.prioridad,
        valor_actual=row.valor_actual,
        estado_semaforo=row.estado_semaforo,
    )


def query_kpis(
    db: Session,
    vendedor_id: int,
    dimension: Optional[str] = None,
    estado: Optional[str] = None,
    prioridad: Optional[str] = None,
) -> KpiQueryResponse:
    query = db.query(DiagnosticoVendedoresSemaforo).filter(
        DiagnosticoVendedoresSemaforo.id_vendedor == vendedor_id
    )

    if dimension:
        query = query.filter(DiagnosticoVendedoresSemaforo.dimension == dimension)
    if estado:
        query = query.filter(DiagnosticoVendedoresSemaforo.estado_semaforo == estado)
    if prioridad:
        query = query.filter(DiagnosticoVendedoresSemaforo.prioridad == prioridad)

    rows = query.all()

    items = [
        KpiQueryItem(
            dimension=row.dimension,
            nombre_kpi=row.nombre_kpi,
            prioridad=row.prioridad,
            valor_actual=row.valor_actual,
            estado_semaforo=row.estado_semaforo,
        )
        for row in rows
    ]

    return KpiQueryResponse(id_vendedor=vendedor_id, items=items)
