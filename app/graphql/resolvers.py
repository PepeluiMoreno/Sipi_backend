
from typing import Optional
from strawberry.types import Info
from app.db.session import SessionLocal
from app.db.models import Inmueble
from .filters import InmuebleFilter, InmuebleOrderBy

async def resolve_inmuebles(
    info: Info,
    filtro: Optional[InmuebleFilter] = None,
    order_by: Optional[InmuebleOrderBy] = None,
    limit: Optional[int] = 50,
    offset: Optional[int] = 0,
):
    db = info.context.db
    q = db.query(Inmueble)
    if filtro:
        if filtro.provincia_id:
            q = q.filter(Inmueble.provincia_id == filtro.provincia_id)
        if filtro.localidad_id:
            q = q.filter(Inmueble.localidad_id == filtro.localidad_id)
        if filtro.diocesis_id:
            q = q.filter(Inmueble.diocesis_id == filtro.diocesis_id)
        if filtro.es_bic is not None:
            q = q.filter(Inmueble.es_bic == filtro.es_bic)
        if filtro.es_ruina is not None:
            q = q.filter(Inmueble.es_ruina == filtro.es_ruina)
        if filtro.esta_inmatriculado is not None:
            q = q.filter(Inmueble.esta_inmatriculado == filtro.esta_inmatriculado)
        if filtro.texto:
            q = q.filter(Inmueble.nombre.ilike(f"%{filtro.texto}%"))
    if order_by:
        col = Inmueble.nombre if order_by.field.value == "nombre" else Inmueble.fecha_creacion
        q = q.order_by(col.asc() if order_by.direction.value == "asc" else col.desc())
    total = q.count()
    items = q.offset(offset).limit(limit).all()
    return {"items": items, "total": total, "page": offset // max(1, limit), "page_size": limit}
