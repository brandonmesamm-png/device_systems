"""
Módulo user_schema
-------------------
Define los modelos (schemas) de datos para el recurso "usuarios",
utilizando Pydantic v2 para validar la información que entra y
sale de la API.
"""

from enum import Enum
from pydantic import BaseModel, EmailStr, Field


class RoleEnum(str, Enum):
    """
    Enum que restringe los valores posibles del campo 'role'.
    Al heredar también de 'str', FastAPI puede mostrarlo
    correctamente en la documentación de Swagger UI.
    """
    admin = "admin"
    support = "support"
    user = "user"


class UserBase(BaseModel):
    """
    Modelo base con los campos que comparten tanto la creación
    como la respuesta de un usuario. Evita repetir código.
    """
    name: str = Field(
        ...,
        min_length=3,
        description="Nombre completo del usuario, mínimo 3 caracteres."
    )
    email: EmailStr = Field(
        ...,
        description="Correo electrónico del usuario, debe tener formato válido."
    )
    role: RoleEnum = Field(
        ...,
        description="Rol del usuario: admin, support o user."
    )
    is_active: bool = Field(
        default=True,
        description="Indica si el usuario está activo en el sistema."
    )


class UserCreate(UserBase):
    """
    Modelo usado en el body del endpoint POST /users.
    Hereda todos los campos de UserBase.
    No incluye 'id' porque lo asigna el servidor automáticamente.
    """
    pass


class UserResponse(UserBase):
    """
    Modelo usado como response_model en las respuestas de la API.
    Incluye 'id' porque ya es un usuario existente en el sistema.
    """
    id: int = Field(..., description="Identificador único del usuario.")

    class Config:
        from_attributes = True