import strawberry
from typing import Optional

@strawberry.type
class ComunidadAutonomaType:
    id: str
    nombre: str
    wikidata_qid: Optional[str]

@strawberry.type
class ProvinciaType:
    id: str
    nombre: str
    wikidata_qid: Optional[str]
    comunidad_autonoma_id: str

@strawberry.type
class LocalidadType:
    id: str
    nombre: str
    wikidata_qid: Optional[str]
    provincia_id: str

@strawberry.type
class DiocesisType:
    id: str
    nombre: str
    wikidata_qid: Optional[str]

@strawberry.type
class FiguraProteccionType:
    id: str
    nombre: str
    nombre_normalizado: str
    descripcion: Optional[str]
    ambito: Optional[str]
    wikidata_qid: Optional[str]

@strawberry.type
class InmuebleType:
    id: str
    nombre: str
    descripcion: Optional[str]
    direccion: str
    latitud: Optional[float]
    longitud: Optional[float]
    wikidata_qid: Optional[str]
    provincia_id: str
    localidad_id: str
    diocesis_id: str
    tipo_inmueble_id: str
    estado_conservacion_id: str
    estado_tratamiento_id: str
    es_bic: bool
    es_ruina: bool
    esta_inmatriculado: bool
    id_inmatriculacion: Optional[str]

    @strawberry.field
    def provincia(self, info) -> Optional["ProvinciaType"]:
        return info.context.provincia_by_id.load(self.provincia_id)

    @strawberry.field
    def localidad(self, info) -> Optional["LocalidadType"]:
        return info.context.localidad_by_id.load(self.localidad_id)

    @strawberry.field
    def diocesis(self, info) -> Optional["DiocesisType"]:
        return info.context.diocesis_by_id.load(self.diocesis_id)

@strawberry.type
class InmuebleFiguraProteccionType:
    id: str
    inmueble_id: str
    figura_proteccion_id: str
    administracion_id: Optional[str]
    bic_id: Optional[str]
    norma: Optional[str]
    fecha_declaracion: Optional[str]

@strawberry.type
class DocumentoType:
    id: str
    url: str
    nombre_archivo: Optional[str]
    tipo_mime: Optional[str]
    tamano_bytes: Optional[int]
    hash_sha256: Optional[str]
