from pydantic import BaseModel, field_validator
from datetime import date, datetime
import re


class Metricas_reputacionBase(BaseModel):
    id_metricas_reputacion: int | None = None
    id_vendedor: int = ...
    fecha_captura: str = 'CURRENT_TIMESTAMP'
    ventas_totales_periodo: int = '0 CHECK'
    total_reclamos: int = '0 CHECK'
    total_mediaciones: int = '0 CHECK'
    total_canceladas: int = '0 CHECK'
    total_envios_incorrectos: int = '0 CHECK'
    nivel_reputacion: str = ...
    insignia: str | None = None

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
    insignia: str | None = None

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
    id_vendedor: int | None = None
    fecha_captura: str | None = None
    ventas_totales_periodo: int | None = None
    total_reclamos: int | None = None
    total_mediaciones: int | None = None
    total_canceladas: int | None = None
    total_envios_incorrectos: int | None = None
    nivel_reputacion: str | None = None
    insignia: str | None = None

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