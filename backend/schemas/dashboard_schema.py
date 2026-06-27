from typing import List, Optional
from pydantic import BaseModel, Field

class ReputacionInfo(BaseModel):

    nivel: str = Field(..., min_length=1, description="Nivel de reputación")
    insignia: Optional[str] = Field(None, description="Insignia")
    ventas_totales: int = Field(..., ge=0, description="Las ventas no pueden ser negativas")
    total_reclamos: int = Field(..., ge=0)
    total_mediaciones: int = Field(..., ge=0)
    total_canceladas: int = Field(..., ge=0)
    total_envios_incorrectos: int = Field(..., ge=0)
    tasa_reclamos: float = Field(..., ge=0.0, le=1.0)
    tasa_cancelaciones: float = Field(..., ge=0.0, le=1.0)

class NegocioInfo(BaseModel):

    ventas_brutas_moneda_local: float = Field(..., ge=0.0)
    ventas_brutas_usd: float = Field(..., ge=0.0)
    unidades_vendidas: int = Field(..., ge=0)
    visitas_totales: int = Field(..., ge=0)
    intencion_compra: int = Field(..., ge=0)
    ventas_concretadas: int = Field(..., ge=0)
    precio_promedio_unidad: float = Field(..., ge=0.0)
    precio_promedio_venta: float = Field(..., ge=0.0)
    cvr_global: float = Field(..., ge=0.0, le=1.0, description="Tasa de conversión global entre 0 y 1")
    ticket_promedio: float = Field(..., ge=0.0)

class CostoInfo(BaseModel):

    ventas_cobradas_total: float = Field(..., ge=0.0)
    neto_recibido: float
    cargos_por_venta: float = Field(..., ge=0.0)
    costos_envio: float = Field(..., ge=0.0)
    inversion_ads: float = Field(..., ge=0.0)
    otros_cargos: float = Field(..., ge=0.0) 
    cargos_envio_full: float = Field(..., ge=0.0)
    descuento_reputacion: float = Field(..., ge=0.0)
    margen_neto: float

class StockInfo(BaseModel):

    espacios_p_asignados: int  = Field(..., ge=0)
    espacios_g_asignados: int = Field(..., ge=0)
    puntaje_calidad: int  = Field(..., ge=0 , le=100, description="Asumiendo una escala de 0 a 100")
    productos_no_aptos_venta: int = Field(..., ge=0)
    productos_sin_rotacion: int = Field(..., ge=0)
    productos_antiguedad: int = Field(..., ge=0)
    productos_exceso_proyeccion: int = Field(..., ge=0)

class PaginaInfo(BaseModel):

    tiene_banner: bool
    tiene_logo: bool
    tiene_carruseles: bool
    categorias_organizadas: bool

class PublicacionResumen(BaseModel):

    id_publicacion: int = Field(..., gt=0, description="El ID debe ser mayor a 0")
    ml_item_id: str = Field(..., min_length=5, description="ID de MercadoLibre (ej. MLA123456)")
    titulo: str = Field(..., min_length=1, max_length=150)
    tipo_publicacion: str = Field(..., min_length=1) # Ej: clasica, premium
    estado_publicacion: str = Field(..., min_length=1) # Ej: activa, pausada
    visitas: int = Field(..., ge=0)
    ventas: int = Field(..., ge=0)
    puntaje_calidad: int = Field(..., ge=0, le=100)
    cvr: float = Field(..., ge=0.0, le=1.0)

class DashboardResponse(BaseModel):

    id_vendedor: int = Field(..., gt=0)
    user_name: str = Field(..., min_length=1)
    nombre_tienda: str = Field(..., min_length=1)
    codigo_pais: str = Field(..., min_length=2, max_length=2, to_upper=True) # Códigos ISO estándar (ej. AR, MX, CO)
    moneda_local: str = Field(..., min_length=3, max_length=3, to_upper=True) # Códigos ISO de moneda (ej. ARS, MXN, COP)
    tipo_plan: int = Field(..., ge=0)

    reputacion: Optional[ReputacionInfo] = None
    negocio: Optional[NegocioInfo] = None
    costos: Optional[CostoInfo] = None
    stock: Optional[StockInfo] = None
    pagina: Optional[PaginaInfo] = None
    publicaciones: List[PublicacionResumen]
