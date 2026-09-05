"""
Módulo user_service
---------------------
Contiene la lógica de negocio del recurso "users":
crear, listar, buscar, actualizar y eliminar usuarios.
Las rutas (user_routes.py) llaman a estas funciones,
sin conocer los detalles de cómo se almacenan los datos.
"""

from typing import Optional, List
from fastapi import HTTPException

from app.data.users_db import users_db, get_next_id
from app.schemas.user_schema import UserCreate, UserUpdate


def list_users(role: Optional[str] = None, is_active: Optional[bool] = None) -> List[dict]:
    """
    Devuelve la lista de usuarios, aplicando filtros opcionales
    por rol y/o estado activo.
    """
    resultado = users_db

    if role is not None:
        resultado = [u for u in resultado if u["role"] == role]

    if is_active is not None:
        resultado = [u for u in resultado if u["is_active"] == is_active]

    return resultado


def get_user_by_id(user_id: int) -> dict:
    """
    Busca un usuario por su ID.
    Lanza un error 404 si no existe.
    """
    for usuario in users_db:
        if usuario["id"] == user_id:
            return usuario

    raise HTTPException(status_code=404, detail="Usuario no encontrado")


def email_exists(email: str, exclude_id: Optional[int] = None) -> bool:
    """
    Verifica si ya existe un usuario con ese correo.
    'exclude_id' permite ignorar al propio usuario al actualizar
    (para no rechazar su propio correo al hacer PUT/PATCH).
    """
    for usuario in users_db:
        if usuario["email"] == email and usuario["id"] != exclude_id:
            return True
    return False


def create_user(nuevo_usuario: UserCreate) -> dict:
    """
    Crea un nuevo usuario, validando que el correo no esté repetido.
    """
    if email_exists(nuevo_usuario.email):
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe un usuario registrado con el correo {nuevo_usuario.email}."
        )

    usuario_guardado = {"id": get_next_id(), **nuevo_usuario.model_dump()}
    usuario_guardado["role"] = usuario_guardado["role"].value
    users_db.append(usuario_guardado)
    return usuario_guardado


def replace_user(user_id: int, datos: UserCreate) -> dict:
    """
    Reemplaza completamente los datos de un usuario existente (PUT).
    Todos los campos son obligatorios.
    """
    usuario = get_user_by_id(user_id)

    if email_exists(datos.email, exclude_id=user_id):
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe un usuario registrado con el correo {datos.email}."
        )

    usuario["name"] = datos.name
    usuario["email"] = datos.email
    usuario["role"] = datos.role.value
    usuario["is_active"] = datos.is_active

    return usuario


def update_user_partial(user_id: int, datos: UserUpdate) -> dict:
    """
    Actualiza parcialmente un usuario (PATCH).
    Solo modifica los campos que el cliente haya enviado.
    """
    usuario = get_user_by_id(user_id)

    # model_dump(exclude_unset=True) devuelve SOLO los campos
    # que el cliente realmente envió en la petición.
    campos_enviados = datos.model_dump(exclude_unset=True)

    if not campos_enviados:
        raise HTTPException(
            status_code=400,
            detail="Debe enviar al menos un campo para actualizar."
        )

    if "email" in campos_enviados and email_exists(campos_enviados["email"], exclude_id=user_id):
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe un usuario registrado con el correo {campos_enviados['email']}."
        )

    for campo, valor in campos_enviados.items():
        # El rol llega como Enum; lo convertimos a texto plano.
        if campo == "role":
            valor = valor.value
        usuario[campo] = valor

    return usuario


def delete_user(user_id: int) -> None:
    """
    Elimina un usuario existente por su ID.
    """
    usuario = get_user_by_id(user_id)
    users_db.remove(usuario)