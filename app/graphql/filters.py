
from __future__ import annotations
from enum import Enum
from typing import Optional
import strawberry

@strawberry.enum
class InmuebleOrderField(Enum):
    NOMBRE = "nombre"
    FECHA_CREACION = "fecha_creacion"

@strawberry.enum
class OrderDirection(Enum):
    ASC = "asc"
    DESC = "desc"

@strawberry.input
class InmuebleOrderBy:
    field: InmuebleOrderField = InmuebleOrderField.NOMBRE
    direction: OrderDirection = OrderDirection.ASC

@strawberry.input
class InmuebleFilter:
    provincia_id: Optional[str] = None
    localidad_id: Optional[str] = None
    diocesis_id: Optional[str] = None
    es_bic: Optional[bool] = None
    es_ruina: Optional[bool] = None
    esta_inmatriculado: Optional[bool] = None
    texto: Optional[str] = None  # búsqueda simple
