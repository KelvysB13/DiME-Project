from typing import Optional
from pydantic import BaseModel, Field


class BasicData(BaseModel):

    user_name: str = Field(..., min_length=1)
    nombre_tienda: str = Field(..., min_length=1)
    codigo_pais: str = Field(default="MX")
    moneda_local: str = Field(default="MXN")
    tipo_plan: str = Field(default="1")
    email: Optional[str] = None


class BusinessMetrics(BaseModel):

    ventas_totales_periodo: int = Field(default=0)
    fecha_inicio_periodo: str = Field(default="2026-05-01")
    fecha_final_periodo: str = Field(default="2026-05-31")
    ventas_brutas_moneda_local: float = Field(default=0.0)
    ventas_brutas_usd: float = Field(default=0.0)
    unidades_vendidas: int = Field(default=0)
    visitas_totales: int = Field(default=0)
    intencion_compra: int = Field(default=0)
    ventas_concretadas: int = Field(default=0)
    precio_promedio_unidad: float = Field(default=0.0)
    precio_promedio_venta: float = Field(default=0.0)


class CostMetrics(BaseModel):

    ventas_cobradas_total: float = Field(default=0.0)
    neto_recibido: float = Field(default=0.0)
    cargos_por_venta: float = Field(default=0.0)
    costos_envio: float = Field(default=0.0)
    inversion_ads: float = Field(default=0.0)
    otros_cargos: float = Field(default=0.0)
    cargos_envio_full: float = Field(default=0.0)
    descuento_reputacion: float = Field(default=0.0)


class ReputationMetrics(BaseModel):

    total_reclamos: int = Field(default=0)
    total_mediaciones: int = Field(default=0)
    total_canceladas: int = Field(default=0)
    total_envios_incorrectos: int = Field(default=0)
    nivel_reputacion: str = Field(default="green")
    insignia: Optional[str] = None


class FullStockMetrics(BaseModel):

    espacios_p_asignados: int = Field(default=0)
    espacios_g_asignados: int = Field(default=0)
    puntaje_calidad: int = Field(default=100)
    productos_no_aptos_venta: int = Field(default=0)
    productos_sin_rotacion: int = Field(default=0)
    productos_antiguedad: int = Field(default=0)
    productos_exceso_proyeccion: int = Field(default=0)


class MetricsRequest(BaseModel):

    datos_basicos: BasicData
    metrica_negocio: BusinessMetrics = Field(default_factory=BusinessMetrics)
    metrica_costo: CostMetrics = Field(default_factory=CostMetrics)
    metrica_reputacion: ReputationMetrics = Field(default_factory=ReputationMetrics)
    metrica_stock_full: FullStockMetrics = Field(default_factory=FullStockMetrics)
    metrica_mi_pagina: Optional[dict] = None


class MetricsResponse(BaseModel):
    
    status: str
    message: str
