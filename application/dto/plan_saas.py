from pydantic import BaseModel, field_validator
from datetime import date, datetime
import re


class Plan_saasBase(BaseModel):
    id_plan: int | None = None
    nombre_plan: str = ...
    descripcion: str | None = None

    model_config = {"extra": "forbid"}


class Plan_saasCreate(BaseModel):
    nombre_plan: str = ...
    descripcion: str | None = None

    model_config = {"extra": "forbid"}

    @field_validator('nombre_plan')
    @classmethod
    def validate_nombre_plan_length(cls, v):
        if v is None: return v
        if len(v) > 50:
            raise ValueError('nombre_plan no puede exceder 50 caracteres')
        return v


class Plan_saasUpdate(BaseModel):
    nombre_plan: str | None = None
    descripcion: str | None = None

    model_config = {"extra": "forbid"}

    @field_validator('nombre_plan')
    @classmethod
    def validate_nombre_plan_length(cls, v):
        if v is None: return v
        if len(v) > 50:
            raise ValueError('nombre_plan no puede exceder 50 caracteres')
        return v


class Plan_saas(Plan_saasBase):
    id_plan: int

    model_config = {"from_attributes": True, "extra": "forbid"}