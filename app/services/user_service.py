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

from sqlalchemy.orm import Session

from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate



def list_users(db: Session, role: Optional[str] = None, is_active: Optional[bool] = None) -> List[User]:
    """
    Devuelve la lista de usuarios, aplicando filtros opcionales
    por rol y/o estado activo.
    """
    query = db.query(User)

    if role is not None:
        query = query.filter(User.role == role)

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    return query.all()

def get_user_by_id(db: Session, user_id: int) -> User:
    """
    Busca un usuario por su ID.
    Lanza un error 404 si no existe.
    """
    usuario = db.query(User).filter(User.id == user_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario





def email_exists(db:Session, email: str, exclude_id: Optional[int] = None) -> bool:
  
    for usuario in db.query(User).filter(User.email == email).all():

        if usuario.id != exclude_id:
            
            return True
    return False

def create_user(db: Session, nuevo_usuario: UserCreate) -> User:
    """
    Crea un nuevo usuario, validando que el correo no esté repetido.
    """
    if email_exists(db, nuevo_usuario.email):
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe un usuario registrado con el correo {nuevo_usuario.email}."
        )

    usuario_guardado = User(
        name=nuevo_usuario.name,
        email=nuevo_usuario.email,
        role=nuevo_usuario.role.value,
        is_active=nuevo_usuario.is_active,
    )

    db.add(usuario_guardado)
    db.commit()
    db.refresh(usuario_guardado)

    return usuario_guardado

def replace_user(db: Session, user_id: int, datos: UserCreate) -> User:
    """
    Reemplaza completamente los datos de un usuario existente (PUT).
    Todos los campos son obligatorios.
    """
    usuario = get_user_by_id(db, user_id)

    if email_exists(db, datos.email, exclude_id=user_id):
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe un usuario registrado con el correo {datos.email}."
        )

    usuario.name = datos.name
    usuario.email = datos.email
    usuario.role = datos.role.value
    usuario.is_active = datos.is_active

    db.commit()
    db.refresh(usuario)

    return usuario

def update_user_partial(db: Session, user_id: int, datos: UserUpdate) -> User:
    """
    Actualiza parcialmente un usuario (PATCH).
    Solo modifica los campos que el cliente haya enviado.
    """
    usuario = get_user_by_id(db, user_id)

    campos_enviados = datos.model_dump(exclude_unset=True)

    if not campos_enviados:
        raise HTTPException(
            status_code=400,
            detail="Debe enviar al menos un campo para actualizar."
        )

    if "email" in campos_enviados and email_exists(db, campos_enviados["email"], exclude_id=user_id):
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe un usuario registrado con el correo {campos_enviados['email']}."
        )

    for campo, valor in campos_enviados.items():
        if campo == "role":
            valor = valor.value
        setattr(usuario, campo, valor)

    db.commit()
    db.refresh(usuario)

    return usuario

def delete_user(db: Session, user_id: int) -> None:
    """
    Elimina un usuario existente por su ID.
    """
    usuario = get_user_by_id(db, user_id)
    db.delete(usuario)
    db.commit()