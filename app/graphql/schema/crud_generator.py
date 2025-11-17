
"""
Generador de operaciones CRUD genéricas para modelos SQLAlchemy
"""
from typing import Type, Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload
import strawberry

from .type_generator import StrawberryTypeGenerator

# ==============================
# Generic CRUD
# ==============================

class GenericCRUD:
    """Generador CRUD para un modelo SQLAlchemy"""

    def __init__(self, model: Type):
        self.model = model
        self.model_name = model.__name__
        self.properties = StrawberryTypeGenerator.generate_strawberry_type(model)._type_definition.fields
        self.input_create = StrawberryTypeGenerator.generate_input_type(model, "create")
        self.input_update = StrawberryTypeGenerator.generate_input_type(model, "update")

    # ----------------------
    # CREATE
    # ----------------------
    async def create(self, session: AsyncSession, input_data: Dict[str, Any]):
        instance = self.model(**input_data)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance

    # ----------------------
    # READ
    # ----------------------
    async def get_by_id(self, session: AsyncSession, id: Any):
        stmt = select(self.model).where(self.model.id == id)
        result = await session.execute(stmt)
        instance = result.scalar_one_or_none()
        if not instance:
            raise NoResultFound(f"{self.model_name} with id {id} not found")
        return instance

    async def list_all(self, session: AsyncSession, filters: Optional[Dict[str, Any]] = None, offset: int = 0, limit: int = 20):
        stmt = select(self.model)
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field):
                    stmt = stmt.where(getattr(self.model, field) == value)
        stmt = stmt.offset(offset).limit(limit)
        result = await session.execute(stmt)
        return result.scalars().all()

    # ----------------------
    # UPDATE
    # ----------------------
    async def update(self, session: AsyncSession, id: Any, input_data: Dict[str, Any]):
        stmt = select(self.model).where(self.model.id == id)
        result = await session.execute(stmt)
        instance = result.scalar_one_or_none()
        if not instance:
            raise NoResultFound(f"{self.model_name} with id {id} not found")
        for key, value in input_data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance

    # ----------------------
    # DELETE
    # ----------------------
    async def delete(self, session: AsyncSession, id: Any):
        stmt = select(self.model).where(self.model.id == id)
        result = await session.execute(stmt)
        instance = result.scalar_one_or_none()
        if not instance:
            raise NoResultFound(f"{self.model_name} with id {id} not found")
        await session.delete(instance)
        await session.commit()
        return instance
