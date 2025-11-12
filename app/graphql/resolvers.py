from typing import Optional, List
from strawberry.types import Info
from sqlalchemy.orm import Session
from app.db.models import Inmueble, Localidad, Provincia, Diocesis

def resolve_inmueble(info: Info, id: str) -> Optional[Inmueble]:
    db: Session = info.context["db"]
    return db.get(Inmueble, id)

def resolve_inmuebles(info: Info, limit: int = 100) -> list[Inmueble]:
    db: Session = info.context["db"]
    return db.query(Inmueble).limit(limit).all()

def resolve_localidades(info: Info) -> list[Localidad]:
    db: Session = info.context["db"]
    return db.query(Localidad).all()

def resolve_provincias(info: Info) -> list[Provincia]:
    db: Session = info.context["db"]
    return db.query(Provincia).all()

def resolve_diocesis(info: Info) -> list[Diocesis]:
    db: Session = info.context["db"]
    return db.query(Diocesis).all()
