from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date, datetime
import re


class Plan_saasBase(BaseModel):
    id_plan: Optional[int] = None
    nombre_plan: str = ...
    descripcion: Optional[str] = None

    model_config = {"extra": "forbid"}


class Plan_saasCreate(BaseModel):
    nombre_plan: str = ...
    descripcion: Optional[str] = None

    model_config = {"extra": "forbid"}

    @field_validator('nombre_plan')
    @classmethod
    def validate_nombre_plan_length(cls, v):
        if v is None: return v
        if len(v) > 50:
            raise ValueError('nombre_plan no puede exceder 50 caracteres')
        return v


class Plan_saasUpdate(BaseModel):
    nombre_plan: Optional[str] = None
    descripcion: Optional[str] = None

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