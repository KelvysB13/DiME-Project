from pydantic import BaseModel, ConfigDict, SecretStr, Field, model_validator


class UpdatePasswordRequest(BaseModel):

    current_password: SecretStr = Field(..., min_length=12, max_length=72, description="Contraseña actual del vendedor")
    new_password: SecretStr = Field(..., min_length=12, max_length=72, description="Nueva contraseña del vendedor")
    confirm_new_password: SecretStr = Field(..., min_length=12, max_length=72, description="Confirmar nueva contraseña")

    @model_validator(mode="after")
    def passwords_match(self):

        if self.new_password.get_secret_value() != self.confirm_new_password.get_secret_value():
            raise ValueError("Las contraseñas nuevas no coinciden")
        
        return self



