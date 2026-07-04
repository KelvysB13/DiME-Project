from typing import List, Optional
from pydantic import BaseModel, Field


class ReputacionInfo(BaseModel):

    nivel: str = Field(..., min_length=1, description="Nivel de reputación")
    insignia: Optional[str] = Field(None, description="Insignia")
    ventas_totales: int = Field(..., ge=0, description="Las ventas no pueden ser negativas")
    total_reclamos: int = Field(..., ge=0)
    total_mediaciones: int = Field(..., ge=0)
    total_canceladas: int = Field(..., ge=0)
    tasa_reclamos: float


class NegocioInfo(BaseModel):

    ventas_brutas_moneda_local: float = Field(..., ge=0.0)
    unidades_vendidas: int = Field(..., ge=0)
    visitas_totales: int = Field(..., ge=0)
    intencion_compra: int = Field(..., ge=0)
    ventas_concretadas: int = Field(..., ge=0)


class CostoInfo(BaseModel):

    ventas_cobradas_total: float = Field(..., ge=0.0)
    neto_recibido: float
    cargos_por_venta: float = Field(..., ge=0.0)
    costos_envio: float = Field(..., ge=0.0)
    inversion_ads: float = Field(..., ge=0.0)


class StockInfo(BaseModel):

    espacios_p_asignados: int = Field(..., ge=0)
    puntaje_calidad: int = Field(..., ge=0, le=100, description="Escala de 0 a 100")
    productos_no_aptos_venta: int = Field(..., ge=0)
    productos_sin_rotacion: int = Field(..., ge=0)


class PaginaInfo(BaseModel):

    tiene_banner: bool
    tiene_logo: bool
    tiene_carruseles: bool
    categorias_organizadas: bool


class PublicacionResumen(BaseModel):

    ml_item_id: str = Field(..., min_length=5, description="ID de MercadoLibre (ej. MLA123456)")
    titulo: str = Field(..., min_length=1, max_length=150)
    tipo_publicacion: str = Field(..., min_length=1)
    estado_publicacion: str = Field(..., min_length=1)
    visitas: int = Field(..., ge=0)
    ventas: int = Field(..., ge=0)
    puntaje_calidad: int = Field(..., ge=0, le=100)


class DashboardResponse(BaseModel):

    nombre_tienda: str = Field(..., min_length=1)
    codigo_pais: str = Field(..., min_length=2, max_length=2, to_upper=True)
    tipo_plan: int = Field(..., ge=0)
    reputacion: Optional[ReputacionInfo] = None
    negocio: Optional[NegocioInfo] = None
    costos: Optional[CostoInfo] = None
    stock: Optional[StockInfo] = None
    pagina: Optional[PaginaInfo] = None
    publicaciones: List[PublicacionResumen]
