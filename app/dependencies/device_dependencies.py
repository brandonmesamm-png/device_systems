"""
Módulo device_dependencies
----------------------------
Funciones reutilizables con Depends() para el recurso "devices".
"""

from fastapi import Path, Depends
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.models.device_model import Device
from app.services.device_service import get_device_by_id


def get_device_or_404(
    device_id: int = Path(..., description="ID del dispositivo", gt=0),
    db: Session = Depends(get_db),
) -> Device:
    """
    Dependencia que obtiene un dispositivo por su ID.
    Si no existe, detiene la petición con un error 404 antes de
    llegar al código del endpoint.
    """
    return get_device_by_id(db, device_id)