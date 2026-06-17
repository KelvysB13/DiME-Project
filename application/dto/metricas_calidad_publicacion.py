from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date, datetime
import re


class Metricas_calidad_publicacionBase(BaseModel):
    id_metricas_calidad_publi: Optional[int] = None
    id_publicacion: int = ...
    fecha_captura: str = 'CURRENT_TIMESTAMP'
    cantidad_fotos: int = '0 CHECK'
    tiene_video: bool = 'FALSE'
    caracteristicas_completas: bool = 'FALSE'
    puntaje_calidad: int = ...

    model_config = {"extra": "forbid"}


class Metricas_calidad_publicacionCreate(BaseModel):
    id_publicacion: int = ...
    fecha_captura: str = 'CURRENT_TIMESTAMP'
    cantidad_fotos: int = '0 CHECK'
    tiene_video: bool = 'FALSE'
    caracteristicas_completas: bool = 'FALSE'
    puntaje_calidad: int = ...

    model_config = {"extra": "forbid"}

    @field_validator('cantidad_fotos')
    @classmethod
    def validate_cantidad_fotos_positive(cls, v):
        if v is None: return v
        if v < 0:
            raise ValueError('cantidad_fotos no puede ser negativo')
        return v

    @field_validator('tiene_video')
    @classmethod
    def validate_tiene_video_bool(cls, v):
        if v is None: return v
        if isinstance(v, bool):
            return v
        if isinstance(v, (int, float)):
            return bool(v)
        if isinstance(v, str):
            return v.lower() in ('true', '1', 'yes', 'si', 'sí')
        return v

    @field_validator('caracteristicas_completas')
    @classmethod
    def validate_caracteristicas_completas_bool(cls, v):
        if v is None: return v
        if isinstance(v, bool):
            return v
        if isinstance(v, (int, float)):
            return bool(v)
        if isinstance(v, str):
            return v.lower() in ('true', '1', 'yes', 'si', 'sí')
        return v


class Metricas_calidad_publicacionUpdate(BaseModel):
    id_publicacion: Optional[int] = None
    fecha_captura: Optional[str] = None
    cantidad_fotos: Optional[int] = None
    tiene_video: Optional[bool] = None
    caracteristicas_completas: Optional[bool] = None
    puntaje_calidad: Optional[int] = None

    model_config = {"extra": "forbid"}

    @field_validator('cantidad_fotos')
    @classmethod
    def validate_cantidad_fotos_positive(cls, v):
        if v is None: return v
        if v < 0:
            raise ValueError('cantidad_fotos no puede ser negativo')
        return v

    @field_validator('tiene_video')
    @classmethod
    def validate_tiene_video_bool(cls, v):
        if v is None: return v
        if isinstance(v, bool):
            return v
        if isinstance(v, (int, float)):
            return bool(v)
        if isinstance(v, str):
            return v.lower() in ('true', '1', 'yes', 'si', 'sí')
        return v

    @field_validator('caracteristicas_completas')
    @classmethod
    def validate_caracteristicas_completas_bool(cls, v):
        if v is None: return v
        if isinstance(v, bool):
            return v
        if isinstance(v, (int, float)):
            return bool(v)
        if isinstance(v, str):
            return v.lower() in ('true', '1', 'yes', 'si', 'sí')
        return v


class Metricas_calidad_publicacion(Metricas_calidad_publicacionBase):
    id_metricas_calidad_publi: int

    model_config = {"from_attributes": True, "extra": "forbid"}