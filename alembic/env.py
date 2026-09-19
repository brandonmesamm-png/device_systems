"""
env.py de Alembic
--------------------
Conecta Alembic con la aplicación device_systems: usa la misma URL de
conexión y la misma metadata de SQLAlchemy que usa la app en tiempo de
ejecución, para que 'alembic revision --autogenerate' detecte los
modelos User, Device y Loan automáticamente.
"""

import sys
from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Permite importar el paquete "app" aunque Alembic se ejecute desde
# la raíz del proyecto.
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.database.connection import Base, DATABASE_URL  # noqa: E402

# Importar los modelos es OBLIGATORIO para que Base.metadata los conozca
# y --autogenerate pueda detectar las tablas devices y loans.
from app.models import user_model, device_model, loan_model  # noqa: E402,F401

# Objeto de configuración de Alembic, que da acceso a los valores del
# archivo .ini que se está usando.
config = context.config

# Inyecta la URL de conexión real de la app (en vez de la que viene
# de ejemplo en alembic.ini).
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Interpreta el archivo de configuración para el logging de Python.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata objetivo: usada por --autogenerate para comparar los modelos
# contra el estado real de la base de datos.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Ejecuta las migraciones en modo 'offline' (genera SQL sin conectar)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Ejecuta las migraciones en modo 'online' (con conexión real a la BD)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()