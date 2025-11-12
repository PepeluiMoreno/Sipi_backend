import strawberry
from typing import Optional, List
from strawberry.types import Info
from .types import InmuebleType, LocalidadType, ProvinciaType, DiocesisType
from . import resolvers

@strawberry.type
class Query:
    @strawberry.field
    def ping(self, info: Info) -> str:
        return "ok"

    @strawberry.field
    def inmueble(self, info: Info, id: str) -> Optional[InmuebleType]:
        obj = resolvers.resolve_inmueble(info, id)
        if not obj:
            return None
        return InmuebleType(
            id=obj.id, nombre=obj.nombre, descripcion=obj.descripcion,
            direccion=obj.direccion, latitud=obj.latitud, longitud=obj.longitud
        )

    @strawberry.field
    def inmuebles(self, info: Info, limit: int = 100) -> List[InmuebleType]:
        rows = resolvers.resolve_inmuebles(info, limit=limit)
        return [InmuebleType(
            id=o.id, nombre=o.nombre, descripcion=o.descripcion,
            direccion=o.direccion, latitud=o.latitud, longitud=o.longitud
        ) for o in rows]

    @strawberry.field
    def localidades(self, info: Info) -> List[LocalidadType]:
        rows = resolvers.resolve_localidades(info)
        return [LocalidadType(id=o.id, nombre=o.nombre) for o in rows]

    @strawberry.field
    def provincias(self, info: Info) -> List[ProvinciaType]:
        rows = resolvers.resolve_provincias(info)
        return [ProvinciaType(id=o.id, nombre=o.nombre) for o in rows]

    @strawberry.field
    def diocesis(self, info: Info) -> List[DiocesisType]:
        rows = resolvers.resolve_diocesis(info)
        return [DiocesisType(id=o.id, nombre=o.nombre, wikidata_qid=o.wikidata_qid) for o in rows]

schema = strawberry.Schema(Query)
