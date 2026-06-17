from dataclasses import dataclass
from typing import Optional
from datetime import date, datetime


@dataclass
class Metricas_mi_pagina:
    id_metricas_pagina: int
    id_vendedor: int
    fecha_captura: str
    tiene_banner: bool
    tiene_logo: bool
    tiene_carruseles: bool
    categorias_organizadas: bool