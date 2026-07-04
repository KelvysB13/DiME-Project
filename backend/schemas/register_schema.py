from pydantic import BaseModel, ConfigDict, EmailStr, SecretStr, Field


class RegisterRequest(BaseModel):

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    email: EmailStr = Field(..., description="Correo electrónico del vendedor")
    password: SecretStr = Field(..., min_length=12, max_length=72, description="Contraseña del vendedor")
    nombre_tienda: str = Field(..., min_length=1, max_length=100, description="Nombre de la tienda")


class PreRegisterResponse(BaseModel):
    message: str = Field(..., description="Mensaje de confirmación")
    pre_token: str = Field(..., description="Token de pre-registro para completar el pago")
    expires_in_minutes: int = Field(..., description="Tiempo de expiración del token en minutos")
