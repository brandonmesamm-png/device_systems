"""
Módulo user_routes
--------------------
Define los endpoints (rutas) relacionados con el recurso "users".
"""

from typing import Optional, List
from fastapi import APIRouter, HTTPException, Path, Query, Response

from app.schemas.user_schema import UserResponse, UserCreate, RoleEnum

# APIRouter agrupa rutas relacionadas para luego
# "engancharlas" al servidor principal (main.py).
router = APIRouter(prefix="/users", tags=["Users"])

# Base de datos simulada en memoria (en vez de una BD real).
fake_users_db: List[dict] = [
    {"id": 1, "name": "Ana Torres", "email": "ana@example.com", "role": "admin", "is_active": True},
    {"id": 2, "name": "Luis Pérez", "email": "luis@example.com", "role": "user", "is_active": True},
    {"id": 3, "name": "Marta Gómez", "email": "marta@example.com", "role": "support", "is_active": False},
]


@router.get("/", response_model=List[UserResponse])
def listar_usuarios(
    response: Response,
    role: Optional[RoleEnum] = Query(
        default=None,
        description="Filtra usuarios por rol (admin, support, user)."
    ),
    is_active: Optional[bool] = Query(
        default=None,
        description="Filtra usuarios por estado activo/inactivo."
    )
):
    """
    GET /users
    GET /users?role=admin
    GET /users?is_active=true
    """
    resultado = fake_users_db

    if role is not None:
        resultado = [u for u in resultado if u["role"] == role.value]

    if is_active is not None:
        resultado = [u for u in resultado if u["is_active"] == is_active]

    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

    return resultado


@router.get("/{user_id}", response_model=UserResponse)
def obtener_usuario(
    response: Response,
    user_id: int = Path(
        ...,
        description="ID del usuario a consultar.",
        gt=0
    )
):
    """
    GET /users/{user_id}
    """
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

    for usuario in fake_users_db:
        if usuario["id"] == user_id:
            return usuario

    raise HTTPException(
        status_code=404,
        detail=f"No se encontró un usuario con id {user_id}."
    )





@router.post("/", response_model=UserResponse, status_code=201)
def crear_usuario(nuevo_usuario: UserCreate, response: Response):
    """
    POST /users
    Registra un nuevo usuario, validando los datos con Pydantic
    y evitando correos duplicados.
    """
    for usuario in fake_users_db:
        if usuario["email"] == nuevo_usuario.email:
            raise HTTPException(
                status_code=400,
                detail=f"Ya existe un usuario registrado con el correo {nuevo_usuario.email}."
            )

    nuevo_id = max((u["id"] for u in fake_users_db), default=0) + 1

    usuario_guardado = {"id": nuevo_id, **nuevo_usuario.model_dump()}
    usuario_guardado["role"] = usuario_guardado["role"].value

    fake_users_db.append(usuario_guardado)

    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

    return usuario_guardado