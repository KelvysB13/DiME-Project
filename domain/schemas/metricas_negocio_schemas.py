from dataclasses import dataclass
from typing import Optional
from datetime import date, datetime


@dataclass
class Metricas_negocio:
    id_metricas_negocio: int
    id_vendedor: int
    fecha_captura: str
    fecha_inicio_periodo: date
    fecha_fin_periodo: date
    ventas_brutas_moneda_local: float
    ventas_brutas_usd: float
    unidades_vendidas: int
    visitas_totales: int
    intencion_compra: int
    ventas_concretadas: int
    precio_promedio_unidad: float
    precio_promedio_venta: float