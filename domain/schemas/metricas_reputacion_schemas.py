from dataclasses import dataclass
from typing import Optional
from datetime import date, datetime


@dataclass
class Metricas_reputacion:
    id_metricas_reputacion: int
    id_vendedor: int
    fecha_captura: str
    ventas_totales_periodo: int
    total_reclamos: int
    total_mediaciones: int
    total_canceladas: int
    total_envios_incorrectos: int
    nivel_reputacion: str
    insignia: Optional[str] = None