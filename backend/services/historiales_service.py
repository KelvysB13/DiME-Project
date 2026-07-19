from datetime import date, datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from models import (
    HistDiagnosticoReputacion as HistReputacionModel,
    HistDiagnosticoFinanzas as HistFinanzasModel,
    HistDiagnosticoPublicaciones as HistPublicacionesModel,
    HistDiagnosticoAds as HistAdsModel,
    HistDiagnosticoStock as HistStockModel,
)
from schemas.historiales_schemas import (
    HistDiagnosticoReputacion as HistReputacionSchema,
    HistDiagnosticoFinanzas as HistFinanzasSchema,
    HistDiagnosticoPublicaciones as HistPublicacionesSchema,
    HistDiagnosticoAds as HistAdsSchema,
    HistDiagnosticoStock as HistStockSchema,
)


# ---------------------------------------------------------------------------
# Reputación
# ---------------------------------------------------------------------------

def create_hist_reputacion(
    db: Session, payload: HistReputacionSchema
) -> HistReputacionSchema:

    row = HistReputacionModel(
        id_vendedor=payload.id_vendedor,
        tasa_reclamos=payload.tasa_reclamos,
        tasa_cancelaciones=payload.tasa_cancelaciones,
        tasa_mediaciones=payload.tasa_mediaciones,
        tasa_envios_incorrectos=payload.tasa_envios_incorrectos,
        nivel_reputacion=payload.nivel_reputacion,
        insignia=payload.insignia,
        fecha_captura=payload.fecha_captura,
    )
    db.add(row)
    db.commit()
    db.refresh(row)

    return _row_to_reputacion_schema(row)


def get_hist_reputacion(
    db: Session, vendedor_id: int, limite: int = 10
) -> List[HistReputacionSchema]:

    rows = (
        db.query(HistReputacionModel)
        .filter(HistReputacionModel.id_vendedor == vendedor_id)
        .order_by(HistReputacionModel.fecha_ingesta.desc())
        .limit(limite)
        .all()
    )
    return [_row_to_reputacion_schema(r) for r in rows]


def get_ultima_hist_reputacion(
    db: Session, vendedor_id: int
) -> Optional[HistReputacionSchema]:

    row = (
        db.query(HistReputacionModel)
        .filter(HistReputacionModel.id_vendedor == vendedor_id)
        .order_by(HistReputacionModel.fecha_ingesta.desc())
        .first()
    )
    if not row:
        return None
    return _row_to_reputacion_schema(row)


def _row_to_reputacion_schema(row: HistReputacionModel) -> HistReputacionSchema:
    return HistReputacionSchema(
        id_vendedor=row.id_vendedor,
        tasa_reclamos=float(row.tasa_reclamos) if row.tasa_reclamos is not None else None,
        tasa_cancelaciones=float(row.tasa_cancelaciones) if row.tasa_cancelaciones is not None else None,
        tasa_mediaciones=float(row.tasa_mediaciones) if row.tasa_mediaciones is not None else None,
        tasa_envios_incorrectos=float(row.tasa_envios_incorrectos) if row.tasa_envios_incorrectos is not None else None,
        nivel_reputacion=row.nivel_reputacion,
        insignia=row.insignia,
        fecha_captura=row.fecha_captura,
        fecha_ingesta=row.fecha_ingesta,
    )


# ---------------------------------------------------------------------------
# Finanzas
# ---------------------------------------------------------------------------

def create_hist_finanzas(
    db: Session, payload: HistFinanzasSchema
) -> HistFinanzasSchema:

    row = HistFinanzasModel(
        id_vendedor=payload.id_vendedor,
        cvr_global=payload.cvr_global,
        margen_neto_real=payload.margen_neto_real,
        ticket_promedio=payload.ticket_promedio,
        carga_total_costos=payload.carga_total_costos,
        ratio_intencion_compra=payload.ratio_intencion_compra,
        descuento_reputacion=payload.descuento_reputacion,
        tasa_cobro_efectivo=payload.tasa_cobro_efectivo,
        crecimiento_mom=payload.crecimiento_mom,
        ventas_periodo_actual=payload.ventas_periodo_actual,
        fecha_inicio_periodo=payload.fecha_inicio_periodo,
        fecha_fin_periodo=payload.fecha_fin_periodo,
    )
    db.add(row)
    db.commit()
    db.refresh(row)

    return _row_to_finanzas_schema(row)


