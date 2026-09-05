"""
main.py
--------
Punto de entrada de la aplicación device_systems.
Crea la instancia de FastAPI, configura sus metadatos
y registra las rutas del recurso "users".
"""

from fastapi import FastAPI

from app.routes.user_routes import router as user_router

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
    """
    Endpoint de bienvenida, útil para verificar que el servidor está activo.
    """
    return {
        "mensaje": "Bienvenido a device_systems API.",
        "docs": "/docs",
        "redoc": "/redoc",
    }