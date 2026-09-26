"""
Módulo auth_routes (con rate limiting)
----------------------------------------
Incluye límites de peticiones con slowapi. El login usa
OAuth2PasswordRequestForm para que el botón "Authorize" de Swagger
funcione correctamente (flujo estándar OAuth2 password).
"""

from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm
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
    description=(
        "Autentica al usuario y retorna un token JWT Bearer. "
        "Usa el formulario estándar OAuth2 (username=correo, password). "
        "Límite: 5 por minuto."
    ),
)
@limiter.limit("5/minute")
def login(
    request: Request,
    # OAuth2PasswordRequestForm es lo que usa el botón "Authorize" de
    # Swagger: envía 'username' (aquí el correo) y 'password' como
    # application/x-www-form-urlencoded, NO como JSON.
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    credenciales = UserLogin(email=form_data.username, password=form_data.password)
    return auth_service.login_usuario(db, credenciales)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Perfil del usuario autenticado",
    description="Retorna los datos del usuario que envía el token. No incluye la contraseña.",
)
def me(current_user: User = Depends(get_current_active_user)):
    return current_user