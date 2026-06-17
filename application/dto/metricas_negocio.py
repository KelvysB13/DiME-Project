from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date, datetime
import re


class Metricas_negocioBase(BaseModel):
    id_metricas_negocio: Optional[int] = None
    id_vendedor: int = ...
    fecha_captura: str = 'CURRENT_TIMESTAMP'
    fecha_inicio_periodo: date = ...
    fecha_fin_periodo: date = ...
    ventas_brutas_moneda_local: float = '0.00 CHECK'
    ventas_brutas_usd: float = '0.00 CHECK'
    unidades_vendidas: int = '0 CHECK'
    visitas_totales: int = '0 CHECK'
    intencion_compra: int = '0 CHECK'
    ventas_concretadas: int = '0 CHECK'
    precio_promedio_unidad: float = '0.00 CHECK'
    precio_promedio_venta: float = '0.00 CHECK'

    model_config = {"extra": "forbid"}


class Metricas_negocioCreate(BaseModel):
    id_vendedor: int = ...
    fecha_captura: str = 'CURRENT_TIMESTAMP'
    fecha_inicio_periodo: date = ...
    fecha_fin_periodo: date = ...
    ventas_brutas_moneda_local: float = '0.00 CHECK'
    ventas_brutas_usd: float = '0.00 CHECK'
    unidades_vendidas: int = '0 CHECK'
    visitas_totales: int = '0 CHECK'
    intencion_compra: int = '0 CHECK'
    ventas_concretadas: int = '0 CHECK'
    precio_promedio_unidad: float = '0.00 CHECK'
    precio_promedio_venta: float = '0.00 CHECK'

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

    @field_validator('precio_promedio_unidad')
    @classmethod
    def validate_precio_promedio_unidad_positive(cls, v):
        if v is None: return v
        if v < 0:
            raise ValueError('precio_promedio_unidad no puede ser negativo')
        return v

    @field_validator('precio_promedio_venta')
    @classmethod
    def validate_precio_promedio_venta_positive(cls, v):
        if v is None: return v
        if v < 0:
            raise ValueError('precio_promedio_venta no puede ser negativo')
        return v


class Metricas_negocioUpdate(BaseModel):
    id_vendedor: Optional[int] = None
    fecha_captura: Optional[str] = None
    fecha_inicio_periodo: Optional[date] = None
    fecha_fin_periodo: Optional[date] = None
    ventas_brutas_moneda_local: Optional[float] = None
    ventas_brutas_usd: Optional[float] = None
    unidades_vendidas: Optional[int] = None
    visitas_totales: Optional[int] = None
    intencion_compra: Optional[int] = None
    ventas_concretadas: Optional[int] = None
    precio_promedio_unidad: Optional[float] = None
    precio_promedio_venta: Optional[float] = None

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

    @field_validator('precio_promedio_unidad')
    @classmethod
    def validate_precio_promedio_unidad_positive(cls, v):
        if v is None: return v
        if v < 0:
            raise ValueError('precio_promedio_unidad no puede ser negativo')
        return v

    @field_validator('precio_promedio_venta')
    @classmethod
    def validate_precio_promedio_venta_positive(cls, v):
        if v is None: return v
        if v < 0:
            raise ValueError('precio_promedio_venta no puede ser negativo')
        return v


class Metricas_negocio(Metricas_negocioBase):
    id_metricas_negocio: int

    model_config = {"from_attributes": True, "extra": "forbid"}