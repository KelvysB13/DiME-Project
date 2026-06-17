from dataclasses import dataclass
from typing import Optional
from datetime import date, datetime


@dataclass
class Metricas_calidad_publicacion:
    id_metricas_calidad_publi: int
    id_publicacion: int
    fecha_captura: str
    cantidad_fotos: int
    tiene_video: bool
    caracteristicas_completas: bool
    puntaje_calidad: int