def get_hist_finanzas(
    db: Session, vendedor_id: int, limite: int = 10
) -> List[HistFinanzasSchema]:

    rows = (
        db.query(HistFinanzasModel)
        .filter(HistFinanzasModel.id_vendedor == vendedor_id)
        .order_by(HistFinanzasModel.fecha_ingesta.desc())
        .limit(limite)
        .all()
    )
    return [_row_to_finanzas_schema(r) for r in rows]


def get_ultima_hist_finanzas(
    db: Session, vendedor_id: int
) -> Optional[HistFinanzasSchema]:

    row = (
        db.query(HistFinanzasModel)
        .filter(HistFinanzasModel.id_vendedor == vendedor_id)
        .order_by(HistFinanzasModel.fecha_ingesta.desc())
        .first()
    )
    if not row:
        return None
    return _row_to_finanzas_schema(row)


def _row_to_finanzas_schema(row: HistFinanzasModel) -> HistFinanzasSchema:
    return HistFinanzasSchema(
        id_vendedor=row.id_vendedor,
        cvr_global=float(row.cvr_global) if row.cvr_global is not None else None,
        margen_neto_real=float(row.margen_neto_real) if row.margen_neto_real is not None else None,
        ticket_promedio=float(row.ticket_promedio) if row.ticket_promedio is not None else None,
        carga_total_costos=float(row.carga_total_costos) if row.carga_total_costos is not None else None,
        ratio_intencion_compra=float(row.ratio_intencion_compra) if row.ratio_intencion_compra is not None else None,
        descuento_reputacion=float(row.descuento_reputacion) if row.descuento_reputacion is not None else None,
        tasa_cobro_efectivo=float(row.tasa_cobro_efectivo) if row.tasa_cobro_efectivo is not None else None,
        crecimiento_mom=float(row.crecimiento_mom) if row.crecimiento_mom is not None else None,
        ventas_periodo_actual=int(row.ventas_periodo_actual) if row.ventas_periodo_actual is not None else None,
        fecha_inicio_periodo=row.fecha_inicio_periodo,
        fecha_fin_periodo=row.fecha_fin_periodo,
        fecha_ingesta=row.fecha_ingesta,
    )


# ---------------------------------------------------------------------------
# Publicaciones
# ---------------------------------------------------------------------------

def create_hist_publicaciones(
    db: Session, payload: HistPublicacionesSchema
) -> HistPublicacionesSchema:

    row = HistPublicacionesModel(
        id_vendedor=payload.id_vendedor,
        total_publicaciones=payload.total_publicaciones,
        cvr_publicacion=payload.cvr_publicacion,
        pct_catalogo_completo=payload.pct_catalogo_completo,
        pct_publicaciones_con_video=payload.pct_publicaciones_con_video,
    )
    db.add(row)
    db.commit()
    db.refresh(row)

    return _row_to_publicaciones_schema(row)


def get_hist_publicaciones(
    db: Session, vendedor_id: int, limite: int = 10
) -> List[HistPublicacionesSchema]:

    rows = (
        db.query(HistPublicacionesModel)
        .filter(HistPublicacionesModel.id_vendedor == vendedor_id)
        .order_by(HistPublicacionesModel.fecha_ingesta.desc())
        .limit(limite)
        .all()
    )
    return [_row_to_publicaciones_schema(r) for r in rows]


def get_ultima_hist_publicaciones(
    db: Session, vendedor_id: int
) -> Optional[HistPublicacionesSchema]:

    row = (
        db.query(HistPublicacionesModel)
        .filter(HistPublicacionesModel.id_vendedor == vendedor_id)
        .order_by(HistPublicacionesModel.fecha_ingesta.desc())
        .first()
    )
    if not row:
        return None
    return _row_to_publicaciones_schema(row)


def _row_to_publicaciones_schema(row: HistPublicacionesModel) -> HistPublicacionesSchema:
    return HistPublicacionesSchema(
        id_vendedor=row.id_vendedor,
        total_publicaciones=int(row.total_publicaciones) if row.total_publicaciones is not None else None,
        cvr_publicacion=float(row.cvr_publicacion) if row.cvr_publicacion is not None else None,
        pct_catalogo_completo=float(row.pct_catalogo_completo) if row.pct_catalogo_completo is not None else None,
        pct_publicaciones_con_video=float(row.pct_publicaciones_con_video) if row.pct_publicaciones_con_video is not None else None,
        fecha_ingesta=row.fecha_ingesta,
    )


