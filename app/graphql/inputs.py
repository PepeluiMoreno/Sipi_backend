import strawberry
from typing import Optional, List

@strawberry.input
class InmuebleInput:
    nombre: str
    descripcion: Optional[str] = None
    direccion: str
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    wikidata_qid: Optional[str] = None
    provincia_id: str
    localidad_id: str
    diocesis_id: str
    tipo_inmueble_id: str
    estado_conservacion_id: str
    estado_tratamiento_id: str
    es_bic: bool = False
    es_ruina: bool = False
    esta_inmatriculado: bool = False
    id_inmatriculacion: Optional[str] = None

@strawberry.input
class InmuebleFiguraProteccionInput:
    inmueble_id: str
    figura_proteccion_id: str
    administracion_id: Optional[str] = None
    bic_id: Optional[str] = None
    norma: Optional[str] = None
    fecha_declaracion: Optional[str] = None

@strawberry.input
class InmuebleUpsertNaturalKey:
    nombre: str
    provincia_id: str
    localidad_id: str
