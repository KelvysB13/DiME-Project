from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date, datetime
from domain.tools.sanitizer import sanitize_string
from domain.tools.validators import validar_telefono_venezuela
import re


class PaisRequest(BaseModel):
    nombre_pais: str = ...

    model_config = {"extra": "forbid"}


class PaisResponse(PaisRequest):
    codigo_pais: str

    model_config = {"from_attributes": True}