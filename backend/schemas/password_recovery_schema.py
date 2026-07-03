from pydantic import BaseModel, EmailStr, SecretStr, Field

class PasswordRecoveryRequest(BaseModel):
    email: EmailStr = Field(..., description="Correo electrónico del vendedor")

class PasswordRecoveryResponse(BaseModel):
    message: str = Field(default="Si el correo existe, recibirás un enlace de recuperación")
    reset_token: str | None = Field(default=None, description="Token de recuperación (solo en desarrollo)")

class ResetPasswordRequest(BaseModel):
    token: str = Field(..., description="Token de recuperación recibido por correo")
    new_password: SecretStr = Field(..., min_length=12, max_length=72, description="Nueva contraseña")

class ResetPasswordResponse(BaseModel):
    message: str = Field(default="Contraseña actualizada exitosamente")
