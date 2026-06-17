from dataclasses import dataclass
from typing import Optional
from datetime import date, datetime


@dataclass
class Moneda:
    codigo_moneda: str
    nombre_moneda: str
    simbolo: str