# crud_generator.py
"""
CRUD genérico para cualquier modelo SQLAlchemy
"""
from typing import Type, Optional, List, Any, Dict
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.inspection import inspect
import strawberry
import uuid

from .base_types import FilterCondition, OrderBy, PaginationInput, PageInfo, suppress_traceback_continue
from .type_generator import StrawberryTypeGenerator, PropertyDetector, PropertyResolver
from .query_builder import DynamicQueryBuilder

class GenericCRUD:
    """CRUD genérico para cualquier modelo SQLAlchemy con soporte para propiedades"""
    
    def __init__(
        self,
        model: Type,
        strawberry_type: Type = None,
        create_input: Type = None,
        update_input: Type = None
    ):
        self.model = model
        self.strawberry_type = strawberry_type or StrawberryTypeGenerator.generate_strawberry_type(model)
        self.create_input = create_input or StrawberryTypeGenerator.generate_input_type(model, "create")
        self.update_input = update_input or StrawberryTypeGenerator.generate_input_type(model, "update")
        
        # Obtener primary key
        mapper = inspect(model)
        self.pk_column = mapper.primary_key[0].name
        self.pk_type = mapper.primary_key[0].type.python_type
        
        # Detectar propiedades del modelo
        self.properties = PropertyDetector.get_model_properties(model)
        
        # Mejorar el tipo Strawberry con resolvers para propiedades
        self._enhance_strawberry_type()
    
    def _enhance_strawberry_type(self):
        """Mejora el tipo Strawberry añadiendo resolvers para propiedades"""
        for prop_name, prop_info in self.properties.items():
            resolver = PropertyResolver.create_property_resolver(prop_name, prop_info)
            setattr(self.strawberry_type, prop_name, strawberry.field(resolver=resolver))
    
    async def _convert_to_strawberry(self, obj: Any) -> Any:
        """Convierte un objeto SQLAlchemy al tipo Strawberry correspondiente"""
        if not obj:
            return None
        
        data = {}
        
        # Procesar columnas de base de datos
        mapper = inspect(self.model)
        for column in mapper.columns:
            col_name = column.name
            if hasattr(obj, col_name):
                value = getattr(obj, col_name)
                # Convertir UUID a string para GraphQL
                if isinstance(value, uuid.UUID):
                    value = str(value)
                data[col_name] = value
        
        # Crear instancia del tipo Strawberry
        strawberry_instance = self.strawberry_type(**data)
        
        # Asignar la instancia del modelo para que los resolvers de propiedades puedan acceder
        strawberry_instance._model_instance = obj
        
        return strawberry_instance
    
    @suppress_traceback_continue
    async def get_by_id(self, db: AsyncSession, id: Any) -> Optional[Any]:
        """Obtener por ID - maneja diferentes tipos de PK"""
        try:
            # Convertir el ID al tipo correcto de la PK
            if self.pk_type == uuid.UUID:
                id_value = uuid.UUID(str(id))
            elif self.pk_type == int:
                id_value = int(id)
            elif self.pk_type == str:
                id_value = str(id)
            else:
                id_value = id
                
            result = await db.execute(
                select(self.model).where(getattr(self.model, self.pk_column) == id_value)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            print(f"Error obteniendo {self.model.__name__} por ID {id}: {e}")
            return None
    
    @suppress_traceback_continue
    async def get_all(
        self,
        db: AsyncSession,
        filters: Optional[List[FilterCondition]] = None,
        order_by: Optional[List[OrderBy]] = None,
        pagination: Optional[PaginationInput] = None,
        include_deleted: bool = False
    ) -> Dict[str, Any]:
        """Obtener todos con filtros, ordenamiento y paginación"""
        # Query base
        query = select(self.model)
        
        # Filtro de soft delete
        if not include_deleted and hasattr(self.model, 'deleted_at'):
            query = query.where(getattr(self.model, 'deleted_at').is_(None))
        
        # Aplicar filtros
        query = DynamicQueryBuilder.apply_filters(query, self.model, filters)
        
        # Contar total antes de paginar
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total_count = total_result.scalar()
        
        # Aplicar ordenamiento
        query = DynamicQueryBuilder.apply_ordering(query, self.model, order_by)
        
        # Aplicar paginación
        query, page, page_size = DynamicQueryBuilder.apply_pagination(query, pagination)
        
        # Ejecutar query
        result = await db.execute(query)
        items = result.scalars().all()
        
        # Calcular page info
        total_pages = (total_count + page_size - 1) // page_size if page_size > 0 else 1
        has_next = page < total_pages
        has_previous = page > 1
        
        page_info = PageInfo(
            has_next_page=has_next,
            has_previous_page=has_previous,
            total_count=total_count,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
        
        return {
            "items": items,
            "page_info": page_info
        }
    
    @suppress_traceback_continue
    async def get_deleted(
        self,
        db: AsyncSession,
        filters: Optional[List[FilterCondition]] = None,
        order_by: Optional[List[OrderBy]] = None,
        pagination: Optional[PaginationInput] = None
    ) -> Dict[str, Any]:
        """Obtener solo registros eliminados"""
        # Query base para eliminados
        query = select(self.model).where(getattr(self.model, 'deleted_at').isnot(None))
        
        # Aplicar filtros adicionales
        query = DynamicQueryBuilder.apply_filters(query, self.model, filters)
        
        # Contar total antes de paginar
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total_count = total_result.scalar()
        
        # Aplicar ordenamiento
        query = DynamicQueryBuilder.apply_ordering(query, self.model, order_by)
        
        # Aplicar paginación
        query, page, page_size = DynamicQueryBuilder.apply_pagination(query, pagination)
        
        # Ejecutar query
        result = await db.execute(query)
        items = result.scalars().all()
        
        # Calcular page info
        total_pages = (total_count + page_size - 1) // page_size if page_size > 0 else 1
        has_next = page < total_pages
        has_previous = page > 1
        
        page_info = PageInfo(
            has_next_page=has_next,
            has_previous_page=has_previous,
            total_count=total_count,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
        
        return {
            "items": items,
            "page_info": page_info
        }
    
    @suppress_traceback_continue
    async def create(self, db: AsyncSession, data: dict) -> Any:
        """Crear nuevo registro"""
        # Si el modelo tiene UUID como PK y no se proporciona, generarlo
        if (self.pk_type == uuid.UUID and 
            self.pk_column not in data and 
            hasattr(self.model, self.pk_column)):
            data[self.pk_column] = str(uuid.uuid4())
        
        obj = self.model(**data)
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj
    
    @suppress_traceback_continue
    async def update(self, db: AsyncSession, id: Any, data: dict) -> Optional[Any]:
        """Actualizar registro existente"""
        obj = await self.get_by_id(db, id)
        if not obj:
            return None
        
        for key, value in data.items():
            if hasattr(obj, key) and value is not None:
                setattr(obj, key, value)
        
        await db.commit()
        await db.refresh(obj)
        return obj
    
    @suppress_traceback_continue
    async def delete(self, db: AsyncSession, id: Any) -> bool:
        """Eliminar registro (soft delete)"""
        obj = await self.get_by_id(db, id)
        if not obj:
            return False
        
        # Soft delete si el modelo tiene el campo
        if hasattr(obj, 'soft_delete'):
            obj.soft_delete()
        else:
            await db.delete(obj)
        
        await db.commit()
        return True
    
    @suppress_traceback_continue
    async def restore(self, db: AsyncSession, id: Any) -> Optional[Any]:
        """Restaurar registro eliminado"""
        obj = await self.get_by_id(db, id)
        if not obj:
            return None
        
        # Restaurar si el modelo tiene el método
        if hasattr(obj, 'restore'):
            obj.restore()
            await db.commit()
            await db.refresh(obj)
            return obj
        return None