from typing import List, Optional
from sqlalchemy.orm import Session
from models.mv_diagnostico_reputacion import DiagnosticoReputacion
from models.mv_diagnostico_finanzas import DiagnosticoFinanzas
from models.mv_diagnostico_ads import DiagnosticoAds
from models.mv_diagnostico_stock import DiagnosticoStock
from models.mv_diagnostico_publicaciones import DiagnosticoPublicaciones
from models.metrica_calidad_model import Calidad
from models.publicacion_model import Publicacion
from schemas.diagnostico_schema import (
    MvDiagnosticoReputacion,
    MvDiagnosticoFinanzas,
    MvDiagnosticoAds,
    MvDiagnosticoStock,
    MvDiagnosticoPublicaciones,
    MetricaCalidadPublicacion,
)


def get_diagnostico_reputacion(db: Session, vendedor_id: int) -> Optional[MvDiagnosticoReputacion]:

    row = (
        db.query(DiagnosticoReputacion)
        .filter(DiagnosticoReputacion.id == vendedor_id)
        .first()
    )
    if not row:
        return None

    return MvDiagnosticoReputacion(
        tasa_reclamos=float(row.tasa_reclamos),
        tasa_cancelaciones=float(row.tasa_cancelaciones),
        tasa_mediaciones=float(row.tasa_mediaciones),
        tasa_envios_incorrectos=float(row.tasa_envios_incorrectos),
        nivel_reputacion=row.nivel_reputacion,
        insignia=row.insignia,
        fecha_captura=row.fecha_captura.date(),
    )


def get_diagnostico_finanzas(db: Session, vendedor_id: int) -> Optional[MvDiagnosticoFinanzas]:

    row = (
        db.query(DiagnosticoFinanzas)
        .filter(DiagnosticoFinanzas.id == vendedor_id)
        .first()
    )
    if not row:
        return None

    return MvDiagnosticoFinanzas(
        cvr_global=float(row.cvr_global),
        margen_neto_real=float(row.margen_neto_real),
        ticket_promedio=float(row.ticket_promedio),
        carga_total_costos=float(row.carga_total_costos),
        ratio_intencion_compra=float(row.ratio_intencion_compra),
        descuento_reputacion=float(row.descuento_reputacion),
        tasa_cobro_efectivo=float(row.tasa_cobro_efectivo),
        crecimiento_mom=float(row.crecimiento_mom) if row.crecimiento_mom is not None else None,
        ventas_periodo_actual=row.ventas_periodo_actual,
        fecha_inicio_periodo=row.fecha_inicio_periodo,
        fecha_fin_periodo=row.fecha_fin_periodo,
    )


def get_diagnostico_ads(db: Session, vendedor_id: int) -> Optional[MvDiagnosticoAds]:

    row = (
        db.query(DiagnosticoAds)
        .filter(DiagnosticoAds.id == vendedor_id)
        .first()
    )
    if not row:
        return None

    return MvDiagnosticoAds(
        roas=float(row.roas),
        acos=float(row.acos),
        inversion_ads_sobre_ventas=float(row.inversion_ads_sobre_ventas),
        inversion_ads=float(row.inversion_ads),
    )


def get_diagnostico_stock(db: Session, vendedor_id: int) -> Optional[MvDiagnosticoStock]:

    row = (
        db.query(DiagnosticoStock)
        .filter(DiagnosticoStock.id == vendedor_id)
        .first()
    )
    if not row:
        return None

    return MvDiagnosticoStock(
        dead_stock_rate=float(row.dead_stock_rate),
        antiguedad_riesgo=float(row.antiguedad_riesgo),
        productos_no_aptos=float(row.productos_no_aptos),
        overstock_rate=float(row.overstock_rate),
        utilizacion_espacios=float(row.utilizacion_espacios),
        puntaje_calidad=row.puntaje_calidad,
    )


def get_diagnostico_publicaciones(db: Session, vendedor_id: int) -> Optional[MvDiagnosticoPublicaciones]:

    row = (
        db.query(DiagnosticoPublicaciones)
        .filter(DiagnosticoPublicaciones.id == vendedor_id)
        .first()
    )
    if not row:
        return None

    return MvDiagnosticoPublicaciones(
        total_publicaciones=row.total_publicaciones,
        cvr_publicacion=float(row.cvr_publicacion),
        pct_catalogo_completo=float(row.pct_catalogo_completo),
        pct_publicaciones_con_video=float(row.pct_publicaciones_con_video),
    )


def get_metricas_calidad_publicacion(db: Session, vendedor_id: int) -> List[MetricaCalidadPublicacion]:

    resultados = (
        db.query(Calidad)
        .join(Publicacion, Calidad.id_publicacion == Publicacion.id_publicacion)
        .filter(Publicacion.id_vendedor == vendedor_id)
        .all()
    )

    return [
        MetricaCalidadPublicacion(
            id_publicacion=r.id_publicacion,
            fecha_captura=r.fecha_captura,
            cantidad_fotos=r.cantidad_fotos,
            tiene_video=r.tiene_video,
            caracteristicas_completas=r.caracteristicas_completas,
            puntaje_calidad=r.puntaje_calidad,
        )
        for r in resultados
    ]
