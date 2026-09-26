"""
Módulo device_routes
-----------------------
Define los endpoints del recurso "devices": GET, POST, PUT, PATCH y DELETE,
incluyendo filtros por tipo, disponibilidad, marca y búsqueda libre.

Protección de rutas (Fase 8):
- POST /devices/         -> admin o support
- PUT  /devices/{id}     -> admin o support
- DELETE /devices/{id}   -> solo admin
"""

from typing import List, Optional

from fastapi import APIRouter, Response, Query, Depends, status
from sqlalchemy.orm import Session

from app.schemas.device_schema import (
    DeviceResponse,
    DeviceCreate,
    DeviceUpdate,
    DeviceTypeEnum,
)
from app.schemas.loan_schema import LoanResponse
from app.dependencies.device_dependencies import get_device_or_404
from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import require_admin, require_admin_or_support
from app.models.device_model import Device
from app.models.user_model import User
from app.services import device_service
from app.services import loan_service

router = APIRouter(
    prefix="/devices",
    tags=["Devices"],
    responses={
        400: {"description": "Número de serie duplicado o PATCH sin campos."},
        401: {"description": "No autenticado."},
        403: {"description": "El rol del usuario no tiene permisos para esta acción."},
        404: {"description": "Dispositivo no encontrado."},
        409: {"description": "El dispositivo tiene un préstamo activo."},
    },
)


def set_headers(response: Response):
    """Agrega las cabeceras personalizadas a cualquier respuesta."""
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"


@router.get(
    "/",
    response_model=List[DeviceResponse],
    summary="Listar dispositivos",
    description=(
        "Lista todos los dispositivos registrados. Permite filtrar opcionalmente "
        "por tipo de dispositivo, disponibilidad, marca (búsqueda parcial) y un "
        "texto de búsqueda libre que compara nombre y número de serie."
    ),
    response_description="Lista de dispositivos que cumplen con los filtros aplicados.",
)
def listar_dispositivos(
    response: Response,
    device_type: Optional[DeviceTypeEnum] = Query(default=None, description="Filtra por tipo de dispositivo."),
    is_available: Optional[bool] = Query(default=None, description="Filtra por disponibilidad."),
    brand: Optional[str] = Query(default=None, description="Filtra por marca (búsqueda parcial, ilike)."),
    search: Optional[str] = Query(default=None, description="Busca el texto en el nombre o el número de serie."),
    db: Session = Depends(get_db),
):
    set_headers(response)
    tipo = device_type.value if device_type else None
    return device_service.list_devices(
        db, device_type=tipo, is_available=is_available, brand=brand, search=search
    )


@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Consultar dispositivo por ID",
    description="Devuelve la información de un dispositivo específico según su ID.",
    response_description="Datos del dispositivo encontrado.",
)
def obtener_dispositivo(response: Response, dispositivo: Device = Depends(get_device_or_404)):
    set_headers(response)
    return dispositivo


@router.post(
    "/",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear dispositivo",
    description=(
        "Registra un nuevo dispositivo. Valida que el número de serie no esté "
        "duplicado. Requiere rol admin o support."
    ),
    response_description="Dispositivo creado exitosamente.",
)
def crear_dispositivo(
    nuevo_dispositivo: DeviceCreate,
    response: Response,
    db: Session = Depends(get_db),
    _usuario_actual: User = Depends(require_admin_or_support),
):
    set_headers(response)
    return device_service.create_device(db, nuevo_dispositivo)


@router.put(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar dispositivo (completo)",
    description=(
        "Reemplaza completamente los datos de un dispositivo existente. "
        "Requiere rol admin o support."
    ),
    response_description="Dispositivo actualizado con los nuevos datos.",
)
def actualizar_dispositivo(
    datos: DeviceCreate,
    response: Response,
    dispositivo: Device = Depends(get_device_or_404),
    db: Session = Depends(get_db),
    _usuario_actual: User = Depends(require_admin_or_support),
):
    set_headers(response)
    return device_service.replace_device(db, dispositivo.id, datos)


@router.patch(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar dispositivo (parcial)",
    description="Actualiza solo los campos enviados por el cliente. Requiere rol admin o support.",
    response_description="Dispositivo actualizado con los campos modificados.",
)
def actualizar_dispositivo_parcial(
    datos: DeviceUpdate,
    response: Response,
    dispositivo: Device = Depends(get_device_or_404),
    db: Session = Depends(get_db),
    _usuario_actual: User = Depends(require_admin_or_support),
):
    set_headers(response)
    return device_service.update_device_partial(db, dispositivo.id, datos)


@router.delete(
    "/{device_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar dispositivo",
    description=(
        "Elimina un dispositivo existente por su ID. "
        "Responde 409 si el dispositivo tiene un préstamo activo. "
        "Requiere rol admin."
    ),
    response_description="Dispositivo eliminado exitosamente (sin contenido).",
)
def eliminar_dispositivo(
    response: Response,
    dispositivo: Device = Depends(get_device_or_404),
    db: Session = Depends(get_db),
    _usuario_actual: User = Depends(require_admin),
):
    set_headers(response)
    device_service.delete_device(db, dispositivo.id)
    return None


@router.get(
    "/{device_id}/loans",
    response_model=List[LoanResponse],
    summary="Historial de préstamos de un dispositivo",
    description="Devuelve todos los préstamos asociados a un dispositivo específico.",
    response_description="Lista de préstamos del dispositivo.",
)
def obtener_prestamos_de_dispositivo(
    response: Response,
    dispositivo: Device = Depends(get_device_or_404),
    db: Session = Depends(get_db),
):
    set_headers(response)
    return loan_service.list_loans_by_device(db, dispositivo.id)