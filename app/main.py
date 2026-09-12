"""
main.py
--------
Punto de entrada de la aplicación device_systems.
"""

from fastapi import FastAPI

from app.database.connection import engine, Base
from app.models import user_model  # necesario para que Base "conozca" el modelo
from app.routes.user_routes import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="device_systems API",
    description=(
        "API REST para la gestión de usuarios del sistema device_systems. "
        "Permite crear, listar, consultar, actualizar (completa y parcialmente) "
        "y eliminar usuarios, con validaciones, manejo de errores y "
        "documentación automática."
    ),
    version="2.0.0",
    contact={
        "name": "Equipo device_systems",
        "email": "contacto@devicesystems.example",
    },
)

app.include_router(user_router)


@app.get("/", tags=["Root"], summary="Estado de la API")
def raiz():
    return {
        "mensaje": "Bienvenido a device_systems API.",
        "docs": "/docs",
        "redoc": "/redoc",
    }