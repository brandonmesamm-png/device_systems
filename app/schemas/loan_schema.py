"""
Módulo loan_schema
--------------------
Schemas Pydantic v2 para el recurso "loans". Incluye LoanDetailResponse,
que muestra la información relacionada del usuario y del dispositivo
obtenida mediante consultas con joins.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.device_schema import DeviceSummary


class LoanStatusEnum(str, Enum):
    """Estados posibles de un préstamo."""
    active = "active"
    returned = "returned"
    overdue = "overdue"


class UserSummary(BaseModel):
    """Datos básicos del usuario mostrados dentro de un préstamo."""

    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class LoanCreate(BaseModel):
    """Modelo usado en POST /loans."""

    user_id: int = Field(..., gt=0, description="ID del usuario que recibe el equipo.")
    device_id: int = Field(..., gt=0, description="ID del dispositivo a prestar.")
    loan_date: Optional[datetime] = Field(
        default=None,
        description="Fecha del préstamo. Si se omite, se usa la fecha actual.",
    )

    model_config = ConfigDict(
        json_schema_extra={"example": {"user_id": 1, "device_id": 3}}
    )


class LoanUpdate(BaseModel):
    """
    Modelo usado en PATCH /loans/{loan_id}.
    Permite ajustar el estado o la fecha de devolución manualmente.
    """

    status: Optional[LoanStatusEnum] = Field(default=None)
    return_date: Optional[datetime] = Field(default=None)

    model_config = ConfigDict(json_schema_extra={"example": {"status": "overdue"}})


class LoanResponse(BaseModel):
    """Respuesta plana de un préstamo (solo IDs, sin datos relacionados)."""

    id: int
    user_id: int
    device_id: int
    loan_date: datetime
    return_date: Optional[datetime] = None
    status: LoanStatusEnum

    model_config = ConfigDict(from_attributes=True)


class LoanDetailResponse(BaseModel):
    """
    Respuesta enriquecida de un préstamo: incluye los datos básicos
    del usuario y del dispositivo asociados, resultado de un join.
    """

    loan_id: int = Field(..., description="Identificador del préstamo.")
    status: LoanStatusEnum
    loan_date: datetime
    return_date: Optional[datetime] = None
    user: UserSummary
    device: DeviceSummary

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "loan_id": 1,
                "status": "active",
                "loan_date": "2026-09-16T10:30:00",
                "return_date": None,
                "user": {"id": 1, "name": "Ana Pérez", "email": "ana@sena.edu.co"},
                "device": {
                    "id": 3,
                    "name": "Laptop Lenovo ThinkPad",
                    "serial_number": "LEN-2024-001",
                    "device_type": "laptop",
                },
            }
        }
    )

    @classmethod
    def from_loan(cls, loan) -> "LoanDetailResponse":
        """
        Construye la respuesta detallada a partir de un objeto Loan del ORM,
        aprovechando las relaciones loan.user y loan.device.
        """
        return cls(
            loan_id=loan.id,
            status=loan.status,
            loan_date=loan.loan_date,
            return_date=loan.return_date,
            user=UserSummary.model_validate(loan.user),
            device=DeviceSummary.model_validate(loan.device),
        )