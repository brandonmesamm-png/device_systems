"""
Módulo user_routes
--------------------
Define los endpoints del recurso "users": GET, POST, PUT, PATCH y DELETE.
Las rutas delegan la lógica de negocio al módulo user_service,
y reutilizan validaciones comunes mediante Depends().
"""

from typing import Optional, List
from fastapi import APIRouter, Response, Query, Depends, status

from app.schemas.user_schema import UserResponse, UserCreate, UserUpdate, RoleEnum
from app.dependencies.user_dependencies import get_user_or_404
from app.services import user_service

router = APIRouter(prefix="/users", tags=["Users"])


def set_headers(response: Response):
    """Agrega las cabeceras personalizadas a cualquier respuesta."""
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"


@router.get(
    "/",
    response_model=List[UserResponse],
    summary="Listar usuarios",
    description="Lista todos los usuarios registrados. Permite filtrar opcionalmente por rol y/o estado activo.",
    response_description="Lista de usuarios que cumplen con los filtros aplicados.",
)
def listar_usuarios(
    response: Response,
    role: Optional[RoleEnum] = Query(default=None, description="Filtra usuarios por rol."),
    is_active: Optional[bool] = Query(default=None, description="Filtra usuarios por estado activo/inactivo."),
):
    set_headers(response)
    role_value = role.value if role else None
    return user_service.list_users(role=role_value, is_active=is_active)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Consultar usuario por ID",
    description="Devuelve la información de un usuario específico según su ID.",
    response_description="Datos del usuario encontrado.",
)
def obtener_usuario(response: Response, usuario: dict = Depends(get_user_or_404)):
    set_headers(response)
    return usuario


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario",
    description="Registra un nuevo usuario. Valida los datos con Pydantic y evita correos duplicados.",
    response_description="Usuario creado exitosamente.",
)
def crear_usuario(nuevo_usuario: UserCreate, response: Response):
    set_headers(response)
    return user_service.create_user(nuevo_usuario)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario (completo)",
    description="Reemplaza completamente los datos de un usuario existente. Todos los campos son obligatorios.",
    response_description="Usuario actualizado con los nuevos datos.",
)
def actualizar_usuario(
    datos: UserCreate,
    response: Response,
    usuario: dict = Depends(get_user_or_404),
):
    set_headers(response)
    return user_service.replace_user(usuario["id"], datos)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario (parcial)",
    description="Actualiza solo los campos enviados por el cliente. Si no se envía ningún campo, responde 400.",
    response_description="Usuario actualizado con los campos modificados.",
)
def actualizar_usuario_parcial(
    datos: UserUpdate,
    response: Response,
    usuario: dict = Depends(get_user_or_404),
):
    set_headers(response)
    return user_service.update_user_partial(usuario["id"], datos)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario",
    description="Elimina un usuario existente por su ID. No retorna contenido si la eliminación fue exitosa.",
    response_description="Usuario eliminado exitosamente (sin contenido).",
)
def eliminar_usuario(response: Response, usuario: dict = Depends(get_user_or_404)):
    set_headers(response)
    user_service.delete_user(usuario["id"])
    return None