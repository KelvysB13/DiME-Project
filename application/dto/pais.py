from pydantic import BaseModel, field_validator
from datetime import date, datetime
import re


class PaisBase(BaseModel):
    codigo_pais: str | None = None
    nombre_pais: str = ...

    model_config = {"extra": "forbid"}


class PaisCreate(BaseModel):
    codigo_pais: str = ...
    nombre_pais: str = ...

    model_config = {"extra": "forbid"}

    @field_validator('codigo_pais')
    @classmethod
    def validate_codigo_pais_length(cls, v):
        if v is None: return v
        if len(v) > 2:
            raise ValueError('codigo_pais no puede exceder 2 caracteres')
        return v

    @field_validator('nombre_pais')
    @classmethod
    def validate_nombre_pais_length(cls, v):
        if v is None: return v
        if len(v) > 60:
            raise ValueError('nombre_pais no puede exceder 60 caracteres')
        return v


class PaisUpdate(BaseModel):
    nombre_pais: str | None = None

    model_config = {"extra": "forbid"}

    @field_validator('nombre_pais')
    @classmethod
    def validate_nombre_pais_length(cls, v):
        if v is None: return v
        if len(v) > 60:
            raise ValueError('nombre_pais no puede exceder 60 caracteres')
        return v


class Pais(PaisBase):
    codigo_pais: str

    model_config = {"from_attributes": True, "extra": "forbid"}