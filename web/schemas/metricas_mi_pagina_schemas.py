from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date, datetime
from domain.tools.sanitizer import sanitize_string
from domain.tools.validators import validar_telefono_venezuela
import re


class Metricas_mi_paginaRequest(BaseModel):
    id_vendedor: int = ...
    fecha_captura: str = ...
    tiene_banner: bool = ...
    tiene_logo: bool = ...
    tiene_carruseles: bool = ...
    categorias_organizadas: bool = ...

    model_config = {"extra": "forbid"}


class Metricas_mi_paginaResponse(Metricas_mi_paginaRequest):
    id_metricas_pagina: int

    model_config = {"from_attributes": True}