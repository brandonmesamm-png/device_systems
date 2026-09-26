"""
Módulo device_schema
----------------------
Schemas Pydantic v2 para el recurso "devices". Validan la información
que entra y sale de la API y alimentan la documentación Swagger.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class DeviceTypeEnum(str, Enum):
    """Tipos de dispositivo permitidos en el sistema."""
    laptop = "laptop"
    tablet = "tablet"
    proyector = "proyector"
    camara = "camara"
    router = "router"
    monitor = "monitor"


class DeviceBase(BaseModel):
    """Campos comunes para crear y responder un dispositivo."""

    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Nombre descriptivo del equipo.",
        examples=["Laptop Lenovo ThinkPad"],
    )
    serial_number: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Número de serie. Debe ser único en todo el sistema.",
        examples=["LEN-2024-001"],
    )
    device_type: DeviceTypeEnum = Field(
        ...,
        description="Tipo de dispositivo: laptop, tablet, proyector, camara, router o monitor.",
    )
    brand: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Marca del equipo (opcional).",
        examples=["Lenovo"],
    )
    is_available: bool = Field(
        default=True,
        description="Indica si el dispositivo está disponible para préstamo.",
    )


class DeviceCreate(DeviceBase):
    """Modelo usado en POST /devices y PUT /devices/{device_id}."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Laptop Lenovo ThinkPad",
                "serial_number": "LEN-2024-001",
                "device_type": "laptop",
                "brand": "Lenovo",
                "is_available": True,
            }
        }
    )


class DeviceUpdate(BaseModel):
    """
    Modelo usado en PATCH /devices/{device_id}.
    Todos los campos son opcionales: el cliente envía solo lo que cambia.
    """

    name: Optional[str] = Field(default=None, min_length=3, max_length=100)
    serial_number: Optional[str] = Field(default=None, min_length=3, max_length=50)
    device_type: Optional[DeviceTypeEnum] = Field(default=None)
    brand: Optional[str] = Field(default=None, max_length=50)
    is_available: Optional[bool] = Field(default=None)

    model_config = ConfigDict(
        json_schema_extra={"example": {"brand": "Lenovo", "is_available": False}}
    )


class DeviceResponse(DeviceBase):
    """Respuesta completa de un dispositivo existente."""

    id: int = Field(..., description="Identificador único del dispositivo.")
    created_at: datetime = Field(..., description="Fecha de registro del dispositivo.")

    model_config = ConfigDict(from_attributes=True)


class DeviceSummary(BaseModel):
    """
    Versión reducida del dispositivo, usada dentro de las respuestas
    de préstamos para no repetir toda la información.
    """

    id: int
    name: str
    serial_number: str
    device_type: str

    model_config = ConfigDict(from_attributes=True)