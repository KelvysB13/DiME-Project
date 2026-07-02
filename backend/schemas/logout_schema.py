from pydantic import BaseModel, Field

class LogoutRequest(BaseModel):
    
    access_token: str = Field(..., description="Token de acceso a invalidar")

class LogoutResponse(BaseModel):

    message: str = Field(default="Sesión cerrada exitosamente")
