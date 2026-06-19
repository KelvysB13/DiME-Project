from pydantic import BaseModel, EmailStr, SecretStr
from typing import Optional, List


# ==============================================================================
# Auth schemas
# ==============================================================================

class LoginRequest(BaseModel):
    email: EmailStr
    password: SecretStr


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 3600


# ==============================================================================
# Dashboard schemas
# ==============================================================================

class ReputacionInfo(BaseModel):
    nivel: str
    insignia: Optional[str] = None
    ventas_totales: int = 0
    total_reclamos: int = 0
    total_mediaciones: int = 0
    total_canceladas: int = 0
    total_envios_incorrectos: int = 0
    tasa_reclamos: float = 0.0
    tasa_cancelaciones: float = 0.0


class NegocioInfo(BaseModel):
    ventas_brutas_moneda_local: float = 0.0
    ventas_brutas_usd: float = 0.0
    unidades_vendidas: int = 0
    visitas_totales: int = 0
    intencion_compra: int = 0
    ventas_concretadas: int = 0
    precio_promedio_unidad: float = 0.0
    precio_promedio_venta: float = 0.0
    cvr_global: float = 0.0
    ticket_promedio: float = 0.0


class CostoInfo(BaseModel):
    ventas_cobradas_total: float = 0.0
    neto_recibido: float = 0.0
    cargos_por_venta: float = 0.0
    costos_envio: float = 0.0
    inversion_ads: float = 0.0
    otros_cargos: float = 0.0
    cargos_envio_full: float = 0.0
    descuento_reputacion: float = 0.0
    margen_neto: float = 0.0


class StockInfo(BaseModel):
    espacios_p_asignados: int = 0
    espacios_g_asignados: int = 0
    puntaje_calidad: int = 0
    productos_no_aptos_venta: int = 0
    productos_sin_rotacion: int = 0
    productos_antiguedad: int = 0
    productos_exceso_proyeccion: int = 0


class PaginaInfo(BaseModel):
    tiene_banner: bool = False
    tiene_logo: bool = False
    tiene_carruseles: bool = False
    categorias_organizadas: bool = False


class PublicacionResumen(BaseModel):
    id_publicacion: int
    ml_item_id: str
    titulo: str
    tipo_publicacion: str
    estado_publicacion: str
    visitas: int = 0
    ventas: int = 0
    puntaje_calidad: int = 0
    cvr: float = 0.0


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
    publicaciones: List[PublicacionResumen] = []
