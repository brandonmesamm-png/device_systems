"""
Configuración de la conexión a la base de datos usando SQLAlchemy.
"""

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./device_systems.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


@event.listens_for(Engine, "connect")
def activar_llaves_foraneas(dbapi_connection, connection_record):
    """
    SQLite no aplica las llaves foráneas por defecto. Este listener ejecuta
    PRAGMA foreign_keys=ON en cada conexión para garantizar la integridad
    referencial: un préstamo no puede apuntar a un usuario o dispositivo
    que no exista.
    """
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()