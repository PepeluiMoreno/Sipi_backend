from __future__ import annotations
import strawberry
from typing import List, Optional, Type
from strawberry.types import Info
from sqlalchemy.orm import Session
from app.db.models.base import Base
from app.db.crud.base import CRUDBase

from .generate_strawberry_types import generate_strawberry_types

# Generar tipos Strawberry
generated_types = generate_strawberry_types(Base, include_relationships=False)

# Registrar tipos en el ámbito global
for type_name, strawberry_type in generated_types.items():
    globals()[type_name] = strawberry_type

# Preparar queries y mutations
query_fields = {}
mutation_fields = {}

# Factory functions corregidas
def create_list_resolver(crud: CRUDBase, strawberry_type: Type):
    async def resolver(
        info: Info,
        limit: int = 50,
        offset: int = 0
    ) -> List[strawberry_type]:
        db = info.context["db"]
        items = crud.list(db, limit=limit, offset=offset)
        results = []
        for item in items:
            data = {}
            for column in item.__table__.columns:
                column_name = column.key
                if hasattr(strawberry_type, '__annotations__') and column_name in strawberry_type.__annotations__:
                    data[column_name] = getattr(item, column_name)
            results.append(strawberry_type(**data))
        return results
    return resolver

def create_get_resolver(crud: CRUDBase, strawberry_type: Type):
    async def resolver(
        info: Info,
        id: strawberry.ID
    ) -> Optional[strawberry_type]:
        db = info.context["db"]
        item = crud.get(db, id)
        if not item:
            return None
        
        data = {}
        for column in item.__table__.columns:
            column_name = column.key
            if hasattr(strawberry_type, '__annotations__') and column_name in strawberry_type.__annotations__:
                data[column_name] = getattr(item, column_name)
        return strawberry_type(**data)
    return resolver

def create_input_type(model_class, strawberry_type: Type):
    input_annotations = {}
    
    for column in model_class.__table__.columns:
        column_name = column.key
        if column_name.startswith("_"):
            continue
            
        if hasattr(strawberry_type, '__annotations__') and column_name in strawberry_type.__annotations__:
            field_type = strawberry_type.__annotations__[column_name]
            
            if not column.primary_key:
                input_annotations[column_name] = Optional[field_type]
    
    input_class_name = f"{model_class.__name__}Input"
    
    InputType = type(
        input_class_name,
        (),
        {'__annotations__': input_annotations}
    )
    
    InputType = strawberry.input(InputType)
    return input_class_name, InputType

# Resolvers específicos con anotaciones completas
def create_create_resolver(crud: CRUDBase, strawberry_type: Type, input_class_name: str):
    InputTypeClass = globals()[input_class_name]
    
    async def resolver(
        info: Info,
        input: InputTypeClass
    ) -> strawberry_type:
        db = info.context["db"]
        input_dict = {k: v for k, v in input.__dict__.items() if v is not None}
        obj = crud.create(db, input_dict)
        db.commit()
        db.refresh(obj)
        
        data = {}
        for column in obj.__table__.columns:
            column_name = column.key
            if hasattr(strawberry_type, '__annotations__') and column_name in strawberry_type.__annotations__:
                data[column_name] = getattr(obj, column_name)
        return strawberry_type(**data)
    return resolver

def create_update_resolver(crud: CRUDBase, strawberry_type: Type, input_class_name: str):
    InputTypeClass = globals()[input_class_name]
    
    async def resolver(
        info: Info,
        id: strawberry.ID,  # ← ANOTACIÓN AÑADIDA AQUÍ
        input: InputTypeClass
    ) -> Optional[strawberry_type]:
        db = info.context["db"]
        db_obj = crud.get(db, id)
        if not db_obj:
            return None
            
        input_dict = {k: v for k, v in input.__dict__.items() if v is not None}
        updated = crud.update(db, db_obj, input_dict)
        db.commit()
        db.refresh(updated)
        
        data = {}
        for column in updated.__table__.columns:
            column_name = column.key
            if hasattr(strawberry_type, '__annotations__') and column_name in strawberry_type.__annotations__:
                data[column_name] = getattr(updated, column_name)
        return strawberry_type(**data)
    return resolver

def create_delete_resolver(crud: CRUDBase):
    async def resolver(
        info: Info,
        id: strawberry.ID
    ) -> bool:
        db = info.context["db"]
        db_obj = crud.get(db, id)
        if not db_obj:
            return False
        crud.delete(db, db_obj)
        db.commit()
        return True
    return resolver

# Procesar cada modelo
for model_class_name, strawberry_type in generated_types.items():
    model_class = None
    for mapper in Base.registry.mappers:
        if mapper.class_.__name__ == model_class_name:
            model_class = mapper.class_
            break
    
    if not model_class:
        continue
        
    name = model_class.__name__
    crud = CRUDBase(model_class)
    
    input_class_name, InputType = create_input_type(model_class, strawberry_type)
    globals()[input_class_name] = InputType
    
    list_resolver = create_list_resolver(crud, strawberry_type)
    get_resolver = create_get_resolver(crud, strawberry_type)
    create_resolver = create_create_resolver(crud, strawberry_type, input_class_name)
    update_resolver = create_update_resolver(crud, strawberry_type, input_class_name)
    delete_resolver = create_delete_resolver(crud)
    
    model_name_lower = name.lower()
    query_fields[f"list_{model_name_lower}"] = strawberry.field(resolver=list_resolver)
    query_fields[f"get_{model_name_lower}"] = strawberry.field(resolver=get_resolver)
    mutation_fields[f"create_{model_name_lower}"] = strawberry.field(resolver=create_resolver)
    mutation_fields[f"update_{model_name_lower}"] = strawberry.field(resolver=update_resolver)
    mutation_fields[f"delete_{model_name_lower}"] = strawberry.field(resolver=delete_resolver)

Query = strawberry.type(type("Query", (), query_fields))
Mutation = strawberry.type(type("Mutation", (), mutation_fields))

# Crear schema
schema = strawberry.Schema(query=Query, mutation=Mutation)