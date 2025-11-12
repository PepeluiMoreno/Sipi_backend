import strawberry
from typing import Optional

@strawberry.type
class InmuebleType:
    id: str
    nombre: Optional[str]
    descripcion: Optional[str]
    direccion: Optional[str]
    latitud: Optional[float]
    longitud: Optional[float]

@strawberry.type
class LocalidadType:
    id: str
    nombre: str

@strawberry.type
class ProvinciaType:
    id: str
    nombre: str

@strawberry.type
class DiocesisType:
    id: str
    nombre: str
    wikidata_qid: Optional[str]
