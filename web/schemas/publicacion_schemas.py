from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date, datetime
from domain.tools.sanitizer import sanitize_string
from domain.tools.validators import validar_telefono_venezuela
import re


class PublicacionRequest(BaseModel):
    id_vendedor: int = ...
    ml_item_id: str = ...
    titulo: str = ...
    tipo_publicacion: str = ...
    estado_publicacion: str = ...

    model_config = {"extra": "forbid"}


class PublicacionResponse(PublicacionRequest):
    id_publicacion: int

    model_config = {"from_attributes": True}