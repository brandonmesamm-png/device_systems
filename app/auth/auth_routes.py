"""
Módulo auth_routes (con rate limiting)
----------------------------------------
Reemplaza auth_routes.py — incluye límites de peticiones con slowapi.
"""

from fastapi import APIRouter, Depends, Request, status
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import get_current_active_user
from app.schemas.auth_schema import UserRegister, UserLogin, Token
from app.schemas.user_schema import UserResponse
from app.auth import auth_service
from app.models.user_model import User

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar usuario",
    description="Crea un nuevo usuario con contraseña segura. La contraseña se almacena como hash. Límite: 3 por minuto.",
)
@limiter.limit("3/minute")
def register(request: Request, datos: UserRegister, db: Session = Depends(get_db)):
    return auth_service.registrar_usuario(db, datos)


@router.post(
    "/login",
    response_model=Token,
    summary="Iniciar sesión",
    description="Autentica al usuario y retorna un token JWT Bearer. Límite: 5 por minuto.",
)
@limiter.limit("5/minute")
def login(request: Request, datos: UserLogin, db: Session = Depends(get_db)):
    return auth_service.login_usuario(db, datos)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Perfil del usuario autenticado",
    description="Retorna los datos del usuario que envía el token. No incluye la contraseña.",
)
def me(current_user: User = Depends(get_current_active_user)):
    return current_user
