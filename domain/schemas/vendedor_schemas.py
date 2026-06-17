from dataclasses import dataclass
from typing import Optional
from datetime import date, datetime


@dataclass
class Vendedor:
    id_vendedor: int
    user_name: str
    nombre_tienda: str
    codigo_pais: str
    moneda_local: str
    tipo_plan: Optional[int] = None
    email: str
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    tiempo_token: Optional[str] = None
    esta_activo: bool
    fecha_creacion: str