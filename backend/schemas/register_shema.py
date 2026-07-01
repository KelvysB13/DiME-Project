from pydantic import BaseModel, EmailStr, Field, SecretStr


class RegisterRequest(BaseModel):
    email: EmailStr = Field(..., max_length=70, description="Correo electrónico")
    password: SecretStr = Field(..., min_length=6, max_length=25, description="Contraseña del vendedor")
    nombre_tienda: str = Field(..., min_length=1, max_length=100, description="Nombre de la tienda")








