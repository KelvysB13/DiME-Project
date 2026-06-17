from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date, datetime
import re


class Metricas_reputacionBase(BaseModel):
    id_metricas_reputacion: Optional[int] = None
    id_vendedor: int = ...
    fecha_captura: str = 'CURRENT_TIMESTAMP'
    ventas_totales_periodo: int = '0 CHECK'
    total_reclamos: int = '0 CHECK'
    total_mediaciones: int = '0 CHECK'
    total_canceladas: int = '0 CHECK'
    total_envios_incorrectos: int = '0 CHECK'
    nivel_reputacion: str = ...
    insignia: Optional[str] = None

    model_config = {"extra": "forbid"}


class Metricas_reputacionCreate(BaseModel):
    id_vendedor: int = ...
    fecha_captura: str = 'CURRENT_TIMESTAMP'
    ventas_totales_periodo: int = '0 CHECK'
    total_reclamos: int = '0 CHECK'
    total_mediaciones: int = '0 CHECK'
    total_canceladas: int = '0 CHECK'
    total_envios_incorrectos: int = '0 CHECK'
    nivel_reputacion: str = ...
    insignia: Optional[str] = None

    model_config = {"extra": "forbid"}

    @field_validator('nivel_reputacion')
    @classmethod
    def validate_nivel_reputacion_length(cls, v):
        if v is None: return v
        if len(v) > 20:
            raise ValueError('nivel_reputacion no puede exceder 20 caracteres')
        return v

    @field_validator('insignia')
    @classmethod
    def validate_insignia_length(cls, v):
        if v is None: return v
        if len(v) > 20:
            raise ValueError('insignia no puede exceder 20 caracteres')
        return v


class Metricas_reputacionUpdate(BaseModel):
    id_vendedor: Optional[int] = None
    fecha_captura: Optional[str] = None
    ventas_totales_periodo: Optional[int] = None
    total_reclamos: Optional[int] = None
    total_mediaciones: Optional[int] = None
    total_canceladas: Optional[int] = None
    total_envios_incorrectos: Optional[int] = None
    nivel_reputacion: Optional[str] = None
    insignia: Optional[str] = None

    model_config = {"extra": "forbid"}

    @field_validator('nivel_reputacion')
    @classmethod
    def validate_nivel_reputacion_length(cls, v):
        if v is None: return v
        if len(v) > 20:
            raise ValueError('nivel_reputacion no puede exceder 20 caracteres')
        return v

    @field_validator('insignia')
    @classmethod
    def validate_insignia_length(cls, v):
        if v is None: return v
        if len(v) > 20:
            raise ValueError('insignia no puede exceder 20 caracteres')
        return v


class Metricas_reputacion(Metricas_reputacionBase):
    id_metricas_reputacion: int

    model_config = {"from_attributes": True, "extra": "forbid"}