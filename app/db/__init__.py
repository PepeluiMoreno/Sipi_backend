"""
app/db/__init__.py
Define las exportaciones principales del paquete de base de datos:
- Base: clase declarativa para los modelos SQLAlchemy.
- engine: instancia de SQLAlchemy Engine.
- SessionLocal: fábrica de sesiones.
- get_db(): generador de sesión para FastAPI / resolvers.
"""

from .session import engine, SessionLocal, get_db
from .models import Base

__all__ = ["engine", "SessionLocal", "get_db", "Base"]