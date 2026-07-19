from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class VendedorResponse(BaseModel):
    id_vendedor: int
    user_name: str
    nombre_tienda: str
    codigo_pais: str
    moneda_local: str
    tipo_plan: Optional[int] = None
    email: str
    esta_activo: bool
    fecha_creacion: Optional[datetime] = None

    class Config:
        from_attributes = True


class VendedorListResponse(BaseModel):
    vendedores: list[VendedorResponse]
    total: int
    page: int
    per_page: int
    total_pages: int
