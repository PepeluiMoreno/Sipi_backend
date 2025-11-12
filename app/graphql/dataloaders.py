from aiodataloader import DataLoader
from sqlalchemy import select
from typing import Iterable, Any
from app.db import SessionLocal

class ByIdLoader(DataLoader):
    def __init__(self, model):
        super().__init__()
        self.model = model

    async def batch_load_fn(self, keys: Iterable[str]) -> list[Any]:
        s = SessionLocal()
        try:
            rows = s.execute(select(self.model).where(self.model.id.in_(keys))).scalars().all()
            by_id = {r.id: r for r in rows}
            return [by_id.get(k) for k in keys]
        finally:
            s.close()
