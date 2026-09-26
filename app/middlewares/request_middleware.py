"""
Módulo request_middleware
--------------------------
Middleware personalizado que mide el tiempo de respuesta,
agrega cabeceras globales y registra cada petición.
"""

import time
import uuid
import logging

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("device_systems")


class RequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4())[:8])
        start = time.time()

        response = await call_next(request)

        process_time = round(time.time() - start, 4)

        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-Request-ID"] = request_id

        logger.info(
            f"[{request_id}] {request.method} {request.url.path} "
            f"→ {response.status_code} ({process_time}s)"
        )

        return response
