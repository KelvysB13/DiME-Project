from pydantic import BaseModel, Field
from typing import Optional

class PlanCreate(BaseModel):

    nombre_plan: str = Field(..., min_length=1, max_length=50)
    precio_mensual: float = Field(..., ge=0)
    limite_publicaciones: Optional[int] = Field(None, ge=0)
    limite_metricas_dias: int = Field(30, ge=1)
    features: list = Field(default=[])
    descripcion: Optional[str] = None

class PlanUpdate(BaseModel):

    nombre_plan: Optional[str] = Field(None, min_length=1, max_length=50)
    precio_mensual: Optional[float] = Field(None, ge=0)
    limite_publicaciones: Optional[int] = Field(None, ge=0)
    limite_metricas_dias: Optional[int] = Field(None, ge=1)
    features: Optional[list] = None
    descripcion: Optional[str] = None

class PlanResponse(BaseModel):

    id: int
    nombre_plan: str
    precio_mensual: float
    limite_publicaciones: Optional[int] = None
    limite_metricas_dias: int
    features: list
    descripcion: Optional[str] = None

    model_config = {"from_attributes": True}

class PlanListResponse(BaseModel):
    
    planes: list[PlanResponse]
