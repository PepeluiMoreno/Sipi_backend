"""
Generador de schema GraphQL completo a partir de modelos y GenericCRUD
"""
from typing import Type, List, Optional, Dict, Any
import strawberry
from sqlalchemy.orm import DeclarativeBase
from .crud_generator import GenericCRUD
from .query_builder import QueryBuilder
from .type_generator import StrawberryTypeGenerator, PropertyResolver
from .base_types import suppress_traceback_continue, FilterCondition, OrderBy, PaginationInput, PageInfo

class SchemaGenerator:
    """Genera schema GraphQL completo con queries, mutaciones y propiedades"""

    @staticmethod
    def get_models_from_base(base_class: DeclarativeBase) -> List[Type]:
        """Obtiene todos los modelos de SQLAlchemy desde la base"""
        return base_class.__subclasses__()

    @staticmethod
    def generate_crud_for_model(model_class: Type) -> Dict[str, Any]:
        """Genera queries, mutaciones e inputs para un modelo"""
        crud = GenericCRUD(model_class)
        model_name = model_class.__name__
        name_prefix = model_name.lower()

        # Generar queries
        queries = QueryBuilder.build_queries(crud, name_prefix)

        # Generar mutaciones básicas
        mutations = SchemaGenerator.generate_mutations(crud, name_prefix)

        # Generar tipos Strawberry y Inputs
        strawberry_type = StrawberryTypeGenerator.generate_strawberry_type(model_class)
        create_input = StrawberryTypeGenerator.generate_input_type(model_class, operation="create")
        update_input = StrawberryTypeGenerator.generate_input_type(model_class, operation="update")

        return {
            "crud": crud,
            "queries": queries,
            "mutations": mutations,
            "strawberry_type": strawberry_type,
            "create_input": create_input,
            "update_input": update_input
        }

    @staticmethod
    def generate_mutations(crud: GenericCRUD, name_prefix: str):
        """Genera mutaciones básicas de create, update, delete y restore"""
        mutations = {}

        @suppress_traceback_continue
        async def create_one(info, data):
            db = info.context["db"]
            instance = await crud.create(db, data.__dict__)
            return await StrawberryTypeGenerator._convert_to_strawberry(instance)

        @suppress_traceback_continue
        async def update_one(info, id, data):
            db = info.context["db"]
            instance = await crud.update(db, id, data.__dict__)
            return await StrawberryTypeGenerator._convert_to_strawberry(instance) if instance else None

        @suppress_traceback_continue
        async def delete_one(info, id):
            db = info.context["db"]
            return await crud.delete(db, id)

        @suppress_traceback_continue
        async def restore_one(info, id):
            db = info.context["db"]
            instance = await crud.restore(db, id)
            return await StrawberryTypeGenerator._convert_to_strawberry(instance) if instance else None

        mutations[f"create{name_prefix.capitalize()}"] = strawberry.mutation(resolver=create_one)
        mutations[f"update{name_prefix.capitalize()}"] = strawberry.mutation(resolver=update_one)
        mutations[f"delete{name_prefix.capitalize()}"] = strawberry.mutation(resolver=delete_one)
        mutations[f"restore{name_prefix.capitalize()}"] = strawberry.mutation(resolver=restore_one)

        return mutations

    @staticmethod
    def generate_complete_schema(base_class: Type[DeclarativeBase]):
        """Genera schema completo a partir de todos los modelos de la base"""
        models = SchemaGenerator.get_models_from_base(base_class)

        all_queries = {}
        all_mutations = {}

        for model in models:
            result = SchemaGenerator.generate_crud_for_model(model)
            all_queries.update(result["queries"])
            all_mutations.update(result["mutations"])

        # Crear tipos Query y Mutation dinámicamente
        Query = type("Query", (), all_queries)
        Mutation = type("Mutation", (), all_mutations)

        return strawberry.Schema(query=Query, mutation=Mutation)
