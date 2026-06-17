from dataclasses import dataclass
from typing import Optional
from datetime import date, datetime


@dataclass
class Publicacion:
    id_publicacion: int
    id_vendedor: int
    ml_item_id: str
    titulo: str
    tipo_publicacion: str
    estado_publicacion: str