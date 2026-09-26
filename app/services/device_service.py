"""
Módulo device_service
-----------------------
Lógica de negocio del recurso "devices": crear, listar con filtros
avanzados, consultar, actualizar y eliminar dispositivos.
"""

from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.device_model import Device
from app.models.loan_model import Loan
from app.schemas.device_schema import DeviceCreate, DeviceUpdate


def list_devices(
    db: Session,
    device_type: Optional[str] = None,
    is_available: Optional[bool] = None,
    brand: Optional[str] = None,
    search: Optional[str] = None,
) -> List[Device]:
    """
    Lista dispositivos aplicando filtros opcionales y acumulables.

    - device_type: coincidencia exacta.
    - is_available: filtra por disponibilidad.
    - brand: búsqueda parcial e insensible a mayúsculas (ilike).
    - search: busca el texto en el nombre O en el número de serie (or_).
    """
    consulta = select(Device)

    if device_type is not None:
        consulta = consulta.where(Device.device_type == device_type)

    if is_available is not None:
        consulta = consulta.where(Device.is_available == is_available)

    if brand is not None:
        consulta = consulta.where(Device.brand.ilike(f"%{brand}%"))

    if search is not None:
        patron = f"%{search}%"
        consulta = consulta.where(
            or_(
                Device.name.ilike(patron),
                Device.serial_number.ilike(patron),
            )
        )

    return list(db.execute(consulta.order_by(Device.id)).scalars().all())


def get_device_by_id(db: Session, device_id: int) -> Device:
    """Busca un dispositivo por su ID. Lanza 404 si no existe."""
    dispositivo = db.get(Device, device_id)
    if dispositivo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe un dispositivo con el ID {device_id}.",
        )
    return dispositivo


def serial_exists(db: Session, serial_number: str, exclude_id: Optional[int] = None) -> bool:
    """Indica si el número de serie ya está registrado en otro dispositivo."""
    consulta = select(Device).where(Device.serial_number == serial_number)
    if exclude_id is not None:
        consulta = consulta.where(Device.id != exclude_id)
    return db.execute(consulta).scalars().first() is not None


def create_device(db: Session, datos: DeviceCreate) -> Device:
    """Crea un dispositivo validando que el número de serie no esté duplicado."""
    if serial_exists(db, datos.serial_number):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un dispositivo con el número de serie {datos.serial_number}.",
        )

    dispositivo = Device(
        name=datos.name,
        serial_number=datos.serial_number,
        device_type=datos.device_type.value,
        brand=datos.brand,
        is_available=datos.is_available,
    )

    db.add(dispositivo)
    db.commit()
    db.refresh(dispositivo)
    return dispositivo


def replace_device(db: Session, device_id: int, datos: DeviceCreate) -> Device:
    """Reemplaza por completo los datos de un dispositivo (PUT)."""
    dispositivo = get_device_by_id(db, device_id)

    if serial_exists(db, datos.serial_number, exclude_id=device_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un dispositivo con el número de serie {datos.serial_number}.",
        )

    dispositivo.name = datos.name
    dispositivo.serial_number = datos.serial_number
    dispositivo.device_type = datos.device_type.value
    dispositivo.brand = datos.brand
    dispositivo.is_available = datos.is_available

    db.commit()
    db.refresh(dispositivo)
    return dispositivo


def update_device_partial(db: Session, device_id: int, datos: DeviceUpdate) -> Device:
    """Actualiza solo los campos enviados por el cliente (PATCH)."""
    dispositivo = get_device_by_id(db, device_id)
    campos = datos.model_dump(exclude_unset=True)

    if not campos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe enviar al menos un campo para actualizar.",
        )

    if "serial_number" in campos and serial_exists(db, campos["serial_number"], exclude_id=device_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un dispositivo con el número de serie {campos['serial_number']}.",
        )

    for campo, valor in campos.items():
        if campo == "device_type" and valor is not None:
            valor = valor.value
        setattr(dispositivo, campo, valor)

    db.commit()
    db.refresh(dispositivo)
    return dispositivo


def delete_device(db: Session, device_id: int) -> None:
    """
    Elimina un dispositivo. Regla de negocio: no se puede eliminar
    un equipo que tenga un préstamo activo (409 Conflict).
    """
    dispositivo = get_device_by_id(db, device_id)

    prestamo_activo = db.execute(
        select(Loan).where(Loan.device_id == device_id, Loan.status == "active")
    ).scalars().first()

    if prestamo_activo is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"No se puede eliminar el dispositivo {device_id} porque tiene "
                f"el préstamo activo {prestamo_activo.id}. Regístrelo como devuelto primero."
            ),
        )

    db.delete(dispositivo)
    db.commit()