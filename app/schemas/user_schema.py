"""
Módulo user_schema
-------------------
Define los modelos (schemas) de datos para el recurso "usuarios",
utilizando Pydantic v2 para validar la información que entra y
sale de la API.
"""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RoleEnum(str, Enum):
    """
    Enum que restringe los valores posibles del campo 'role'.
    """
    admin = "admin"
    support = "support"
    user = "user"


class UserBase(BaseModel):
    """
    Modelo base con los campos que comparten la creación
    y la respuesta de un usuario.
    """
    name: str = Field(
        ...,
        min_length=3,
        description="Nombre completo del usuario, mínimo 3 caracteres.",
        examples=["Ana Pérez"],
    )
    email: EmailStr = Field(
        ...,
        description="Correo electrónico del usuario, debe tener formato válido.",
        examples=["ana@sena.edu.co"],
    )
    role: RoleEnum = Field(
        ...,
        description="Rol del usuario: admin, support o user.",
        examples=["user"],
    )
    is_active: bool = Field(
        default=True,
        description="Indica si el usuario está activo en el sistema.",
    )


class UserCreate(UserBase):
    """
    Modelo usado en POST /users y PUT /users/{user_id}.
    Todos los campos son obligatorios.
    """
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Ana Pérez",
                "email": "ana@sena.edu.co",
                "role": "user",
                "is_active": True,
            }
        }
    )


class UserUpdate(BaseModel):
    """
    Modelo usado en PATCH /users/{user_id}.
    Todos los campos son OPCIONALES: el cliente solo envía
    los que quiere modificar.
    """
    name: Optional[str] = Field(default=None, min_length=3, description="Nuevo nombre (opcional).")
    email: Optional[EmailStr] = Field(default=None, description="Nuevo correo (opcional).")
    role: Optional[RoleEnum] = Field(default=None, description="Nuevo rol (opcional).")
    is_active: Optional[bool] = Field(default=None, description="Nuevo estado activo (opcional).")

    model_config = ConfigDict(
        json_schema_extra={"example": {"role": "support", "is_active": False}}
    )


class UserResponse(UserBase):
    """
    Modelo usado como response_model en las respuestas de la API.
    Incluye 'id' porque ya es un usuario existente en el sistema.
    """
    id: int = Field(..., description="Identificador único del usuario.")

    model_config = ConfigDict(from_attributes=True)