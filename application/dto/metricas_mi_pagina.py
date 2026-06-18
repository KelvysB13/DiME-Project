from pydantic import BaseModel, field_validator
from datetime import date, datetime
import re


class Metricas_mi_paginaBase(BaseModel):
    id_metricas_pagina: int | None = None
    id_vendedor: int = ...
    fecha_captura: str = 'CURRENT_TIMESTAMP'
    tiene_banner: bool = 'FALSE'
    tiene_logo: bool = 'FALSE'
    tiene_carruseles: bool = 'FALSE'
    categorias_organizadas: bool = 'FALSE'

    model_config = {"extra": "forbid"}


class Metricas_mi_paginaCreate(BaseModel):
    id_vendedor: int = ...
    fecha_captura: str = 'CURRENT_TIMESTAMP'
    tiene_banner: bool = 'FALSE'
    tiene_logo: bool = 'FALSE'
    tiene_carruseles: bool = 'FALSE'
    categorias_organizadas: bool = 'FALSE'

    model_config = {"extra": "forbid"}

    @field_validator('tiene_banner')
    @classmethod
    def validate_tiene_banner_bool(cls, v):
        if v is None: return v
        if isinstance(v, bool):
            return v
        if isinstance(v, (int, float)):
            return bool(v)
        if isinstance(v, str):
            return v.lower() in ('true', '1', 'yes', 'si', 'sí')
        return v

    @field_validator('tiene_logo')
    @classmethod
    def validate_tiene_logo_bool(cls, v):
        if v is None: return v
        if isinstance(v, bool):
            return v
        if isinstance(v, (int, float)):
            return bool(v)
        if isinstance(v, str):
            return v.lower() in ('true', '1', 'yes', 'si', 'sí')
        return v

    @field_validator('tiene_carruseles')
    @classmethod
    def validate_tiene_carruseles_bool(cls, v):
        if v is None: return v
        if isinstance(v, bool):
            return v
        if isinstance(v, (int, float)):
            return bool(v)
        if isinstance(v, str):
            return v.lower() in ('true', '1', 'yes', 'si', 'sí')
        return v

    @field_validator('categorias_organizadas')
    @classmethod
    def validate_categorias_organizadas_bool(cls, v):
        if v is None: return v
        if isinstance(v, bool):
            return v
        if isinstance(v, (int, float)):
            return bool(v)
        if isinstance(v, str):
            return v.lower() in ('true', '1', 'yes', 'si', 'sí')
        return v


class Metricas_mi_paginaUpdate(BaseModel):
    id_vendedor: int | None = None
    fecha_captura: str | None = None
    tiene_banner: bool | None = None
    tiene_logo: bool | None = None
    tiene_carruseles: bool | None = None
    categorias_organizadas: bool | None = None

    model_config = {"extra": "forbid"}

    @field_validator('tiene_banner')
    @classmethod
    def validate_tiene_banner_bool(cls, v):
        if v is None: return v
        if isinstance(v, bool):
            return v
        if isinstance(v, (int, float)):
            return bool(v)
        if isinstance(v, str):
            return v.lower() in ('true', '1', 'yes', 'si', 'sí')
        return v

    @field_validator('tiene_logo')
    @classmethod
    def validate_tiene_logo_bool(cls, v):
        if v is None: return v
        if isinstance(v, bool):
            return v
        if isinstance(v, (int, float)):
            return bool(v)
        if isinstance(v, str):
            return v.lower() in ('true', '1', 'yes', 'si', 'sí')
        return v

    @field_validator('tiene_carruseles')
    @classmethod
    def validate_tiene_carruseles_bool(cls, v):
        if v is None: return v
        if isinstance(v, bool):
            return v
        if isinstance(v, (int, float)):
            return bool(v)
        if isinstance(v, str):
            return v.lower() in ('true', '1', 'yes', 'si', 'sí')
        return v

    @field_validator('categorias_organizadas')
    @classmethod
    def validate_categorias_organizadas_bool(cls, v):
        if v is None: return v
        if isinstance(v, bool):
            return v
        if isinstance(v, (int, float)):
            return bool(v)
        if isinstance(v, str):
            return v.lower() in ('true', '1', 'yes', 'si', 'sí')
        return v


class Metricas_mi_pagina(Metricas_mi_paginaBase):
    id_metricas_pagina: int

    model_config = {"from_attributes": True, "extra": "forbid"}