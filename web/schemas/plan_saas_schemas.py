from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date, datetime
from domain.tools.sanitizer import sanitize_string
from domain.tools.validators import validar_telefono_venezuela
import re


class Plan_saasRequest(BaseModel):
    nombre_plan: str = ...
    descripcion: Optional[str] = None

    model_config = {"extra": "forbid"}


class Plan_saasResponse(Plan_saasRequest):
    id_plan: int

    model_config = {"from_attributes": True}