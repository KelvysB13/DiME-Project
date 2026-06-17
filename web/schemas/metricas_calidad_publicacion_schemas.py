from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date, datetime
from domain.tools.sanitizer import sanitize_string
from domain.tools.validators import validar_telefono_venezuela
import re


class Metricas_calidad_publicacionRequest(BaseModel):
    id_publicacion: int = ...
    fecha_captura: str = ...
    cantidad_fotos: int = ...
    tiene_video: bool = ...
    caracteristicas_completas: bool = ...
    puntaje_calidad: int = ...

    model_config = {"extra": "forbid"}


class Metricas_calidad_publicacionResponse(Metricas_calidad_publicacionRequest):
    id_metricas_calidad_publi: int

    model_config = {"from_attributes": True}