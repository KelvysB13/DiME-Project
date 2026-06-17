from dataclasses import dataclass
from typing import Optional
from datetime import date, datetime


@dataclass
class Metricas_costo:
    id_metricas_costo: int
    id_vendedor: int
    fecha_captura: str
    ventas_cobradas_total: float
    neto_recibido: float
    cargos_por_venta: float
    costos_envio: float
    inversion_ads: float
    otros_cargos: float
    cargos_envio_full: float
    descuento_reputacion: float