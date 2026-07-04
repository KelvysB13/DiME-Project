from pydantic import BaseModel, Field
from typing import Optional

class PlanResponse(BaseModel):
    id: int
    nombre_plan: str
    precio_mensual: float
    limite_publicaciones: Optional[int] = None
    limite_metricas_dias: int
    features: list
    descripcion: Optional[str] = None

class PlanListResponse(BaseModel):
    planes: list[PlanResponse]
