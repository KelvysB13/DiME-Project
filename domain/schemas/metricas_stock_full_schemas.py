from dataclasses import dataclass
from typing import Optional
from datetime import date, datetime


@dataclass
class Metricas_stock_full:
    id_metricas_stock: int
    id_vendedor: int
    fecha_captura: str
    espacios_p_asignados: int
    espacios_g_asignados: int
    puntaje_calidad: int
    productos_no_aptos_venta: int
    productos_sin_rotacion: int
    productos_antiguedad: int
    productos_exceso_proyeccion: int