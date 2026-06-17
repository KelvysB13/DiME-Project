from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date, datetime
import re


class Metricas_stock_fullBase(BaseModel):
    id_metricas_stock: Optional[int] = None
    id_vendedor: int = ...
    fecha_captura: str = 'CURRENT_TIMESTAMP'
    espacios_p_asignados: int = '0 CHECK'
    espacios_g_asignados: int = '0 CHECK'
    puntaje_calidad: int = ...
    productos_no_aptos_venta: int = '0 CHECK'
    productos_sin_rotacion: int = '0 CHECK'
    productos_antiguedad: int = '0 CHECK'
    productos_exceso_proyeccion: int = '0 CHECK'

    model_config = {"extra": "forbid"}


class Metricas_stock_fullCreate(BaseModel):
    id_vendedor: int = ...
    fecha_captura: str = 'CURRENT_TIMESTAMP'
    espacios_p_asignados: int = '0 CHECK'
    espacios_g_asignados: int = '0 CHECK'
    puntaje_calidad: int = ...
    productos_no_aptos_venta: int = '0 CHECK'
    productos_sin_rotacion: int = '0 CHECK'
    productos_antiguedad: int = '0 CHECK'
    productos_exceso_proyeccion: int = '0 CHECK'

    model_config = {"extra": "forbid"}

    @field_validator('productos_antiguedad')
    @classmethod
    def validate_productos_antiguedad_positive(cls, v):
        if v is None: return v
        if v < 0:
            raise ValueError('productos_antiguedad no puede ser negativo')
        return v


class Metricas_stock_fullUpdate(BaseModel):
    id_vendedor: Optional[int] = None
    fecha_captura: Optional[str] = None
    espacios_p_asignados: Optional[int] = None
    espacios_g_asignados: Optional[int] = None
    puntaje_calidad: Optional[int] = None
    productos_no_aptos_venta: Optional[int] = None
    productos_sin_rotacion: Optional[int] = None
    productos_antiguedad: Optional[int] = None
    productos_exceso_proyeccion: Optional[int] = None

    model_config = {"extra": "forbid"}

    @field_validator('productos_antiguedad')
    @classmethod
    def validate_productos_antiguedad_positive(cls, v):
        if v is None: return v
        if v < 0:
            raise ValueError('productos_antiguedad no puede ser negativo')
        return v


class Metricas_stock_full(Metricas_stock_fullBase):
    id_metricas_stock: int

    model_config = {"from_attributes": True, "extra": "forbid"}