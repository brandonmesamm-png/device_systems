"""
Módulo users_db
-----------------
Simula una base de datos en memoria para el recurso "users".
En un proyecto real, esto sería reemplazado por una conexión
a una base de datos (PostgreSQL, MongoDB, etc).
"""

from typing import List

# Lista de usuarios en memoria, compartida por toda la aplicación.
users_db: List[dict] = [
    {"id": 1, "name": "Ana Torres", "email": "ana@example.com", "role": "admin", "is_active": True},
    {"id": 2, "name": "Luis Pérez", "email": "luis@example.com", "role": "user", "is_active": True},
    {"id": 3, "name": "Marta Gómez", "email": "marta@example.com", "role": "support", "is_active": False},
]


def get_next_id() -> int:
    """
    Calcula el siguiente ID disponible, basado en el mayor
    ID existente en la lista de usuarios.
    """
    return max((u["id"] for u in users_db), default=0) + 1