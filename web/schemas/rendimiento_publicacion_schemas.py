from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date, datetime
from domain.tools.sanitizer import sanitize_string
from domain.tools.validators import validar_telefono_venezuela
import re


class Rendimiento_publicacionRequest(BaseModel):
    id_publicacion: int = ...
    fecha_captura: str = ...
    fecha_inicio_periodo: date = ...
    fecha_fin_periodo: date = ...
    visitas: int = ...
    ventas: int = ...

    model_config = {"extra": "forbid"}


class Rendimiento_publicacionResponse(Rendimiento_publicacionRequest):
    id_rendimiento_publi: int

    model_config = {"from_attributes": True}