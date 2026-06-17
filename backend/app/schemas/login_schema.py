from pydantic import BaseModel, ConfigDict, EmailStr, SecretStr, Field

#Schema para el pedido de login del vendedor.
class LoginRequest(BaseModel):

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    email: EmailStr = Field(..., description="Correo electrónico del vendedor")
    password: SecretStr = Field(..., min_length=12, max_length=128, description="Contraseña del vendedor")
