"""
Módulo loan_routes
---------------------
Define los endpoints del recurso "loans": creación, consulta, devolución
y consultas con joins/filtros avanzados.

IMPORTANTE: las rutas literales como /loans/details deben declararse
ANTES que /loans/{loan_id}, o FastAPI intentará interpretar "details"
como un loan_id.
"""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Response, Query, Depends, status
from sqlalchemy.orm import Session

from app.schemas.loan_schema import (
    LoanResponse,
    LoanDetailResponse,
    LoanCreate,
    LoanUpdate,
    LoanStatusEnum,
)
from app.schemas.device_schema import DeviceTypeEnum
from app.dependencies.loan_dependencies import get_loan_or_404
from app.dependencies.database_dependency import get_db
from app.models.loan_model import Loan
from app.services import loan_service

router = APIRouter(
    prefix="/loans",
    tags=["Loans"],
    responses={
        400: {"description": "Rango de fechas inválido o PATCH sin campos."},
        404: {"description": "Usuario, dispositivo o préstamo no encontrado."},
        409: {"description": "Dispositivo no disponible o préstamo ya devuelto."},
    },
)


def set_headers(response: Response):
    """Agrega las cabeceras personalizadas a cualquier respuesta."""
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"


@router.get(
    "/details",
    response_model=List[LoanDetailResponse],
    summary="Listar préstamos con información relacionada (join)",
    description=(
        "Lista los préstamos combinando datos de users y devices mediante "
        "join(). Admite filtros por estado, usuario, dispositivo, correo del "
        "usuario, tipo de dispositivo, texto de búsqueda libre y rango de fechas."
    ),
    response_description="Préstamos con los datos del usuario y del dispositivo.",
)
def listar_prestamos_con_detalle(
    response: Response,
    status_filter: Optional[LoanStatusEnum] = Query(default=None, alias="status", description="Filtra por estado."),
    user_id: Optional[int] = Query(default=None, gt=0, description="Filtra por ID de usuario."),
    device_id: Optional[int] = Query(default=None, gt=0, description="Filtra por ID de dispositivo."),
    user_email: Optional[str] = Query(default=None, description="Filtra por correo del usuario (parcial)."),
    device_type: Optional[DeviceTypeEnum] = Query(default=None, description="Filtra por tipo de dispositivo."),
    search: Optional[str] = Query(default=None, description="Búsqueda libre en usuario y dispositivo."),
    from_date: Optional[datetime] = Query(default=None, description="Fecha inicial del préstamo (ISO 8601)."),
    to_date: Optional[datetime] = Query(default=None, description="Fecha final del préstamo (ISO 8601)."),
    db: Session = Depends(get_db),
):
    set_headers(response)
    prestamos = loan_service.list_loans(
        db,
        status_filter=status_filter.value if status_filter else None,
        user_id=user_id,
        device_id=device_id,
        user_email=user_email,
        device_type=device_type.value if device_type else None,
        search=search,
        from_date=from_date,
        to_date=to_date,
    )
    return [LoanDetailResponse.from_loan(p) for p in prestamos]


@router.get(
    "/",
    response_model=List[LoanResponse],
    summary="Listar préstamos",
    description=(
        "Lista los préstamos en formato plano (solo IDs). Admite filtros por "
        "estado, usuario, dispositivo, correo del usuario (parcial) y tipo de "
        "dispositivo. Los filtros se combinan con AND."
    ),
    response_description="Lista de préstamos que cumplen con los filtros aplicados.",
)
def listar_prestamos(
    response: Response,
    status_filter: Optional[LoanStatusEnum] = Query(default=None, alias="status", description="Filtra por estado."),
    user_id: Optional[int] = Query(default=None, gt=0, description="Filtra por ID de usuario."),
    device_id: Optional[int] = Query(default=None, gt=0, description="Filtra por ID de dispositivo."),
    user_email: Optional[str] = Query(default=None, description="Filtra por correo del usuario (parcial)."),
    device_type: Optional[DeviceTypeEnum] = Query(default=None, description="Filtra por tipo de dispositivo."),
    db: Session = Depends(get_db),
):
    set_headers(response)
    return loan_service.list_loans(
        db,
        status_filter=status_filter.value if status_filter else None,
        user_id=user_id,
        device_id=device_id,
        user_email=user_email,
        device_type=device_type.value if device_type else None,
    )


@router.get(
    "/{loan_id}",
    response_model=LoanDetailResponse,
    summary="Consultar préstamo por ID (con detalle)",
    description="Devuelve un préstamo específico junto con los datos del usuario y del dispositivo.",
    response_description="Datos del préstamo, usuario y dispositivo asociados.",
)
def obtener_prestamo(response: Response, prestamo: Loan = Depends(get_loan_or_404)):
    set_headers(response)
    return LoanDetailResponse.from_loan(prestamo)


@router.post(
    "/",
    response_model=LoanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar préstamo",
    description=(
        "Crea un préstamo. Valida que el usuario y el dispositivo existan y "
        "que el dispositivo esté disponible. Al crearlo, el dispositivo pasa "
        "a is_available = False."
    ),
    response_description="Préstamo registrado exitosamente.",
)
def crear_prestamo(nuevo_prestamo: LoanCreate, response: Response, db: Session = Depends(get_db)):
    set_headers(response)
    return loan_service.create_loan(db, nuevo_prestamo)


@router.patch(
    "/{loan_id}/return",
    response_model=LoanResponse,
    summary="Registrar devolución de un préstamo",
    description=(
        "Marca un préstamo como 'returned', asigna la fecha de devolución y "
        "vuelve a poner el dispositivo como disponible. Responde 409 si el "
        "préstamo ya había sido devuelto."
    ),
    response_description="Préstamo actualizado tras la devolución.",
)
def devolver_prestamo(
    response: Response,
    prestamo: Loan = Depends(get_loan_or_404),
    db: Session = Depends(get_db),
):
    set_headers(response)
    return loan_service.return_loan(db, prestamo.id)


@router.patch(
    "/{loan_id}",
    response_model=LoanResponse,
    summary="Actualizar préstamo (parcial)",
    description=(
        "Actualiza campos puntuales de un préstamo, como su estado (por "
        "ejemplo, marcarlo 'overdue'). Responde 409 si el préstamo ya fue devuelto."
    ),
    response_description="Préstamo actualizado con los campos modificados.",
)
def actualizar_prestamo_parcial(
    datos: LoanUpdate,
    response: Response,
    prestamo: Loan = Depends(get_loan_or_404),
    db: Session = Depends(get_db),
):
    set_headers(response)
    return loan_service.update_loan_partial(db, prestamo.id, datos)