from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, Field, field_validator


class HistDiagnosticoReputacion(BaseModel):

    id_vendedor: int = Field(..., ge=1, description="ID del vendedor")
    tasa_reclamos: Optional[float] = Field(None, ge=0, description="Porcentaje de reclamos sobre ventas")
    tasa_cancelaciones: Optional[float] = Field(None, ge=0, description="Porcentaje de cancelaciones sobre ventas")
    tasa_mediaciones: Optional[float] = Field(None, ge=0, description="Porcentaje de mediaciones sobre ventas")
    tasa_envios_incorrectos: Optional[float] = Field(None, ge=0, description="Porcentaje de envíos incorrectos sobre ventas")
    nivel_reputacion: Optional[str] = Field(None, min_length=1, description="Nivel de reputación (green, yellow, red)")
    insignia: Optional[str] = Field(None, description="Insignia del vendedor (platinum, gold, leader, etc.)")
    fecha_captura: Optional[date] = Field(None, description="Fecha de captura de la métrica")
    fecha_ingesta: Optional[datetime] = Field(None, description="Momento de ingesta del registro")


class HistDiagnosticoFinanzas(BaseModel):

    id_vendedor: int = Field(..., ge=1, description="ID del vendedor")
    cvr_global: Optional[float] = Field(None, ge=0, le=100, description="Tasa de conversión global")
    margen_neto_real: Optional[float] = Field(None, ge=0, le=100, description="Margen neto real")
    ticket_promedio: Optional[float] = Field(None, ge=0, description="Ticket promedio por unidad vendida")
    carga_total_costos: Optional[float] = Field(None, ge=0, description="Carga total de costos sobre ventas brutas")
    ratio_intencion_compra: Optional[float] = Field(None, ge=0, le=100, description="Ratio de intención de compra")
    descuento_reputacion: Optional[float] = Field(None, ge=0, description="Descuento por reputación sobre ventas brutas")
    tasa_cobro_efectivo: Optional[float] = Field(None, ge=0, le=100, description="Tasa de cobro efectivo")
    crecimiento_mom: Optional[float] = Field(None, description="Crecimiento mes contra mes")
    ventas_periodo_actual: Optional[int] = Field(None, ge=0, description="Ventas concretadas en el período actual")
    fecha_inicio_periodo: Optional[date] = Field(None, description="Inicio del período analizado")
    fecha_fin_periodo: Optional[date] = Field(None, description="Fin del período analizado")
    fecha_ingesta: Optional[datetime] = Field(None, description="Momento de ingesta del registro")

    @field_validator("fecha_fin_periodo")
    @classmethod
    def validar_fechas(cls, v, info):
        inicio = info.data.get("fecha_inicio_periodo")
        if inicio and v and v < inicio:
            raise ValueError("fecha_fin_periodo debe ser >= fecha_inicio_periodo")
        return v


class HistDiagnosticoPublicaciones(BaseModel):

    id_vendedor: int = Field(..., ge=1, description="ID del vendedor")
    total_publicaciones: Optional[int] = Field(None, ge=0, description="Cantidad total de publicaciones activas")
    cvr_publicacion: Optional[float] = Field(None, ge=0, le=100, description="CVR promedio por publicación")
    pct_catalogo_completo: Optional[float] = Field(None, ge=0, le=100, description="Porcentaje de publicaciones con características completas")
    pct_publicaciones_con_video: Optional[float] = Field(None, ge=0, le=100, description="Porcentaje de publicaciones con video")
    fecha_ingesta: Optional[datetime] = Field(None, description="Momento de ingesta del registro")


class HistDiagnosticoAds(BaseModel):

    id_vendedor: int = Field(..., ge=1, description="ID del vendedor")
    roas: Optional[float] = Field(None, ge=0, description="Return On Ad Spend (ventas/inversión ads)")
    acos: Optional[float] = Field(None, ge=0, description="Advertising Cost of Sales")
    inversion_ads_sobre_ventas: Optional[float] = Field(None, ge=0, description="Inversión en ads como porcentaje de ventas")
    inversion_ads: Optional[float] = Field(None, ge=0, description="Inversión total en Mercado Ads en moneda local")
    fecha_ingesta: Optional[datetime] = Field(None, description="Momento de ingesta del registro")


class HistDiagnosticoStock(BaseModel):

    id_vendedor: int = Field(..., ge=1, description="ID del vendedor")
    dead_stock_rate: Optional[float] = Field(None, ge=0, le=100, description="Porcentaje de productos sin rotación")
    antiguedad_riesgo: Optional[float] = Field(None, ge=0, le=100, description="Porcentaje de productos con antigüedad de riesgo")
    productos_no_aptos: Optional[float] = Field(None, ge=0, le=100, description="Porcentaje de productos no aptos para venta")
    overstock_rate: Optional[float] = Field(None, ge=0, le=100, description="Porcentaje de productos con exceso de proyección")
    utilizacion_espacios: Optional[float] = Field(None, ge=0, le=100, description="Porcentaje de utilización de espacios")
    puntaje_calidad: Optional[float] = Field(None, ge=0, le=100, description="Puntaje de calidad del stock (0-100)")
    fecha_ingesta: Optional[datetime] = Field(None, description="Momento de ingesta del registro")
