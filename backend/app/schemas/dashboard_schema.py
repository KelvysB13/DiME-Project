from typing import List, Optional
from pydantic import BaseModel

class ReputacionInfo(BaseModel):
    
    nivel: str
    insignia: Optional[str] = None
    ventas_totales: int
    total_reclamos: int
    total_mediaciones: int
    total_canceladas: int
    total_envios_incorrectos: int
    tasa_reclamos: float
    tasa_cancelaciones: float

class NegocioInfo(BaseModel):

    ventas_brutas_moneda_local: float
    ventas_brutas_usd: float
    unidades_vendidas: int
    visitas_totales: int
    intencion_compra: int
    ventas_concretadas: int
    precio_promedio_unidad: float
    precio_promedio_venta: float
    cvr_global: float
    ticket_promedio: float

class CostoInfo(BaseModel):

    ventas_cobradas_total: float
    neto_recibido: float
    cargos_por_venta: float
    costos_envio: float
    inversion_ads: float
    otros_cargos: float
    cargos_envio_full: float
    descuento_reputacion: float
    margen_neto: float

class StockInfo(BaseModel):

    espacios_p_asignados: int
    espacios_g_asignados: int
    puntaje_calidad: int
    productos_no_aptos_venta: int
    productos_sin_rotacion: int
    productos_antiguedad: int
    productos_exceso_proyeccion: int

class PaginaInfo(BaseModel):

    tiene_banner: bool
    tiene_logo: bool
    tiene_carruseles: bool
    categorias_organizadas: bool

class PublicacionResumen(BaseModel):

    id_publicacion: int
    ml_item_id: str
    titulo: str
    tipo_publicacion: str
    estado_publicacion: str
    visitas: int
    ventas: int
    puntaje_calidad: int
    cvr: float

class DashboardResponse(BaseModel):

    id_vendedor: int
    user_name: str
    nombre_tienda: str
    codigo_pais: str
    moneda_local: str
    tipo_plan: int
    reputacion: Optional[ReputacionInfo] = None
    negocio: Optional[NegocioInfo] = None
    costos: Optional[CostoInfo] = None
    stock: Optional[StockInfo] = None
    pagina: Optional[PaginaInfo] = None
    publicaciones: List[PublicacionResumen]