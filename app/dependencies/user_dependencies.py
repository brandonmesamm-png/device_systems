"""
Módulo user_dependencies
--------------------------
Funciones reutilizables para ser usadas con Depends() en las rutas.
Centralizan validaciones y lógica común, evitando repetir código
en cada endpoint.
"""

from typing import Optional
from fastapi import HTTPException, Path, Header, Depends
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.models.user_model import User
from app.services.user_service import get_user_by_id


def get_user_or_404(
    user_id: int = Path(..., description="ID del usuario", gt=0),
    db: Session = Depends(get_db),
) -> User:
    """
    Dependencia que obtiene un usuario por su ID.
    Si no existe, FastAPI detiene la petición aquí mismo
    con un error 404, antes de llegar al código del endpoint.
    """
    return get_user_by_id(db, user_id)


def get_api_settings() -> dict:
    """
    Dependencia que simula configuración general de la API.
    """
    return {
        "app_name": "device_systems",
        "api_version": "2.0.0",
    }


def verify_basic_auth(x_api_key: Optional[str] = Header(default=None)) -> None:
    """
    Dependencia que simula una autenticación básica mediante
    una cabecera personalizada 'X-API-Key'.
    """
    if x_api_key is None:
        raise HTTPException(
            status_code=401,
            detail="Falta la cabecera 'X-API-Key' para autenticar la solicitud."
        )
    if x_api_key != "clave-secreta-123":
        raise HTTPException(
            status_code=401,
            detail="Credenciales inválidas."
        )