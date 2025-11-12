# app/graphql/filters.py
import strawberry
from typing import Optional
from enum import Enum 

@strawberry.input
class DateRange:
    gte: Optional[str] = None
    lte: Optional[str] = None

@strawberry.input
class BBox:
    min_lon: float
    min_lat: float
    max_lon: float
    max_lat: float

@strawberry.input
class GeoRadius:
    lon: float
    lat: float
    radius_m: float

@strawberry.input
class InmuebleFilter:
    id: Optional[str] = None
    wikidata_qid: Optional[str] = None
    provincia_id: Optional[str] = None
    localidad_id: Optional[str] = None
    diocesis_id: Optional[str] = None
    tipo_inmueble_id: Optional[str] = None
    es_bic: Optional[bool] = None
    es_ruina: Optional[bool] = None
    esta_inmatriculado: Optional[bool] = None
    q: Optional[str] = None
    fecha_declaracion: Optional[DateRange] = None
    bbox: Optional[BBox] = None
    geo: Optional[GeoRadius] = None

# ✅ Enum correcto
@strawberry.enum
class InmuebleOrderBy(Enum):
    nombre_asc = "nombre_asc"
    nombre_desc = "nombre_desc"
    created_asc = "created_asc"
    created_desc = "created_desc"

