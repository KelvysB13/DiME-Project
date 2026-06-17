from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date, datetime
import re


class Metricas_costoBase(BaseModel):
    id_metricas_costo: Optional[int] = None
    id_vendedor: int = ...
    fecha_captura: str = 'CURRENT_TIMESTAMP'
    ventas_cobradas_total: float = '0.00'
    neto_recibido: float = '0.00'
    cargos_por_venta: float = '0.00 CHECK'
    costos_envio: float = '0.00 CHECK'
    inversion_ads: float = '0.00 CHECK'
    otros_cargos: float = '0.00 CHECK'
    cargos_envio_full: float = '0.00 CHECK'
    descuento_reputacion: float = '0.00'

    model_config = {"extra": "forbid"}


class Metricas_costoCreate(BaseModel):
    id_vendedor: int = ...
    fecha_captura: str = 'CURRENT_TIMESTAMP'
    ventas_cobradas_total: float = '0.00'
    neto_recibido: float = '0.00'
    cargos_por_venta: float = '0.00 CHECK'
    costos_envio: float = '0.00 CHECK'
    inversion_ads: float = '0.00 CHECK'
    otros_cargos: float = '0.00 CHECK'
    cargos_envio_full: float = '0.00 CHECK'
    descuento_reputacion: float = '0.00'

    model_config = {"extra": "forbid"}

    @field_validator('ventas_cobradas_total')
    @classmethod
    def validate_ventas_cobradas_total_positive(cls, v):
        if v is None: return v
        if v < 0:
            raise ValueError('ventas_cobradas_total no puede ser negativo')
        return v

    @field_validator('costos_envio')
    @classmethod
    def validate_costos_envio_positive(cls, v):
        if v is None: return v
        if v < 0:
            raise ValueError('costos_envio no puede ser negativo')
        return v


class Metricas_costoUpdate(BaseModel):
    id_vendedor: Optional[int] = None
    fecha_captura: Optional[str] = None
    ventas_cobradas_total: Optional[float] = None
    neto_recibido: Optional[float] = None
    cargos_por_venta: Optional[float] = None
    costos_envio: Optional[float] = None
    inversion_ads: Optional[float] = None
    otros_cargos: Optional[float] = None
    cargos_envio_full: Optional[float] = None
    descuento_reputacion: Optional[float] = None

    model_config = {"extra": "forbid"}

    @field_validator('ventas_cobradas_total')
    @classmethod
    def validate_ventas_cobradas_total_positive(cls, v):
        if v is None: return v
        if v < 0:
            raise ValueError('ventas_cobradas_total no puede ser negativo')
        return v

    @field_validator('costos_envio')
    @classmethod
    def validate_costos_envio_positive(cls, v):
        if v is None: return v
        if v < 0:
            raise ValueError('costos_envio no puede ser negativo')
        return v


class Metricas_costo(Metricas_costoBase):
    id_metricas_costo: int

    model_config = {"from_attributes": True, "extra": "forbid"}