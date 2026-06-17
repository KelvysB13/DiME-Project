from dataclasses import dataclass
from typing import Optional
from datetime import date, datetime


@dataclass
class Reportes_diagnostico:
    id_reporte: int
    id_vendedor: int
    fecha_generacion: date
    fecha_inicio_periodo: date
    fecha_fin_periodo: date
    resumen_ejecutivo: Optional[str] = None
    plan_accion: dict