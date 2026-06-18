from pydantic import BaseModel, field_validator
from datetime import date, datetime
import re


class Reportes_diagnosticoBase(BaseModel):
    id_reporte: int | None = None
    id_vendedor: int = ...
    fecha_generacion: date = 'CURRENT_DATE'
    fecha_inicio_periodo: date = ...
    fecha_fin_periodo: date = ...
    resumen_ejecutivo: str | None = None
    plan_accion: dict = '{}'

    model_config = {"extra": "forbid"}


class Reportes_diagnosticoCreate(BaseModel):
    id_vendedor: int = ...
    fecha_generacion: date = 'CURRENT_DATE'
    fecha_inicio_periodo: date = ...
    fecha_fin_periodo: date = ...
    resumen_ejecutivo: str | None = None
    plan_accion: dict = '{}'

    model_config = {"extra": "forbid"}

    @field_validator('fecha_generacion')
    @classmethod
    def validate_fecha_generacion_date(cls, v):
        if v is None: return v
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError('Formato de fecha inválido, use YYYY-MM-DD')
        return v

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


class Reportes_diagnosticoUpdate(BaseModel):
    id_vendedor: int | None = None
    fecha_generacion: date | None = None
    fecha_inicio_periodo: date | None = None
    fecha_fin_periodo: date | None = None
    resumen_ejecutivo: str | None = None
    plan_accion: dict | None = None

    model_config = {"extra": "forbid"}

    @field_validator('fecha_generacion')
    @classmethod
    def validate_fecha_generacion_date(cls, v):
        if v is None: return v
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError('Formato de fecha inválido, use YYYY-MM-DD')
        return v

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


class Reportes_diagnostico(Reportes_diagnosticoBase):
    id_reporte: int

    model_config = {"from_attributes": True, "extra": "forbid"}