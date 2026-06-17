from dataclasses import dataclass
from typing import Optional
from datetime import date, datetime


@dataclass
class Rendimiento_publicacion:
    id_rendimiento_publi: int
    id_publicacion: int
    fecha_captura: str
    fecha_inicio_periodo: date
    fecha_fin_periodo: date
    visitas: int
    ventas: int