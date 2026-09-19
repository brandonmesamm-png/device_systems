"""
Módulo loan_service
---------------------
Lógica de negocio del recurso "loans". Aquí viven las reglas del
préstamo (disponibilidad, devolución) y las consultas con joins
que combinan las tablas loans, users y devices.
"""

from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session, joinedload

from app.models.device_model import Device
from app.models.loan_model import Loan
from app.models.user_model import User
from app.schemas.loan_schema import LoanCreate, LoanUpdate


def _consulta_base():
    """
    Consulta base con JOIN explícito hacia users y devices.

    joinedload() evita el problema N+1: trae el usuario y el dispositivo
    en la misma consulta, de modo que loan.user y loan.device ya vienen
    cargados cuando se arma la respuesta detallada.
    """
    return (
        select(Loan)
        .join(User, Loan.user_id == User.id)
        .join(Device, Loan.device_id == Device.id)
        .options(joinedload(Loan.user), joinedload(Loan.device))
    )


def list_loans(
    db: Session,
    status_filter: Optional[str] = None,
    user_id: Optional[int] = None,
    device_id: Optional[int] = None,
    user_email: Optional[str] = None,
    device_type: Optional[str] = None,
    search: Optional[str] = None,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
) -> List[Loan]:
    """
    Lista préstamos combinando información de las tres tablas.

    Todos los filtros son opcionales y se acumulan con AND. Los que
    apuntan a columnas de users o devices son posibles gracias al join.
    """
    consulta = _consulta_base()

    if status_filter is not None:
        consulta = consulta.where(Loan.status == status_filter)

    if user_id is not None:
        consulta = consulta.where(Loan.user_id == user_id)

    if device_id is not None:
        consulta = consulta.where(Loan.device_id == device_id)

    if user_email is not None:
        consulta = consulta.where(User.email.ilike(f"%{user_email}%"))

    if device_type is not None:
        consulta = consulta.where(Device.device_type == device_type)

    if search is not None:
        patron = f"%{search}%"
        consulta = consulta.where(
            or_(
                User.name.ilike(patron),
                User.email.ilike(patron),
                Device.name.ilike(patron),
                Device.serial_number.ilike(patron),
            )
        )

    if from_date is not None and to_date is not None:
        if from_date > to_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El parámetro from_date no puede ser posterior a to_date.",
            )
        consulta = consulta.where(and_(Loan.loan_date >= from_date, Loan.loan_date <= to_date))
    elif from_date is not None:
        consulta = consulta.where(Loan.loan_date >= from_date)
    elif to_date is not None:
        consulta = consulta.where(Loan.loan_date <= to_date)

    return list(db.execute(consulta.order_by(Loan.id)).unique().scalars().all())


def get_loan_by_id(db: Session, loan_id: int) -> Loan:
    """Busca un préstamo por su ID, con usuario y dispositivo cargados."""
    consulta = _consulta_base().where(Loan.id == loan_id)
    prestamo = db.execute(consulta).unique().scalars().first()

    if prestamo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe un préstamo con el ID {loan_id}.",
        )
    return prestamo


def list_loans_by_user(db: Session, user_id: int) -> List[Loan]:
    """
    Historial de préstamos de un usuario.
    Valida primero que el usuario exista (404 si no).
    """
    if db.get(User, user_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe un usuario con el ID {user_id}.",
        )
    return list_loans(db, user_id=user_id)


def list_loans_by_device(db: Session, device_id: int) -> List[Loan]:
    """
    Historial de préstamos de un dispositivo.
    Valida primero que el dispositivo exista (404 si no).
    """
    if db.get(Device, device_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe un dispositivo con el ID {device_id}.",
        )
    return list_loans(db, device_id=device_id)


def create_loan(db: Session, datos: LoanCreate) -> Loan:
    """
    Registra un préstamo aplicando las reglas de negocio:

    1. El usuario debe existir           -> 404
    2. El dispositivo debe existir       -> 404
    3. El dispositivo debe estar libre   -> 409
    4. Se crea el préstamo como 'active'
    5. El dispositivo pasa a is_available = False
    """
    usuario = db.get(User, datos.user_id)
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe un usuario con el ID {datos.user_id}.",
        )

    dispositivo = db.get(Device, datos.device_id)
    if dispositivo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe un dispositivo con el ID {datos.device_id}.",
        )

    if not dispositivo.is_available:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"El dispositivo '{dispositivo.name}' (ID {dispositivo.id}) "
                f"no está disponible: ya se encuentra prestado."
            ),
        )

    prestamo = Loan(
        user_id=datos.user_id,
        device_id=datos.device_id,
        loan_date=datos.loan_date or datetime.utcnow(),
        status="active",
    )

    dispositivo.is_available = False

    db.add(prestamo)
    db.commit()
    db.refresh(prestamo)
    return prestamo


def return_loan(db: Session, loan_id: int) -> Loan:
    """
    Registra la devolución de un préstamo:

    1. El préstamo debe existir            -> 404
    2. No puede estar ya devuelto          -> 409
    3. status pasa a 'returned'
    4. Se asigna la fecha de devolución
    5. El dispositivo vuelve a estar disponible
    """
    prestamo = get_loan_by_id(db, loan_id)

    if prestamo.status == "returned":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"El préstamo {loan_id} ya fue devuelto el "
                f"{prestamo.return_date:%Y-%m-%d %H:%M} y no puede devolverse de nuevo."
            ),
        )

    prestamo.status = "returned"
    prestamo.return_date = datetime.utcnow()
    prestamo.device.is_available = True

    db.commit()
    db.refresh(prestamo)
    return prestamo


def update_loan_partial(db: Session, loan_id: int, datos: LoanUpdate) -> Loan:
    """
    Actualiza parcialmente un préstamo (por ejemplo, marcarlo como 'overdue').

    Reglas de negocio:
    - Se debe enviar al menos un campo                      -> 400
    - Un préstamo ya devuelto no se puede modificar          -> 409
    - Mantiene coherente la disponibilidad del dispositivo según el estado.
    """
    prestamo = get_loan_by_id(db, loan_id)
    campos = datos.model_dump(exclude_unset=True)

    if not campos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe enviar al menos un campo para actualizar.",
        )

    if prestamo.status == "returned":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"El préstamo {loan_id} ya fue devuelto y no puede modificarse. "
                f"Registre un préstamo nuevo si el equipo se vuelve a prestar."
            ),
        )

    if "status" in campos and campos["status"] is not None:
        nuevo_estado = campos["status"].value
        prestamo.status = nuevo_estado

        if nuevo_estado == "returned":
            prestamo.return_date = campos.get("return_date") or datetime.utcnow()
            prestamo.device.is_available = True
        else:
            prestamo.device.is_available = False

    elif "return_date" in campos:
        prestamo.return_date = campos["return_date"]

    db.commit()
    db.refresh(prestamo)
    return prestamo