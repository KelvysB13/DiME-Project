from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date, datetime
from domain.tools.sanitizer import sanitize_string
from domain.tools.validators import validar_telefono_venezuela
import re


class VendedorRequest(BaseModel):
    user_name: str = ...
    nombre_tienda: str = ...
    codigo_pais: str = ...
    moneda_local: str = ...
    tipo_plan: Optional[int] = None
    email: str = ...
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    tiempo_token: Optional[str] = None
    esta_activo: bool = ...
    fecha_creacion: str = ...

    model_config = {"extra": "forbid"}


class VendedorResponse(VendedorRequest):
    id_vendedor: int

    model_config = {"from_attributes": True}