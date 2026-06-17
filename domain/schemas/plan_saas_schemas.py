from dataclasses import dataclass
from typing import Optional
from datetime import date, datetime


@dataclass
class Plan_saas:
    id_plan: int
    nombre_plan: str
    descripcion: Optional[str] = None