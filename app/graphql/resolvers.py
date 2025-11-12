from typing import Optional
from sqlalchemy import select, func
from app.db.session  import get_db
from app.db.models import (
    Inmueble, ComunidadAutonoma, Provincia, Localidad, Diocesis, FiguraProteccion,
    InmuebleFiguraProteccion, Documento, InmuebleDocumento
)
from .types import (
    InmuebleType, ComunidadAutonomaType, ProvinciaType, LocalidadType, DiocesisType,
    FiguraProteccionType, InmuebleFiguraProteccionType, DocumentoType
)
from .filters import InmuebleFilter, InmuebleOrderBy
from .common import page_info


def to_dict(row):
    return {c.key: getattr(row, c.key) for c in row.__table__.columns}

def _apply_inmueble_filters(stmt, f: Optional[InmuebleFilter]):
    if not f:
        return stmt
    if f.id:
        stmt = stmt.where(Inmueble.id == f.id)
    if f.wikidata_qid:
        stmt = stmt.where(Inmueble.wikidata_qid == f.wikidata_qid)
    if f.provincia_id:
        stmt = stmt.where(Inmueble.provincia_id == f.provincia_id)
    if f.localidad_id:
        stmt = stmt.where(Inmueble.localidad_id == f.localidad_id)
    if f.diocesis_id:
        stmt = stmt.where(Inmueble.diocesis_id == f.diocesis_id)
    if f.tipo_inmueble_id:
        stmt = stmt.where(Inmueble.tipo_inmueble_id == f.tipo_inmueble_id)
    if f.es_bic is not None:
        stmt = stmt.where(Inmueble.es_bic == f.es_bic)
    if f.es_ruina is not None:
        stmt = stmt.where(Inmueble.es_ruina == f.es_ruina)
    if f.esta_inmatriculado is not None:
        stmt = stmt.where(Inmueble.esta_inmatriculado == f.esta_inmatriculado)
    if f.q:
        ilike = f"%{f.q}%"
        stmt = stmt.where((Inmueble.nombre.ilike(ilike)) | (Inmueble.direccion.ilike(ilike)))
    if f.bbox:
        stmt = stmt.where(
            (Inmueble.longitud >= f.bbox.min_lon) &
            (Inmueble.longitud <= f.bbox.max_lon) &
            (Inmueble.latitud >= f.bbox.min_lat) &
            (Inmueble.latitud <= f.bbox.max_lat)
        )
    return stmt

def _apply_inmueble_order(stmt, order: Optional[InmuebleOrderBy]):
    if not order:
        return stmt.order_by(Inmueble.nombre.asc())
    mapping = {
        InmuebleOrderBy.nombre_asc: Inmueble.nombre.asc(),
        InmuebleOrderBy.nombre_desc: Inmueble.nombre.desc(),
        InmuebleOrderBy.created_asc: Inmueble.fecha_creacion.asc(),
        InmuebleOrderBy.created_desc: Inmueble.fecha_creacion.desc(),
    }
    return stmt.order_by(mapping.get(order, Inmueble.nombre.asc()))

def list_inmuebles(f: Optional[InmuebleFilter] = None, order_by: Optional[InmuebleOrderBy] = None,
                   limit: int = 50, offset: int = 0):
    with get_db() as db:
        base = select(Inmueble)
        base = _apply_inmueble_filters(base, f)
        total = db.execute(select(func.count()).select_from(base.subquery())).scalar_one()
        stmt = _apply_inmueble_order(base, order_by).offset(offset).limit(limit)
        rows = db.execute(stmt).scalars().all()
        items = [InmuebleType(**to_dict(r)) for r in rows]
        return items, page_info(total, limit, offset)

def get_inmueble(id: str):
    with get_db() as db:
        r = db.get(Inmueble, id)
        return InmuebleType(**to_dict(r)) if r else None

def list_comunidades():
    with get_db() as db:
        rows = db.execute(select(ComunidadAutonoma)).scalars().all()
        return [ComunidadAutonomaType(**to_dict(r)) for r in rows]

def list_provincias(comunidad_id: Optional[str] = None):
    with get_db() as db:
        stmt = select(Provincia)
        if comunidad_id:
            stmt = stmt.where(Provincia.comunidad_autonoma_id == comunidad_id)
        rows = db.execute(stmt).scalars().all()
        return [ProvinciaType(**to_dict(r)) for r in rows]

def list_localidades(provincia_id: Optional[str] = None):
    with get_db() as db:
        stmt = select(Localidad)
        if provincia_id:
            stmt = stmt.where(Localidad.provincia_id == provincia_id)
        rows = db.execute(stmt).scalars().all()
        return [LocalidadType(**to_dict(r)) for r in rows]

def list_diocesis():
    with get_db() as db:
        rows = db.execute(select(Diocesis)).scalars().all()
        return [DiocesisType(**to_dict(r)) for r in rows]

def list_figuras():
    with get_db() as db:
        rows = db.execute(select(FiguraProteccion)).scalars().all()
        return [FiguraProteccionType(**to_dict(r)) for r in rows]

def list_inmueble_figuras(inmueble_id: str):
    with get_db() as db:
        rows = db.execute(select(InmuebleFiguraProteccion).where(InmuebleFiguraProteccion.inmueble_id == inmueble_id)).scalars().all()
        return [InmuebleFiguraProteccionType(**to_dict(r)) for r in rows]

def list_inmueble_documentos(inmueble_id: str):
    with get_db() as db:
        stmt = select(Documento).join(InmuebleDocumento, InmuebleDocumento.documento_id == Documento.id).where(InmuebleDocumento.inmueble_id == inmueble_id)
        rows = db.execute(stmt).scalars().all()
        return [DocumentoType(**to_dict(r)) for r in rows]
