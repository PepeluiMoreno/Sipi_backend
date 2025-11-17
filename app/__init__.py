# app/db/__init__.py
"""
Importar todos los modelos para que SQLAlchemy los registre
"""
from app.db.base import Base

# Importar todos los modelos
from app.db.models.agentes import *
from app.db.models.inmuebles import *
from app.db.models.catalogos import *
from app.db.models.transmisiones import *
from app.db.models.actuaciones import *
from app.db.models.geografia import *

__all__ = ['Base']