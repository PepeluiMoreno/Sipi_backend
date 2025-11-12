import strawberry
from typing import Optional, List
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, and_
from app.db.session import SessionLocal
from app.db.models import Inmueble, InmuebleFiguraProteccion
from .inputs import InmuebleInput, InmuebleFiguraProteccionInput, InmuebleUpsertNaturalKey
from .types import InmuebleType, InmuebleFiguraProteccionType
from .common import Error

@strawberry.type
class MutationResult:
    ok: bool
    id: Optional[str] = None
    errors: Optional[List[Error]] = None

@strawberry.type
class BatchResult:
    ok: bool
    count: int
    ids: Optional[List[str]] = None
    errors: Optional[List[Error]] = None

def create_inmueble(input: InmuebleInput) -> MutationResult:
    s = SessionLocal()
    try:
        with s.begin():
            obj = Inmueble(**input.__dict__)
            s.add(obj)
            s.flush()
            return MutationResult(ok=True, id=obj.id)
    except IntegrityError as e:
        s.rollback()
        return MutationResult(ok=False, errors=[Error(code="INTEGRITY", message=str(e))])
    finally:
        s.close()


def upsert_inmueble_by_natural_key(key: InmuebleUpsertNaturalKey, patch: InmuebleInput) -> MutationResult:
    s = SessionLocal()
    try:
        with s.begin():
            stmt = select(Inmueble).where(
                and_(Inmueble.nombre == key.nombre,
                     Inmueble.provincia_id == key.provincia_id,
                     Inmueble.localidad_id == key.localidad_id)
            )
            obj = s.execute(stmt).scalars().first()
            if obj:
                for k, v in patch.__dict__.items():
                    setattr(obj, k, v)
                return MutationResult(ok=True, id=obj.id)
            obj = Inmueble(**patch.__dict__)
            s.add(obj)
            s.flush()
            return MutationResult(ok=True, id=obj.id)
    except IntegrityError as e:
        s.rollback()
        return MutationResult(ok=False, errors=[Error(code="INTEGRITY", message=str(e))])
    finally:
        s.close()


def batch_upsert_inmuebles(items: List[InmuebleInput]) -> BatchResult:
    s = SessionLocal()
    ids = []
    try:
        with s.begin():
            for data in items:
                obj = Inmueble(**data.__dict__)
                s.add(obj)
                s.flush()
                ids.append(obj.id)
        return BatchResult(ok=True, count=len(ids), ids=ids)
    except IntegrityError as e:
        s.rollback()
        return BatchResult(ok=False, count=0, errors=[Error(code="INTEGRITY", message=str(e))])
    finally:
        s.close()


def delete_inmueble(id: str) -> MutationResult:
    s = SessionLocal()
    try:
        with s.begin():
            obj = s.get(Inmueble, id)
            if not obj:
                return MutationResult(ok=False, errors=[Error(code="NOT_FOUND", message="Inmueble no existe")])
            s.delete(obj)
            return MutationResult(ok=True, id=id)
    finally:
        s.close()


def upsert_inmueble_figura(input: InmuebleFiguraProteccionInput) -> MutationResult:
    s = SessionLocal()
    try:
        with s.begin():
            stmt = select(InmuebleFiguraProteccion).where(
                InmuebleFiguraProteccion.inmueble_id == input.inmueble_id,
                InmuebleFiguraProteccion.figura_proteccion_id == input.figura_proteccion_id
            )
            existing = s.execute(stmt).scalars().first()
            if existing:
                for k, v in input.__dict__.items():
                    setattr(existing, k, v)
                return MutationResult(ok=True, id=existing.id)
            obj = InmuebleFiguraProteccion(**input.__dict__)
            s.add(obj)
            s.flush()
            return MutationResult(ok=True, id=obj.id)
    except IntegrityError as e:
        s.rollback()
        return MutationResult(ok=False, errors=[Error(code="INTEGRITY", message=str(e))])
    finally:
        s.close()
