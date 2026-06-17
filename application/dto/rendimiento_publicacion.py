from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date, datetime
import re


class Rendimiento_publicacionBase(BaseModel):
    id_rendimiento_publi: Optional[int] = None
    id_publicacion: int = ...
    fecha_captura: str = 'CURRENT_TIMESTAMP'
    fecha_inicio_periodo: date = ...
    fecha_fin_periodo: date = ...
    visitas: int = '0 CHECK'
    ventas: int = '0 CHECK'

    model_config = {"extra": "forbid"}


class Rendimiento_publicacionCreate(BaseModel):
    id_publicacion: int = ...
    fecha_captura: str = 'CURRENT_TIMESTAMP'
    fecha_inicio_periodo: date = ...
    fecha_fin_periodo: date = ...
    visitas: int = '0 CHECK'
    ventas: int = '0 CHECK'

    model_config = {"extra": "forbid"}

    @field_validator('fecha_inicio_periodo')
    @classmethod
    def validate_fecha_inicio_periodo_date(cls, v):
        if v is None: return v
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError('Formato de fecha inválido, use YYYY-MM-DD')
        return v

    @field_validator('fecha_fin_periodo')
    @classmethod
    def validate_fecha_fin_periodo_date(cls, v):
        if v is None: return v
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError('Formato de fecha inválido, use YYYY-MM-DD')
        return v
        from datetime import date
        if v < date.today():
            raise ValueError(f'{py_name} debe ser una fecha futura')


class Rendimiento_publicacionUpdate(BaseModel):
    id_publicacion: Optional[int] = None
    fecha_captura: Optional[str] = None
    fecha_inicio_periodo: Optional[date] = None
    fecha_fin_periodo: Optional[date] = None
    visitas: Optional[int] = None
    ventas: Optional[int] = None

    model_config = {"extra": "forbid"}

    @field_validator('fecha_inicio_periodo')
    @classmethod
    def validate_fecha_inicio_periodo_date(cls, v):
        if v is None: return v
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError('Formato de fecha inválido, use YYYY-MM-DD')
        return v

    @field_validator('fecha_fin_periodo')
    @classmethod
    def validate_fecha_fin_periodo_date(cls, v):
        if v is None: return v
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError('Formato de fecha inválido, use YYYY-MM-DD')
        return v
        from datetime import date
        if v < date.today():
            raise ValueError(f'{py_name} debe ser una fecha futura')


class Rendimiento_publicacion(Rendimiento_publicacionBase):
    id_rendimiento_publi: int

    model_config = {"from_attributes": True, "extra": "forbid"}