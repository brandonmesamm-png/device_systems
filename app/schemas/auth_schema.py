"""
Módulo auth_schema
-------------------
Schemas Pydantic v2 para registro, login y respuesta de tokens.
"""

from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict


class UserRegister(BaseModel):
    """Schema para registrar un nuevo usuario con contraseña."""
    name: str = Field(..., min_length=3, description="Nombre completo, mínimo 3 caracteres.", examples=["Ana Pérez"])
    email: EmailStr = Field(..., description="Correo electrónico válido.", examples=["ana@sena.edu.co"])
    password: str = Field(..., min_length=8, description="Contraseña segura.", examples=["Segura123"])
    role: str = Field(default="user", description="Rol: admin, support o user.", examples=["user"])

    @field_validator("password")
    @classmethod
    def validar_password(cls, v: str) -> str:
        if " " in v:
            raise ValueError("La contraseña no puede contener espacios.")
        if not any(c.isupper() for c in v):
            raise ValueError("La contraseña debe tener al menos una mayúscula.")
        if not any(c.islower() for c in v):
            raise ValueError("La contraseña debe tener al menos una minúscula.")
        if not any(c.isdigit() for c in v):
            raise ValueError("La contraseña debe tener al menos un número.")
        return v

    @field_validator("role")
    @classmethod
    def validar_role(cls, v: str) -> str:
        roles_permitidos = {"admin", "support", "user"}
        if v not in roles_permitidos:
            raise ValueError(f"Rol inválido. Los roles permitidos son: {roles_permitidos}")
        return v

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Ana Pérez",
                "email": "ana@sena.edu.co",
                "password": "Segura123",
                "role": "user"
            }
        }
    )


class UserLogin(BaseModel):
    """Schema para iniciar sesión."""
    email: EmailStr = Field(..., examples=["ana@sena.edu.co"])
    password: str = Field(..., examples=["Segura123"])

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"email": "ana@sena.edu.co", "password": "Segura123"}
        }
    )


class Token(BaseModel):
    """Schema de respuesta del login."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Datos extraídos del token JWT."""
    email: str | None = None
    role: str | None = None
