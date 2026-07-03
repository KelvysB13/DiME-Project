from typing import Optional
from pydantic import BaseModel, Field

class PaymentMethodRequest(BaseModel):

    nombre_titular: str = Field(..., min_length=1, max_length=100, description="Nombre del titular de la tarjeta")
    numero_tarjeta: str = Field(..., min_length=16, max_length=16, description="Número de la tarjeta")
    mes_caducidad: int = Field(..., ge=1, le=12, description="Mes de expiración (1-12)")
    anio_caducidad: int = Field(..., ge=0, le=99, description="Últimos 2 dígitos del año de expiración")
    cvv: str = Field(..., min_length=3, max_length=3, description="CVV de la tarjeta")

class PaymentMethodResponse(BaseModel):

    success: bool = Field(..., description="Indica si la actualización del método de pago fue exitosa")
    message: Optional[str] = Field(None, description="Mensaje adicional sobre el resultado")
