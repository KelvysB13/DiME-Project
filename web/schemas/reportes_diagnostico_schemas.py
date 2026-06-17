from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date, datetime
from domain.tools.sanitizer import sanitize_string
from domain.tools.validators import validar_telefono_venezuela
import re


class Reportes_diagnosticoRequest(BaseModel):
    id_vendedor: int = ...
    fecha_generacion: date = ...
    fecha_inicio_periodo: date = ...
    fecha_fin_periodo: date = ...
    resumen_ejecutivo: Optional[str] = None
    plan_accion: dict = ...

    model_config = {"extra": "forbid"}


class Reportes_diagnosticoResponse(Reportes_diagnosticoRequest):
    id_reporte: int

    model_config = {"from_attributes": True}