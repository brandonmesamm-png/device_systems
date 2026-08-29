"""
main.py
--------
Punto de entrada de la aplicación device_systems.
Crea la instancia de FastAPI y registra las rutas del recurso "users".
"""

from fastapi import FastAPI

from app.routes.user_routes import router as user_router

app = FastAPI(
    title="device_systems",
    description="API REST para la gestión de usuarios del sistema device_systems.",
    version="1.0"
)

# Registra todas las rutas definidas en user_routes.py bajo la app principal.
app.include_router(user_router)


@app.get("/", tags=["Root"])
def raiz():
    """
    Endpoint de bienvenida, útil para verificar que el servidor está activo.
    """
    return {"mensaje": "Bienvenido a device_systems API. Visita /docs para ver la documentación."}