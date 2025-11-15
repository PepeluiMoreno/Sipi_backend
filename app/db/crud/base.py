# app/db/crud/base.py
from typing import Any, Dict, List, Optional, Generic, TypeVar
from sqlalchemy.orm import Session
from app.db.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)

class CRUDBase(Generic[ModelType]):
    def __init__(self, model: type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def list(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: Dict[str, Any]) -> ModelType:
        obj_data = obj_in
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        db.flush()
        return db_obj

    def update(self, db: Session, *, db_obj: ModelType, obj_in: Dict[str, Any]) -> ModelType:
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        db.add(db_obj)
        db.flush()
        return db_obj

    def delete(self, db: Session, *, db_obj: ModelType) -> ModelType:
        db.delete(db_obj)
        db.flush()
        return db_obj