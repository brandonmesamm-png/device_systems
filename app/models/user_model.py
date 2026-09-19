"""
Módulo user_model
-------------------
Modelo ORM que representa la tabla 'users' en la base de datos.
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

    # Relación One-to-Many: un usuario puede tener muchos préstamos.
    # back_populates conecta este atributo con Loan.user, de modo que
    # SQLAlchemy mantiene ambos lados sincronizados automáticamente.
    loans = relationship(
        "Loan",
        back_populates="user",
        cascade="all, delete-orphan",
    )