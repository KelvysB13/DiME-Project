from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field


class KpiMaestroCreate(BaseModel):
    dimension: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Dimensión del KPI: Reputación, Finanzas, Publicaciones, Publicidad, Logística",
    )
    nombre_kpi: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Nombre único del KPI",
    )
    operador_logico: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="Operador lógico para evaluar el KPI: '<', '>', 'RANGO', '='",
    )
    umbral_verde_inf: Optional[Decimal] = Field(
        None,
        ge=0,
        description="Límite inferior del umbral verde (numérico)",
    )
    umbral_verde_sup: Optional[Decimal] = Field(
        None,
        ge=0,
        description="Límite superior del umbral verde (numérico)",
    )
    umbral_amarillo_inf: Optional[Decimal] = Field(
        None,
        ge=0,
        description="Límite inferior del umbral amarillo (numérico)",
    )
    umbral_amarillo_sup: Optional[Decimal] = Field(
        None,
        ge=0,
        description="Límite superior del umbral amarillo (numérico)",
    )
    texto_ideal: Optional[str] = Field(
        None,
        max_length=50,
        description="Valor de texto ideal (ej: 'verde', 'platinum')",
    )
    texto_alerta: Optional[str] = Field(
        None,
        max_length=100,
        description="Valores de texto de alerta separados por coma (ej: 'amarillo,naranja')",
    )
    texto_peligro: Optional[str] = Field(
        None,
        max_length=50,
        description="Valor de texto de peligro (ej: 'rojo', 'sin_insignia')",
    )
    prioridad: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="Prioridad del KPI",
    )


class KpiMaestroUpdate(BaseModel):
    dimension: Optional[str] = Field(
        None,
        min_length=1,
        max_length=50,
        description="Dimensión del KPI",
    )
    nombre_kpi: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Nombre único del KPI",
    )
    operador_logico: Optional[str] = Field(
        None,
        min_length=1,
        max_length=20,
        description="Operador lógico para evaluar el KPI",
    )
    umbral_verde_inf: Optional[Decimal] = Field(
        None,
        ge=0,
        description="Límite inferior del umbral verde",
    )
    umbral_verde_sup: Optional[Decimal] = Field(
        None,
        ge=0,
        description="Límite superior del umbral verde",
    )
    umbral_amarillo_inf: Optional[Decimal] = Field(
        None,
        ge=0,
        description="Límite inferior del umbral amarillo",
    )
    umbral_amarillo_sup: Optional[Decimal] = Field(
        None,
        ge=0,
        description="Límite superior del umbral amarillo",
    )
    texto_ideal: Optional[str] = Field(
        None,
        max_length=50,
        description="Valor de texto ideal",
    )
    texto_alerta: Optional[str] = Field(
        None,
        max_length=100,
        description="Valores de texto de alerta separados por coma",
    )
    texto_peligro: Optional[str] = Field(
        None,
        max_length=50,
        description="Valor de texto de peligro",
    )
    prioridad: Optional[str] = Field(
        None,
        min_length=1,
        max_length=20,
        description="Prioridad del KPI",
    )


class KpiMaestroResponse(BaseModel):
    id_kpi: int = Field(..., ge=1, description="ID único del KPI")
    dimension: str = Field(..., description="Dimensión del KPI")
    nombre_kpi: str = Field(..., description="Nombre único del KPI")
    operador_logico: str = Field(..., description="Operador lógico del KPI")
    umbral_verde_inf: Optional[Decimal] = Field(None, description="Límite inferior del umbral verde")
    umbral_verde_sup: Optional[Decimal] = Field(None, description="Límite superior del umbral verde")
    umbral_amarillo_inf: Optional[Decimal] = Field(None, description="Límite inferior del umbral amarillo")
    umbral_amarillo_sup: Optional[Decimal] = Field(None, description="Límite superior del umbral amarillo")
    texto_ideal: Optional[str] = Field(None, description="Valor de texto ideal")
    texto_alerta: Optional[str] = Field(None, description="Valores de texto de alerta")
    texto_peligro: Optional[str] = Field(None, description="Valor de texto de peligro")
    prioridad: str = Field(..., description="Prioridad del KPI")