# ---------------------------------------------------------------------------
# Ads
# ---------------------------------------------------------------------------

def create_hist_ads(
    db: Session, payload: HistAdsSchema
) -> HistAdsSchema:

    row = HistAdsModel(
        id_vendedor=payload.id_vendedor,
        roas=payload.roas,
        acos=payload.acos,
        inversion_ads_sobre_ventas=payload.inversion_ads_sobre_ventas,
        inversion_ads=payload.inversion_ads,
    )
    db.add(row)
    db.commit()
    db.refresh(row)

    return _row_to_ads_schema(row)


def get_hist_ads(
    db: Session, vendedor_id: int, limite: int = 10
) -> List[HistAdsSchema]:

    rows = (
        db.query(HistAdsModel)
        .filter(HistAdsModel.id_vendedor == vendedor_id)
        .order_by(HistAdsModel.fecha_ingesta.desc())
        .limit(limite)
        .all()
    )
    return [_row_to_ads_schema(r) for r in rows]


def get_ultima_hist_ads(
    db: Session, vendedor_id: int
) -> Optional[HistAdsSchema]:

    row = (
        db.query(HistAdsModel)
        .filter(HistAdsModel.id_vendedor == vendedor_id)
        .order_by(HistAdsModel.fecha_ingesta.desc())
        .first()
    )
    if not row:
        return None
    return _row_to_ads_schema(row)


def _row_to_ads_schema(row: HistAdsModel) -> HistAdsSchema:
    return HistAdsSchema(
        id_vendedor=row.id_vendedor,
        roas=float(row.roas) if row.roas is not None else None,
        acos=float(row.acos) if row.acos is not None else None,
        inversion_ads_sobre_ventas=float(row.inversion_ads_sobre_ventas) if row.inversion_ads_sobre_ventas is not None else None,
        inversion_ads=float(row.inversion_ads) if row.inversion_ads is not None else None,
        fecha_ingesta=row.fecha_ingesta,
    )


# ---------------------------------------------------------------------------
# Stock
# ---------------------------------------------------------------------------

def create_hist_stock(
    db: Session, payload: HistStockSchema
) -> HistStockSchema:

    row = HistStockModel(
        id_vendedor=payload.id_vendedor,
        dead_stock_rate=payload.dead_stock_rate,
        antiguedad_riesgo=payload.antiguedad_riesgo,
        productos_no_aptos=payload.productos_no_aptos,
        overstock_rate=payload.overstock_rate,
        utilizacion_espacios=payload.utilizacion_espacios,
        puntaje_calidad=payload.puntaje_calidad,
    )
    db.add(row)
    db.commit()
    db.refresh(row)

    return _row_to_stock_schema(row)


def get_hist_stock(
    db: Session, vendedor_id: int, limite: int = 10
) -> List[HistStockSchema]:

    rows = (
        db.query(HistStockModel)
        .filter(HistStockModel.id_vendedor == vendedor_id)
        .order_by(HistStockModel.fecha_ingesta.desc())
        .limit(limite)
        .all()
    )
    return [_row_to_stock_schema(r) for r in rows]


def get_ultima_hist_stock(
    db: Session, vendedor_id: int
) -> Optional[HistStockSchema]:

    row = (
        db.query(HistStockModel)
        .filter(HistStockModel.id_vendedor == vendedor_id)
        .order_by(HistStockModel.fecha_ingesta.desc())
        .first()
    )
    if not row:
        return None
    return _row_to_stock_schema(row)


def _row_to_stock_schema(row: HistStockModel) -> HistStockSchema:
    return HistStockSchema(
        id_vendedor=row.id_vendedor,
        dead_stock_rate=float(row.dead_stock_rate) if row.dead_stock_rate is not None else None,
        antiguedad_riesgo=float(row.antiguedad_riesgo) if row.antiguedad_riesgo is not None else None,
        productos_no_aptos=float(row.productos_no_aptos) if row.productos_no_aptos is not None else None,
        overstock_rate=float(row.overstock_rate) if row.overstock_rate is not None else None,
        utilizacion_espacios=float(row.utilizacion_espacios) if row.utilizacion_espacios is not None else None,
        puntaje_calidad=float(row.puntaje_calidad) if row.puntaje_calidad is not None else None,
        fecha_ingesta=row.fecha_ingesta,
    )
