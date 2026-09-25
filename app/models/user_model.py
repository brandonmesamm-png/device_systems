"""
Módulo user_model (actualizado para EV11)
------------------------------------------
Agrega el campo hashed_password para soportar autenticación JWT.
"""

from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship

from app.database.connection import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    role = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Campo nuevo para autenticación
    hashed_password = Column(String, nullable=False)

    loans = relationship(
        "Loan",
        back_populates="user",
        cascade="all, delete-orphan",
    )