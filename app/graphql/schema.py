import strawberry
from typing import List, Optional
from .types import (
    InmuebleType, ComunidadAutonomaType, ProvinciaType, LocalidadType, DiocesisType,
    FiguraProteccionType, InmuebleFiguraProteccionType, DocumentoType
)
from .filters import InmuebleFilter, InmuebleOrderBy
from .common import PageInfo
from .inputs import InmuebleInput, InmuebleFiguraProteccionInput, InmuebleUpsertNaturalKey
from . import resolvers
from .mutations import (
    create_inmueble, delete_inmueble, upsert_inmueble_figura,
    upsert_inmueble_by_natural_key, batch_upsert_inmuebles,
    MutationResult, BatchResult
)

@strawberry.type
class InmuebleConnection:
    items: List[InmuebleType]
    page_info: PageInfo

@strawberry.type
class Query:
    ping: str = "pong"
    inmuebles: InmuebleConnection = strawberry.field(resolver=lambda *args, **kwargs: None)
    inmueble: Optional[InmuebleType] = strawberry.field(resolver=resolvers.get_inmueble)
    comunidades: List[ComunidadAutonomaType] = strawberry.field(resolver=resolvers.list_comunidades)
    provincias: List[ProvinciaType] = strawberry.field(resolver=resolvers.list_provincias)
    localidades: List[LocalidadType] = strawberry.field(resolver=resolvers.list_localidades)
    diocesis: List[DiocesisType] = strawberry.field(resolver=resolvers.list_diocesis)
    figuras_proteccion: List[FiguraProteccionType] = strawberry.field(resolver=resolvers.list_figuras)
    inmueble_figuras: List[InmuebleFiguraProteccionType] = strawberry.field(resolver=resolvers.list_inmueble_figuras)
    inmueble_documentos: List[DocumentoType] = strawberry.field(resolver=resolvers.list_inmueble_documentos)

    def resolve_inmuebles(self, info, f: Optional[InmuebleFilter] = None,
                          order_by: Optional[InmuebleOrderBy] = None,
                          limit: int = 50, offset: int = 0) -> "InmuebleConnection":
        items, pi = resolvers.list_inmuebles(f=f, order_by=order_by, limit=limit, offset=offset)
        return InmuebleConnection(items=items, page_info=pi)

@strawberry.type
class Mutation:
    create_inmueble: MutationResult = strawberry.field(resolver=create_inmueble)
    upsert_inmueble_by_natural_key: MutationResult = strawberry.field(resolver=upsert_inmueble_by_natural_key)
    batch_upsert_inmuebles: BatchResult = strawberry.field(resolver=batch_upsert_inmuebles)
    delete_inmueble: MutationResult = strawberry.field(resolver=delete_inmueble)
    upsert_inmueble_figura: MutationResult = strawberry.field(resolver=upsert_inmueble_figura)

schema = strawberry.Schema(query=Query, mutation=Mutation)
