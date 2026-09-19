"""
main.py
--------
Punto de entrada de la aplicación device_systems.
"""

from fastapi import FastAPI

from app.database.connection import engine, Base
from app.models import user_model, device_model, loan_model  # necesario para que Base "conozca" los modelos
from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router



app = FastAPI(
    title="device_systems API",
    description=(
        "API REST para la gestión de usuarios, dispositivos y préstamos del "
        "sistema device_systems. Permite crear, listar, consultar, actualizar "
        "(completa y parcialmente) y eliminar usuarios y dispositivos, "
        "registrar préstamos con validaciones de disponibilidad, consultar "
        "información relacionada mediante joins y aplicar filtros avanzados."
    ),
    version="3.0.0",
    contact={
        "name": "Equipo device_systems",
        "email": "contacto@devicesystems.example",
    },
)

app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)


@app.get("/", tags=["Root"], summary="Estado de la API")
def raiz():
    return {
        "mensaje": "Bienvenido a device_systems API.",
        "docs": "/docs",
        "redoc": "/redoc",
    }