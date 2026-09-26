"""
Módulo auth_service
---------------------
Lógica de negocio para registro y login de usuarios.
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user_model import User
from app.schemas.auth_schema import UserRegister, UserLogin, Token
from app.auth.security import get_password_hash, verify_password, create_access_token


def registrar_usuario(db: Session, datos: UserRegister) -> User:
    """Registra un usuario nuevo con contraseña hasheada."""
    existente = db.query(User).filter(User.email == datos.email).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un usuario con el correo {datos.email}."
        )

    usuario = User(
        name=datos.name,
        email=datos.email,
        role=datos.role,
        is_active=True,
        hashed_password=get_password_hash(datos.password),
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def login_usuario(db: Session, datos: UserLogin) -> Token:
    """Autentica un usuario y retorna un token JWT."""
    usuario = db.query(User).filter(User.email == datos.email).first()

    if not usuario or not verify_password(datos.password, usuario.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not usuario.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo."
        )

    token = create_access_token(data={"sub": usuario.email, "role": usuario.role})
    return Token(access_token=token, token_type="bearer")
