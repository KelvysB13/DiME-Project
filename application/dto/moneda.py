from pydantic import BaseModel, field_validator
from datetime import date, datetime
import re


class MonedaBase(BaseModel):
    codigo_moneda: str | None = None
    nombre_moneda: str = ...
    simbolo: str = ...

    model_config = {"extra": "forbid"}


class MonedaCreate(BaseModel):
    codigo_moneda: str = ...
    nombre_moneda: str = ...
    simbolo: str = ...

    model_config = {"extra": "forbid"}

    @field_validator('codigo_moneda')
    @classmethod
    def validate_codigo_moneda_length(cls, v):
        if v is None: return v
        if len(v) > 3:
            raise ValueError('codigo_moneda no puede exceder 3 caracteres')
        return v

    @field_validator('nombre_moneda')
    @classmethod
    def validate_nombre_moneda_length(cls, v):
        if v is None: return v
        if len(v) > 50:
            raise ValueError('nombre_moneda no puede exceder 50 caracteres')
        return v

    @field_validator('simbolo')
    @classmethod
    def validate_simbolo_length(cls, v):
        if v is None: return v
        if len(v) > 5:
            raise ValueError('simbolo no puede exceder 5 caracteres')
        return v


class MonedaUpdate(BaseModel):
    nombre_moneda: str | None = None
    simbolo: str | None = None

    model_config = {"extra": "forbid"}

    @field_validator('nombre_moneda')
    @classmethod
    def validate_nombre_moneda_length(cls, v):
        if v is None: return v
        if len(v) > 50:
            raise ValueError('nombre_moneda no puede exceder 50 caracteres')
        return v

    @field_validator('simbolo')
    @classmethod
    def validate_simbolo_length(cls, v):
        if v is None: return v
        if len(v) > 5:
            raise ValueError('simbolo no puede exceder 5 caracteres')
        return v


class Moneda(MonedaBase):
    codigo_moneda: str

    model_config = {"from_attributes": True, "extra": "forbid"}