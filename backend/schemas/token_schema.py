from typing import Literal
from pydantic import BaseModel, Field

# Schema para solicitud de token.
class TokenRequest(BaseModel):

    refresh_token: str = Field(..., description="Token de actualización para renovar el token de acceso")

# Schema para respuesta de token renovado.
class TokenResponse(BaseModel):

    id_vendedor: int = Field(..., description="ID del vendedor autenticado")
    access_token: str = Field(..., description="Token de acceso renovado")
    token_type: Literal["bearer"] = "bearer"
    expires_in: int = Field(..., description="Tiempo en segundos hasta que el token de acceso expire")
    role: Literal["vendedor", "admin"] = Field(default="vendedor", description="Rol del usuario autenticado")
