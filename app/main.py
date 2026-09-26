"""
main.py (actualizado para EV11)
---------------------------------
Agrega autenticación, CORS, middleware y rate limiting.
"""

import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.database.connection import engine, Base
from app.models import user_model, device_model, loan_model
from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router
from app.auth.auth_routes import router as auth_router
from app.middlewares.request_middleware import RequestMiddleware

logging.basicConfig(level=logging.INFO)

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="device_systems API",
    description=(
        "API REST segura para la gestión de usuarios, dispositivos y préstamos. "
        "Incluye autenticación JWT, autorización por roles, rate limiting y middleware personalizado."
    ),
    version="3.0.0",
    contact={
        "name": "Equipo device_systems",
        "email": "contacto@devicesystems.example",
    },
)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware personalizado
app.add_middleware(RequestMiddleware)

# Routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)


@app.get("/", tags=["Root"], summary="Estado de la API")
def raiz():
    return {
        "mensaje": "Bienvenido a device_systems API v3.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
    }
