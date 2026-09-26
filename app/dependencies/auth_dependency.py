"""
Módulo auth_dependency
------------------------
Dependencias para proteger rutas con JWT y verificar roles.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.auth.security import decode_access_token
from app.dependencies.database_dependency import get_db
from app.models.user_model import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Extrae y valida el usuario desde el token JWT."""
    credenciales_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise credenciales_error
    except JWTError:
        raise credenciales_error

    usuario = db.query(User).filter(User.email == email).first()
    if usuario is None:
        raise credenciales_error
    return usuario


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Verifica que el usuario autenticado esté activo."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo."
        )
    return current_user


def require_admin(current_user: User = Depends(get_current_active_user)) -> User:
    """Solo permite acceso a usuarios con rol admin."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere rol de administrador."
        )
    return current_user


def require_admin_or_support(current_user: User = Depends(get_current_active_user)) -> User:
    """Permite acceso a admin y support."""
    if current_user.role not in {"admin", "support"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere rol admin o support."
        )
    return current_user
