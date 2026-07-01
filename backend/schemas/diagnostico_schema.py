from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, Field, field_validator


class MvDiagnosticoReputacion(BaseModel):

    tasa_reclamos: float = Field(..., ge=0, description="Porcentaje de reclamos sobre ventas")
    tasa_cancelaciones: float = Field(..., ge=0, description="Porcentaje de cancelaciones sobre ventas")
    tasa_mediaciones: float = Field(..., ge=0, description="Porcentaje de mediaciones sobre ventas")
    tasa_envios_incorrectos: float = Field(..., ge=0, description="Porcentaje de envíos incorrectos sobre ventas")
    nivel_reputacion: str = Field(..., min_length=1, description="Nivel de reputación (green, yellow, red)")
    insignia: Optional[str] = Field(None, description="Insignia del vendedor (platinum, gold, leader, etc.)")
    fecha_captura: date = Field(..., description="Fecha de captura de la métrica")


class MvDiagnosticoFinanzas(BaseModel):

    cvr_global: float = Field(..., ge=0, le=100, description="Tasa de conversión global (ventas/visitas) * 100")
    margen_neto_real: float = Field(..., ge=0, le=100, description="Margen neto real (neto/ventas_brutas) * 100")
    ticket_promedio: float = Field(..., ge=0, description="Ticket promedio por unidad vendida")
    carga_total_costos: float = Field(..., ge=0, description="Carga total de costos sobre ventas brutas")
    ratio_intencion_compra: float = Field(..., ge=0, le=100, description="Ratio de intención de compra")
    descuento_reputacion: float = Field(..., ge=0, description="Descuento por reputación sobre ventas brutas")
    tasa_cobro_efectivo: float = Field(..., ge=0, le=100, description="Tasa de cobro efectivo")
    crecimiento_mom: Optional[float] = Field(None, description="Crecimiento mes contra mes (NULL si no hay histórico)")
    ventas_periodo_actual: int = Field(..., ge=0, description="Ventas concretadas en el período actual")
    fecha_inicio_periodo: date = Field(..., description="Inicio del período analizado")
    fecha_fin_periodo: date = Field(..., description="Fin del período analizado")

    @field_validator("fecha_fin_periodo")
    @classmethod
    def validar_fechas(cls, v, info):
        inicio = info.data.get("fecha_inicio_periodo")
        if inicio and v < inicio:
            raise ValueError("fecha_fin_periodo debe ser >= fecha_inicio_periodo")
        return v


class MvDiagnosticoAds(BaseModel):

    roas: float = Field(..., ge=0, description="Return On Ad Spend (ventas/inversión ads)")
    acos: float = Field(..., ge=0, description="Advertising Cost of Sales (inversión ads/ventas) * 100")
    inversion_ads_sobre_ventas: float = Field(..., ge=0, description="Inversión en ads como porcentaje de ventas")
    inversion_ads: float = Field(..., ge=0, description="Inversión total en Mercado Ads en moneda local")


class MvDiagnosticoStock(BaseModel):

    dead_stock_rate: float = Field(..., ge=0, le=100, description="Porcentaje de productos sin rotación")
    antiguedad_riesgo: float = Field(..., ge=0, le=100, description="Porcentaje de productos con antigüedad de riesgo")
    productos_no_aptos: float = Field(..., ge=0, le=100, description="Porcentaje de productos no aptos para venta")
    overstock_rate: float = Field(..., ge=0, le=100, description="Porcentaje de productos con exceso de proyección")
    utilizacion_espacios: float = Field(..., ge=0, le=100, description="Porcentaje de utilización de espacios")
    puntaje_calidad: int = Field(..., ge=0, le=100, description="Puntaje de calidad del stock (0-100)")


class MvDiagnosticoPublicaciones(BaseModel):

    total_publicaciones: int = Field(..., ge=0, description="Cantidad total de publicaciones activas")
    cvr_publicacion: float = Field(..., ge=0, le=100, description="CVR promedio por publicación")
    pct_catalogo_completo: float = Field(..., ge=0, le=100, description="Porcentaje de publicaciones con características completas")
    pct_publicaciones_con_video: float = Field(..., ge=0, le=100, description="Porcentaje de publicaciones con video")


class MetricaCalidadPublicacion(BaseModel):

    id_publicacion: int = Field(..., ge=1, description="ID de la publicación evaluada")
    fecha_captura: datetime = Field(..., description="Momento de captura de la métrica")
    cantidad_fotos: int = Field(..., ge=0, description="Cantidad de fotos de la publicación")
    tiene_video: bool = Field(..., description="Indica si la publicación tiene video")
    caracteristicas_completas: bool = Field(..., description="Indica si todas las características están completas")
    puntaje_calidad: int = Field(..., ge=0, le=100, description="Puntaje de calidad de ML (0-100)")
