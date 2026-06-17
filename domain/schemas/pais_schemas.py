from dataclasses import dataclass
from typing import Optional
from datetime import date, datetime


@dataclass
class Pais:
    codigo_pais: str
    nombre_pais: str