"""
Módulo loan_model
-------------------
Modelo ORM que representa la tabla 'loans': el préstamo de un dispositivo
a un usuario. Es la tabla que relaciona 'users' con 'devices'.
"""

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database.connection import Base


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)

    # Claves foráneas: garantizan la integridad referencial. Un préstamo
    # NO puede existir sin un usuario y un dispositivo válidos.
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    device_id = Column(
        Integer,
        ForeignKey("devices.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    loan_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    return_date = Column(DateTime, nullable=True)
    status = Column(String, nullable=False, default="active", index=True)

    # Relaciones Many-to-One: cada préstamo pertenece a un usuario
    # y a un dispositivo.
    user = relationship("User", back_populates="loans")
    device = relationship("Device", back_populates="loans")