from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date, datetime
import re


class PublicacionBase(BaseModel):
    id_publicacion: Optional[int] = None
    id_vendedor: int = ...
    ml_item_id: str = ...
    titulo: str = ...
    tipo_publicacion: str = ...
    estado_publicacion: str = ...

    model_config = {"extra": "forbid"}


class PublicacionCreate(BaseModel):
    id_vendedor: int = ...
    ml_item_id: str = ...
    titulo: str = ...
    tipo_publicacion: str = ...
    estado_publicacion: str = ...

    model_config = {"extra": "forbid"}

    @field_validator('ml_item_id')
    @classmethod
    def validate_ml_item_id_length(cls, v):
        if v is None: return v
        if len(v) > 20:
            raise ValueError('ml_item_id no puede exceder 20 caracteres')
        return v

    @field_validator('titulo')
    @classmethod
    def validate_titulo_length(cls, v):
        if v is None: return v
        if len(v) > 100:
            raise ValueError('titulo no puede exceder 100 caracteres')
        return v

    @field_validator('tipo_publicacion')
    @classmethod
    def validate_tipo_publicacion_length(cls, v):
        if v is None: return v
        if len(v) > 20:
            raise ValueError('tipo_publicacion no puede exceder 20 caracteres')
        return v

    @field_validator('estado_publicacion')
    @classmethod
    def validate_estado_publicacion_length(cls, v):
        if v is None: return v
        if len(v) > 20:
            raise ValueError('estado_publicacion no puede exceder 20 caracteres')
        return v


class PublicacionUpdate(BaseModel):
    id_vendedor: Optional[int] = None
    ml_item_id: Optional[str] = None
    titulo: Optional[str] = None
    tipo_publicacion: Optional[str] = None
    estado_publicacion: Optional[str] = None

    model_config = {"extra": "forbid"}

    @field_validator('ml_item_id')
    @classmethod
    def validate_ml_item_id_length(cls, v):
        if v is None: return v
        if len(v) > 20:
            raise ValueError('ml_item_id no puede exceder 20 caracteres')
        return v

    @field_validator('titulo')
    @classmethod
    def validate_titulo_length(cls, v):
        if v is None: return v
        if len(v) > 100:
            raise ValueError('titulo no puede exceder 100 caracteres')
        return v

    @field_validator('tipo_publicacion')
    @classmethod
    def validate_tipo_publicacion_length(cls, v):
        if v is None: return v
        if len(v) > 20:
            raise ValueError('tipo_publicacion no puede exceder 20 caracteres')
        return v

    @field_validator('estado_publicacion')
    @classmethod
    def validate_estado_publicacion_length(cls, v):
        if v is None: return v
        if len(v) > 20:
            raise ValueError('estado_publicacion no puede exceder 20 caracteres')
        return v


class Publicacion(PublicacionBase):
    id_publicacion: int

    model_config = {"from_attributes": True, "extra": "forbid"}