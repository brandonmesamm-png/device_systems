"""
Módulo device_model
---------------------
Modelo ORM que representa la tabla 'devices': los equipos tecnológicos
disponibles para préstamo (laptops, tablets, proyectores, etc.).
"""

from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    serial_number = Column(String, unique=True, nullable=False, index=True)
    device_type = Column(String, nullable=False, index=True)
    brand = Column(String, nullable=True)
    is_available = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relación One-to-Many: un dispositivo puede aparecer en muchos préstamos
    # históricos. cascade borra los préstamos si se elimina el dispositivo.
    loans = relationship(
        "Loan",
        back_populates="device",
        cascade="all, delete-orphan",
    )