from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date, datetime
import re


class VendedorBase(BaseModel):
    id_vendedor: Optional[int] = None
    user_name: str = ...
    nombre_tienda: str = ...
    codigo_pais: str = ...
    moneda_local: str = ...
    tipo_plan: Optional[int] = None
    email: str = ...
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    tiempo_token: Optional[str] = None
    esta_activo: bool = 'TRUE'
    fecha_creacion: str = 'CURRENT_TIMESTAMP'

    model_config = {"extra": "forbid"}


class VendedorCreate(BaseModel):
    user_name: str = ...
    nombre_tienda: str = ...
    codigo_pais: str = ...
    moneda_local: str = ...
    tipo_plan: Optional[int] = None
    email: str = ...
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    tiempo_token: Optional[str] = None
    esta_activo: bool = 'TRUE'
    fecha_creacion: str = 'CURRENT_TIMESTAMP'

    model_config = {"extra": "forbid"}

    @field_validator('user_name')
    @classmethod
    def validate_user_name_length(cls, v):
        if v is None: return v
        if len(v) > 50:
            raise ValueError('user_name no puede exceder 50 caracteres')
        return v

    @field_validator('nombre_tienda')
    @classmethod
    def validate_nombre_tienda_length(cls, v):
        if v is None: return v
        if len(v) > 100:
            raise ValueError('nombre_tienda no puede exceder 100 caracteres')
        return v

    @field_validator('codigo_pais')
    @classmethod
    def validate_codigo_pais_length(cls, v):
        if v is None: return v
        if len(v) > 2:
            raise ValueError('codigo_pais no puede exceder 2 caracteres')
        return v

    @field_validator('codigo_pais')
    @classmethod
    def validate_codigo_pais_code(cls, v):
        if v is None: return v
        if not re.match(r'^[A-Za-z0-9\-]+$', str(v)):
            raise ValueError('Solo se permiten caracteres alfanuméricos y guiones')
        return v

    @field_validator('moneda_local')
    @classmethod
    def validate_moneda_local_length(cls, v):
        if v is None: return v
        if len(v) > 3:
            raise ValueError('moneda_local no puede exceder 3 caracteres')
        return v

    @field_validator('email')
    @classmethod
    def validate_email_length(cls, v):
        if v is None: return v
        if len(v) > 255:
            raise ValueError('email no puede exceder 255 caracteres')
        return v

    @field_validator('email')
    @classmethod
    def validate_email_email(cls, v):
        if v is None: return v
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{{2,}}$', str(v)):
            raise ValueError('Formato de email inválido')
        return v

    @field_validator('esta_activo')
    @classmethod
    def validate_esta_activo_bool(cls, v):
        if v is None: return v
        if isinstance(v, bool):
            return v
        if isinstance(v, (int, float)):
            return bool(v)
        if isinstance(v, str):
            return v.lower() in ('true', '1', 'yes', 'si', 'sí')
        return v


class VendedorUpdate(BaseModel):
    user_name: Optional[str] = None
    nombre_tienda: Optional[str] = None
    codigo_pais: Optional[str] = None
    moneda_local: Optional[str] = None
    tipo_plan: Optional[int] = None
    email: Optional[str] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    tiempo_token: Optional[str] = None
    esta_activo: Optional[bool] = None
    fecha_creacion: Optional[str] = None

    model_config = {"extra": "forbid"}

    @field_validator('user_name')
    @classmethod
    def validate_user_name_length(cls, v):
        if v is None: return v
        if len(v) > 50:
            raise ValueError('user_name no puede exceder 50 caracteres')
        return v

    @field_validator('nombre_tienda')
    @classmethod
    def validate_nombre_tienda_length(cls, v):
        if v is None: return v
        if len(v) > 100:
            raise ValueError('nombre_tienda no puede exceder 100 caracteres')
        return v

    @field_validator('codigo_pais')
    @classmethod
    def validate_codigo_pais_length(cls, v):
        if v is None: return v
        if len(v) > 2:
            raise ValueError('codigo_pais no puede exceder 2 caracteres')
        return v

    @field_validator('codigo_pais')
    @classmethod
    def validate_codigo_pais_code(cls, v):
        if v is None: return v
        if not re.match(r'^[A-Za-z0-9\-]+$', str(v)):
            raise ValueError('Solo se permiten caracteres alfanuméricos y guiones')
        return v

    @field_validator('moneda_local')
    @classmethod
    def validate_moneda_local_length(cls, v):
        if v is None: return v
        if len(v) > 3:
            raise ValueError('moneda_local no puede exceder 3 caracteres')
        return v

    @field_validator('email')
    @classmethod
    def validate_email_length(cls, v):
        if v is None: return v
        if len(v) > 255:
            raise ValueError('email no puede exceder 255 caracteres')
        return v

    @field_validator('email')
    @classmethod
    def validate_email_email(cls, v):
        if v is None: return v
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{{2,}}$', str(v)):
            raise ValueError('Formato de email inválido')
        return v

    @field_validator('esta_activo')
    @classmethod
    def validate_esta_activo_bool(cls, v):
        if v is None: return v
        if isinstance(v, bool):
            return v
        if isinstance(v, (int, float)):
            return bool(v)
        if isinstance(v, str):
            return v.lower() in ('true', '1', 'yes', 'si', 'sí')
        return v


class Vendedor(VendedorBase):
    id_vendedor: int

    model_config = {"from_attributes": True, "extra": "forbid"}