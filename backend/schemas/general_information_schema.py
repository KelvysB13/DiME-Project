from pydantic import BaseModel, EmailStr, Field


class UserInfo(BaseModel):
    user_name: str = Field(
        ..., min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_]+$",
        description="Nombre de usuario único (solo letras, números y guion bajo)"
    )
    nombre_tienda: str = Field(
        ..., min_length=1, max_length=100,
        description="Nombre comercial de la tienda"
    )
    email: EmailStr = Field(
        ..., max_length=70,
        description="Correo electrónico del vendedor"
    )
    nombre_pais: str = Field(
        ..., min_length=1, max_length=60,
        description="Nombre del país (ej. México, Argentina, Colombia)"
    )
    es_admin: bool = Field(
        default=False,
        description="Indica si el vendedor tiene rol de administrador de la plataforma"
    )
