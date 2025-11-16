# schema_generator.py
"""
Generador de queries y mutaciones automáticas
"""
from typing import List, Optional, Dict, Any
import strawberry
from strawberry.types import Info

from .base_types import FilterCondition, OrderBy, PaginationInput, PageInfo, suppress_traceback_continue

class SchemaGenerator:
    """Genera queries y mutaciones automáticamente con soporte para propiedades"""
    
    @staticmethod
    def generate_queries(crud, name_prefix: str):
        """Genera queries para un CRUD"""
        model_name = crud.model.__name__
        
        # Generar tipo de respuesta paginada específico
        response_name = f"Paginated{model_name}Response"
        
        @strawberry.type
        class SpecificPaginatedResponse:
            items: List[str]
            page_info: PageInfo
        
        # Registrar el tipo en globals para que Strawberry lo encuentre
        globals()[response_name] = SpecificPaginatedResponse
        
        @suppress_traceback_continue
        async def get_one(info: Info, id: strawberry.ID) -> Optional[str]:
            db = info.context["db"]
            obj = await crud.get_by_id(db, id)
            return await crud._convert_to_strawberry(obj)
        
        @suppress_traceback_continue
        async def get_many(
            info: Info,
            filters: Optional[List[FilterCondition]] = None,
            order_by: Optional[List[OrderBy]] = None,
            pagination: Optional[PaginationInput] = None
        ) -> SpecificPaginatedResponse:
            db = info.context["db"]
            result = await crud.get_all(db, filters, order_by, pagination, include_deleted=False)
            
            # Convertir items a tipos Strawberry
            strawberry_items = []
            for item in result["items"]:
                strawberry_item = await crud._convert_to_strawberry(item)
                strawberry_items.append(strawberry_item)
            
            return SpecificPaginatedResponse(
                items=strawberry_items,
                page_info=result["page_info"]
            )
        
        @suppress_traceback_continue
        async def get_deleted(
            info: Info,
            filters: Optional[List[FilterCondition]] = None,
            order_by: Optional[List[OrderBy]] = None,
            pagination: Optional[PaginationInput] = None
        ) -> SpecificPaginatedResponse:
            db = info.context["db"]
            result = await crud.get_deleted(db, filters, order_by, pagination)
            
            # Convertir items a tipos Strawberry
            strawberry_items = []
            for item in result["items"]:
                strawberry_item = await crud._convert_to_strawberry(item)
                strawberry_items.append(strawberry_item)
            
            return SpecificPaginatedResponse(
                items=strawberry_items,
                page_info=result["page_info"]
            )
        
        @suppress_traceback_continue
        async def get_all(
            info: Info,
            filters: Optional[List[FilterCondition]] = None,
            order_by: Optional[List[OrderBy]] = None,
            pagination: Optional[PaginationInput] = None
        ) -> SpecificPaginatedResponse:
            db = info.context["db"]
            result = await crud.get_all(db, filters, order_by, pagination, include_deleted=True)
            
            # Convertir items a tipos Strawberry
            strawberry_items = []
            for item in result["items"]:
                strawberry_item = await crud._convert_to_strawberry(item)
                strawberry_items.append(strawberry_item)
            
            return SpecificPaginatedResponse(
                items=strawberry_items,
                page_info=result["page_info"]
            )
        
        return {
            f"{name_prefix}": strawberry.field(resolver=get_one),
            f"{name_prefix}s": strawberry.field(resolver=get_many),
            f"{name_prefix}sBorrados": strawberry.field(resolver=get_deleted),
            f"{name_prefix}sTodos": strawberry.field(resolver=get_all)
        }
    
    @staticmethod
    def generate_mutations(crud, name_prefix: str):
        """Genera mutaciones para un CRUD"""
        
        @suppress_traceback_continue
        async def create_one(info: Info, data: Any) -> str:
            db = info.context["db"]
            data_dict = {k: v for k, v in data.__dict__.items() if v is not None}
            obj = await crud.create(db, data_dict)
            return await crud._convert_to_strawberry(obj)
        
        @suppress_traceback_continue
        async def update_one(
            info: Info,
            id: strawberry.ID,
            data: Any
        ) -> Optional[str]:
            db = info.context["db"]
            data_dict = {k: v for k, v in data.__dict__.items() if v is not None}
            obj = await crud.update(db, id, data_dict)
            return await crud._convert_to_strawberry(obj) if obj else None
        
        @suppress_traceback_continue
        async def delete_one(info: Info, id: strawberry.ID) -> bool:
            db = info.context["db"]
            return await crud.delete(db, id)
        
        @suppress_traceback_continue
        async def restore_one(info: Info, id: strawberry.ID) -> Optional[str]:
            db = info.context["db"]
            obj = await crud.restore(db, id)
            return await crud._convert_to_strawberry(obj) if obj else None
        
        return {
            f"create{name_prefix.capitalize()}": strawberry.mutation(resolver=create_one),
            f"update{name_prefix.capitalize()}": strawberry.mutation(resolver=update_one),
            f"delete{name_prefix.capitalize()}": strawberry.mutation(resolver=delete_one),
            f"restore{name_prefix.capitalize()}": strawberry.mutation(resolver=restore_one)
        }

def get_all_models():
    """Obtiene automáticamente TODOS los modelos de la metadata de SQLAlchemy"""
    from app.db.base import Base
    
    models = []
    
    for mapper in Base.registry.mappers:
        model_class = mapper.class_
        
        if hasattr(model_class, '__tablename__') and model_class.__tablename__ is not None:
            models.append(model_class)
    
    return models