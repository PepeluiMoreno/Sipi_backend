
from __future__ import annotations
import asyncio
from typing import Any, Callable, Dict, Iterable, List, Tuple, Type
from sqlalchemy.orm import Session
from collections import defaultdict

# Minimal synchronous batching DataLoader without external deps
class SimpleDataLoader:
    def __init__(self, batch_load_fn: Callable[[List[Any]], Dict[Any, Any]]):
        self.batch_load_fn = batch_load_fn

    async def load_many(self, keys: List[Any]) -> List[Any]:
        loop = asyncio.get_event_loop()
        result_map = await loop.run_in_executor(None, self.batch_load_fn, keys)
        return [result_map.get(k) for k in keys]

    async def load(self, key: Any) -> Any:
        res = await self.load_many([key])
        return res[0] if res else None

def build_by_id_loader(db: Session, model_cls: Type) -> SimpleDataLoader:
    def batch(keys: List[Any]) -> Dict[Any, Any]:
        rows = db.query(model_cls).filter(model_cls.id.in_(keys)).all()
        return {r.id: r for r in rows}
    return SimpleDataLoader(batch)

def build_foreign_key_group_loader(db: Session, model_cls: Type, fk_name: str) -> SimpleDataLoader:
    def batch(keys: List[Any]) -> Dict[Any, List[Any]]:
        rows = db.query(model_cls).filter(getattr(model_cls, fk_name).in_(keys)).all()
        grouped: Dict[Any, List[Any]] = defaultdict(list)
        for r in rows:
            grouped[getattr(r, fk_name)].append(r)
        return grouped
    return SimpleDataLoader(batch)

def build_dataloaders(db: Session) -> Dict[str, Any]:
    from app.db.models import (
        Inmueble, Provincia, Localidad, Diocesis,
        InmuebleFiguraProteccion, FiguraProteccion
    )
    return {
        "inmueble_by_id": build_by_id_loader(db, Inmueble),
        "provincia_by_id": build_by_id_loader(db, Provincia),
        "localidad_by_id": build_by_id_loader(db, Localidad),
        "diocesis_by_id": build_by_id_loader(db, Diocesis),
        "protecciones_by_inmueble": build_foreign_key_group_loader(db, InmuebleFiguraProteccion, "inmueble_id"),
        "figura_by_id": build_by_id_loader(db, FiguraProteccion),
    }
