"""
Módulo user_dependencies
--------------------------
Funciones reutilizables para ser usadas con Depends() en las rutas.
Centralizan validaciones y lógica común, evitando repetir código
en cada endpoint.
"""

from fastapi import HTTPException, Path, Header
from typing import Optional

from app.services.user_service import get_user_by_id


def get_user_or_404(user_id: int = Path(..., description="ID del usuario", gt=0)) -> dict:
    """
    Dependencia que obtiene un usuario por su ID.
    Si no existe, FastAPI detiene la petición aquí mismo
    con un error 404, antes de llegar al código del endpoint.
    """
    return get_user_by_id(user_id)


def get_api_settings() -> dict:
    """
    Dependencia que simula configuración general de la API.
    Útil para inyectar valores comunes (nombre, versión) sin
    repetirlos manualmente en cada respuesta.
    """
    return {
        "app_name": "device_systems",
        "api_version": "2.0.0",
    }


def verify_basic_auth(x_api_key: Optional[str] = Header(default=None)) -> None:
    """
    Dependencia que simula una autenticación básica mediante
    una cabecera personalizada 'X-API-Key'.

    Esto es solo una simulación educativa: en un proyecto real
    se validaría contra una base de datos o un servicio de auth.
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