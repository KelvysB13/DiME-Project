from pydantic import BaseModel, Field

class LogoutResponse(BaseModel):

    message: str = Field(default="Sesión cerrada exitosamente")
