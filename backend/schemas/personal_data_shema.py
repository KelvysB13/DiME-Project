from typing import Optional
from pydantic import BaseModel, Field


class PersonalDataResponse(BaseModel):

    nombre_tienda: str = Field(..., min_length=1, max_length=100, description="Nombre de la tienda")
    codigo_pais: str = Field(..., min_length=2, max_length=2, to_upper=True, description="Código ISO del país (ej. MX, AR)")
    tipo_plan: int = Field(..., ge=0, description="ID del plan (1=Free, 2=Básico, 3=Premium)")
    insignia: Optional[str] = Field(None, max_length=20, description="Insignia de Mercado Libre (platinum, gold, leader, etc.)")
