from typing import List, Optional
from pydantic import BaseModel, Field


class KpiQueryItem(BaseModel):
    dimension: str = Field(..., description="Dimensión del KPI")
    nombre_kpi: str = Field(..., description="Nombre del KPI")
    prioridad: str = Field(..., description="Prioridad del KPI")
    valor_actual: Optional[str] = Field(None, description="Valor actual del KPI")
    estado_semaforo: str = Field(..., description="Estado del semáforo: VERDE, AMARILLO, ROJO, GRIS")


class KpiQueryResponse(BaseModel):
    id_vendedor: int = Field(..., description="ID del vendedor")
    items: List[KpiQueryItem] = Field(default_factory=list, description="Lista de KPIs con su estado semáforo")
