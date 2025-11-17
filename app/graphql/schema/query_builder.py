"""
Construcción de queries y resolvers GraphQL a partir de GenericCRUD
"""
from typing import List, Optional, Dict, Any, Callable
import strawberry
from strawberry.types import Info
from .crud_generator import GenericCRUD
from .type_generator import PropertyResolver, StrawberryTypeGenerator
from .base_types import FilterCondition, OrderBy, PaginationInput, PageInfo, suppress_traceback_continue

# ==============================
# Query Builder
# ==============================

class QueryBuilder:
    """Genera queries y resolvers GraphQL desde GenericCRUD"""

    @staticmethod
    def build_queries(crud: GenericCRUD, name_prefix: str = None) -> Dict[str, strawberry.field]:
        if name_prefix is None:
            name_prefix = crud.model_name.lower()

        queries = {}

        # Resolver para obtener uno por ID
        @suppress_traceback_continue
        async def get_one(info: Info, id: strawberry.ID):
            db = info.context["db"]
            instance = await crud.get_by_id(db, id)
            return await StrawberryTypeGenerator._convert_to_strawberry(instance)

        # Resolver para obtener lista
        @suppress_traceback_continue
        async def get_many(
            info: Info,
            filters: Optional[List[FilterCondition]] = None,
            order_by: Optional[List[OrderBy]] = None,
            pagination: Optional[PaginationInput] = None
        ):
            db = info.context["db"]
            offset = pagination.page * pagination.page_size if pagination else 0
            limit = pagination.page_size if pagination else 20
            filter_dict = {f.field: f.value for f in filters} if filters else {}
            items = await crud.list_all(db, filter_dict, offset, limit)
            return {
                "items": [await StrawberryTypeGenerator._convert_to_strawberry(item) for item in items],
                "page_info": PageInfo(
                    total=len(items),
                    page=pagination.page if pagination else 1,
                    page_size=pagination.page_size if pagination else 20
                )
            }

        queries[f"{name_prefix}"] = strawberry.field(resolver=get_one)
        queries[f"{name_prefix}s"] = strawberry.field(resolver=get_many)

        return queries

