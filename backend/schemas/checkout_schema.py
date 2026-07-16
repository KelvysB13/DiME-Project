from typing import Optional
from pydantic import BaseModel, Field

class CheckoutRequest(BaseModel):

    pre_token: str = Field(..., description="Token de pre-registro obtenido en /auth/register")
    id_plan: int = Field(..., gt=0, description="ID del plan a contratar (2=Básico, 3=Premium)")
    nombre_titular: str = Field(..., min_length=1, max_length=100, description="Nombre del titular de la tarjeta")
    numero_tarjeta: str = Field(..., min_length=16, max_length=16, description="Número de la tarjeta")
    mes_caducidad: int = Field(..., ge=1, le=12, description="Mes de expiración (1-12)")
    anio_caducidad: int = Field(..., ge=0, le=99, description="Últimos 2 dígitos del año de expiración")
    cvv: str = Field(..., min_length=3, max_length=3, description="CVV de la tarjeta")

class CheckoutResponse(BaseModel):

    success: bool = Field(..., description="Indica si el pago fue procesado exitosamente")
    message: Optional[str] = Field(None, description="Mensaje adicional sobre el resultado")
    access_token: Optional[str] = Field(None, description="Token de acceso JWT para auto-login")
    token_type: Optional[str] = Field(None, description="Tipo de token (bearer)")
    expires_in: Optional[int] = Field(None, description="Tiempo de expiración en segundos")
    role: Optional[str] = Field(None, description="Rol del usuario (vendedor)")
    id_vendedor: Optional[int] = Field(None, description="ID del vendedor creado")
