from pydantic import BaseModel, field_validator
from datetime import date, datetime
import re


class Metricas_costoBase(BaseModel):
    id_metricas_costo: int | None = None
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
    id_vendedor: int | None = None
    fecha_captura: str | None = None
    ventas_cobradas_total: float | None = None
    neto_recibido: float | None = None
    cargos_por_venta: float | None = None
    costos_envio: float | None = None
    inversion_ads: float | None = None
    otros_cargos: float | None = None
    cargos_envio_full: float | None = None
    descuento_reputacion: float | None = None

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