"""
Sistema genérico para generar automáticamente CRUD completo con Strawberry GraphQL
Soporta SQLAlchemy, filtros dinámicos, paginación, relaciones y propiedades
"""
from typing import TypeVar, Generic, Type, Optional, List, Any, Dict, get_args, get_origin, Callable
from datetime import datetime, date
from decimal import Decimal
import strawberry
from strawberry.types import Info
from strawberry.field import StrawberryField
from sqlalchemy import select, func, and_, or_, asc, desc
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.inspection import inspect
from enum import Enum
import uuid
import inspect as python_inspect
from types import MethodType

# Importar la Base de datos principal
from app.db.base import Base

# ==================== TIPOS BASE ====================

@strawberry.type
class PageInfo:
    """Información de paginación"""
    has_next_page: bool
    has_previous_page: bool
    total_count: int
    page: int
    page_size: int
    total_pages: int


T = TypeVar('T')


@strawberry.type
class PaginatedResponse(Generic[T]):
    """Respuesta paginada genérica"""
    items: List[T]
    page_info: PageInfo


# ==================== ENUMS GENÉRICOS ====================

@strawberry.enum
class OrderDirection(Enum):
    ASC = "asc"
    DESC = "desc"


@strawberry.enum
class FilterOperator(Enum):
    """Operadores para filtros dinámicos"""
    EQ = "eq"           # Igual
    NE = "ne"           # No igual
    GT = "gt"           # Mayor que
    GTE = "gte"         # Mayor o igual
    LT = "lt"           # Menor que
    LTE = "lte"         # Menor o igual
    LIKE = "like"       # LIKE (case sensitive)
    ILIKE = "ilike"     # ILIKE (case insensitive)
    IN = "in"           # IN
    NOT_IN = "not_in"   # NOT IN
    IS_NULL = "is_null" # IS NULL
    BETWEEN = "between" # BETWEEN


# ==================== INPUTS GENÉRICOS ====================

@strawberry.input
class FilterCondition:
    """Condición de filtro dinámica"""
    field: str
    operator: FilterOperator
    value: Optional[strawberry.scalars.JSON] = None
    values: Optional[List[strawberry.scalars.JSON]] = None


@strawberry.input
class OrderBy:
    """Ordenamiento"""
    field: str
    direction: OrderDirection = OrderDirection.ASC


@strawberry.input
class PaginationInput:
    """Input de paginación"""
    page: int = 1
    page_size: int = 20


# ==================== DETECTOR DE PROPIEDADES ====================

class PropertyDetector:
    """Detecta propiedades y métodos en modelos SQLAlchemy"""
    
    @staticmethod
    def is_property_method(obj) -> bool:
        """Determina si un objeto es una propiedad (@property)"""
        return isinstance(obj, property) or (
            hasattr(obj, 'fget') and obj.fget is not None
        )
    
    @staticmethod
    def is_callable_method(obj) -> bool:
        """Determina si un objeto es un método callable que puede ser útil"""
        return callable(obj) and not isinstance(obj, type) and not obj.__name__.startswith('_')
    
    @staticmethod
    def get_model_properties(model: Type) -> Dict[str, Any]:
        """Obtiene todas las propiedades y métodos útiles de un modelo"""
        properties = {}
        
        # Obtener todas las propiedades (@property)
        for attr_name in dir(model):
            if attr_name.startswith('_'):
                continue
                
            attr = getattr(model, attr_name)
            
            # Detectar propiedades (@property)
            if PropertyDetector.is_property_method(attr):
                properties[attr_name] = {
                    'type': 'property',
                    'obj': attr,
                    'return_type': PropertyDetector.infer_return_type(attr)
                }
            
            # Detectar métodos útiles (excluyendo métodos internos)
            elif (PropertyDetector.is_callable_method(attr) and 
                  hasattr(attr, '__name__') and 
                  not attr_name.startswith('_')):
                # Excluir métodos de SQLAlchemy y métodos especiales
                excluded_prefixes = ['query', 'metadata', 'register', 'test_']
                if not any(attr_name.startswith(prefix) for prefix in excluded_prefixes):
                    properties[attr_name] = {
                        'type': 'method',
                        'obj': attr,
                        'return_type': PropertyDetector.infer_return_type(attr)
                    }
        
        return properties
    
    @staticmethod
    def infer_return_type(prop_obj) -> Type:
        """Infiere el tipo de retorno de una propiedad o método"""
        try:
            # Para propiedades
            if hasattr(prop_obj, 'fget') and prop_obj.fget is not None:
                func = prop_obj.fget
            else:
                func = prop_obj
            
            # Intentar obtener anotaciones de tipo
            if hasattr(func, '__annotations__') and 'return' in func.__annotations__:
                return func.__annotations__['return']
            
            # Para métodos sin anotación, intentar inferir del nombre
            if hasattr(func, '__name__'):
                name = func.__name__.lower()
                if name.startswith('is_') or name.startswith('has_') or name.startswith('tiene_'):
                    return bool
                elif name.startswith('get_') or name.endswith('_list'):
                    return List[Any]
                elif 'count' in name or 'total' in name:
                    return int
                elif 'date' in name or 'fecha' in name:
                    return date
                elif 'datetime' in name:
                    return datetime
            
            # Por defecto, string
            return str
            
        except Exception:
            return str


# ==================== GENERADOR DE TIPOS STRAWBERRY MEJORADO ====================

class StrawberryTypeGenerator:
    """Genera tipos Strawberry desde modelos SQLAlchemy incluyendo propiedades"""
    
    _type_mapping = {
        int: int,
        str: str,
        float: float,
        bool: bool,
        datetime: datetime,
        date: date,
        Decimal: float,
        List: List[Any],
        dict: strawberry.scalars.JSON,
    }
    
    @classmethod
    def _should_be_id(cls, column) -> bool:
        """Determina si una columna debe ser strawberry.ID"""
        return column.primary_key or column.name == 'id'
    
    @classmethod
    def python_type_to_strawberry(cls, python_type: Type, column=None) -> Type:
        """Convierte tipo Python a tipo Strawberry"""
        # Manejar Optional
        origin = get_origin(python_type)
        if origin is Optional:
            args = get_args(python_type)
            if len(args) > 0:
                inner_type = cls.python_type_to_strawberry(args[0], column)
                return Optional[inner_type]
        
        # Manejar List
        if origin is list:
            args = get_args(python_type)
            if len(args) > 0:
                inner_type = cls.python_type_to_strawberry(args[0], column)
                return List[inner_type]
            return List[Any]
        
        # Manejar enums
        if isinstance(python_type, type) and issubclass(python_type, enum.Enum):
            return python_type
        
        # Manejar UUID e IDs
        if python_type == uuid.UUID:
            return strawberry.ID
        
        # Para columnas específicas, verificar si son IDs
        if column and cls._should_be_id(column):
            return strawberry.ID
            
        return cls._type_mapping.get(python_type, str)
    
    @classmethod
    def generate_strawberry_type(cls, model: Type, type_name: str = None) -> Type:
        """Genera un tipo Strawberry desde un modelo SQLAlchemy incluyendo propiedades"""
        if type_name is None:
            type_name = f"{model.__name__}Type"
        
        mapper = inspect(model)
        fields = {}
        
        # Procesar columnas de la base de datos
        for column in mapper.columns:
            col_name = column.name
            python_type = column.type.python_type
            strawberry_type = cls.python_type_to_strawberry(python_type, column)
            
            # Manejar nullable
            if column.nullable:
                fields[col_name] = Optional[strawberry_type]
            else:
                fields[col_name] = strawberry_type
        
        # Procesar propiedades y métodos del modelo
        properties = PropertyDetector.get_model_properties(model)
        for prop_name, prop_info in properties.items():
            return_type = prop_info['return_type']
            strawberry_type = cls.python_type_to_strawberry(return_type)
            fields[prop_name] = strawberry_type
        
        # Crear el tipo dinámicamente
        strawberry_type = strawberry.type(
            type(type_name, (), {"__annotations__": fields})
        )
        
        return strawberry_type

    @classmethod
    def generate_input_type(cls, model: Type, operation: str = "create") -> Type:
        """Genera un Input Strawberry para crear/actualizar"""
        type_name = f"{model.__name__}{operation.capitalize()}Input"
        
        mapper = inspect(model)
        fields = {}
        
        for column in mapper.columns:
            col_name = column.name
            
            # Skip ID en create, opcional en update
            if column.primary_key:
                if operation == "create":
                    continue
                elif operation == "update":
                    fields[col_name] = Optional[strawberry.ID]
                    continue
            
            # Skip campos auto-generados
            if column.server_default is not None or column.default is not None:
                python_type = column.type.python_type
                strawberry_type = cls.python_type_to_strawberry(python_type, column)
                fields[col_name] = Optional[strawberry_type]
                continue
            
            python_type = column.type.python_type
            strawberry_type = cls.python_type_to_strawberry(python_type, column)
            
            # En create: requerido si not nullable, en update: todo opcional
            if operation == "create":
                if column.nullable:
                    fields[col_name] = Optional[strawberry_type]
                else:
                    fields[col_name] = strawberry_type
            else:  # update
                fields[col_name] = Optional[strawberry_type]
        
        # Crear el input dinámicamente
        input_type = strawberry.input(
            type(type_name, (), {"__annotations__": fields})
        )
        
        return input_type


# ==================== RESOLVER DE PROPIEDADES ====================

class PropertyResolver:
    """Resuelve propiedades y métodos en resolvers GraphQL"""
    
    @staticmethod
    def create_property_resolver(prop_name: str, prop_info: Dict) -> Callable:
        """Crea un resolver para una propiedad o método"""
        
        async def resolver(self, info: Info) -> Any:
            try:
                # Obtener la instancia del modelo
                model_instance = self._model_instance
                
                # Obtener el valor de la propiedad/método
                prop_value = getattr(model_instance, prop_name)
                
                # Si es un método, llamarlo
                if prop_info['type'] == 'method' and callable(prop_value):
                    result = prop_value()
                    # Si es una coroutine, esperarla
                    if hasattr(result, '__await__'):
                        result = await result
                    return result
                # Si es una propiedad, retornar directamente
                else:
                    return prop_value
                    
            except Exception as e:
                print(f"Error resolviendo propiedad {prop_name}: {e}")
                return None
        
        return resolver


# ==================== QUERY BUILDER ====================

class DynamicQueryBuilder:
    """Construye queries SQLAlchemy dinámicamente"""
    
    @staticmethod
    def apply_filters(query, model: Type, filters: Optional[List[FilterCondition]]):
        """Aplica filtros dinámicos a la query"""
        if not filters:
            return query
        
        conditions = []
        for filter_cond in filters:
            column = getattr(model, filter_cond.field, None)
            if column is None:
                continue
            
            op = filter_cond.operator
            value = filter_cond.value
            values = filter_cond.values
            
            if op == FilterOperator.EQ:
                conditions.append(column == value)
            elif op == FilterOperator.NE:
                conditions.append(column != value)
            elif op == FilterOperator.GT:
                conditions.append(column > value)
            elif op == FilterOperator.GTE:
                conditions.append(column >= value)
            elif op == FilterOperator.LT:
                conditions.append(column < value)
            elif op == FilterOperator.LTE:
                conditions.append(column <= value)
            elif op == FilterOperator.LIKE:
                conditions.append(column.like(f"%{value}%"))
            elif op == FilterOperator.ILIKE:
                conditions.append(column.ilike(f"%{value}%"))
            elif op == FilterOperator.IN:
                if values:
                    conditions.append(column.in_(values))
            elif op == FilterOperator.NOT_IN:
                if values:
                    conditions.append(~column.in_(values))
            elif op == FilterOperator.IS_NULL:
                if value:
                    conditions.append(column.is_(None))
                else:
                    conditions.append(column.isnot(None))
            elif op == FilterOperator.BETWEEN:
                if values and len(values) == 2:
                    conditions.append(column.between(values[0], values[1]))
        
        if conditions:
            query = query.where(and_(*conditions))
        
        return query
    
    @staticmethod
    def apply_ordering(query, model: Type, order_by: Optional[List[OrderBy]]):
        """Aplica ordenamiento a la query"""
        if not order_by:
            return query
        
        for order in order_by:
            column = getattr(model, order.field, None)
            if column is None:
                continue
            
            if order.direction == OrderDirection.ASC:
                query = query.order_by(asc(column))
            else:
                query = query.order_by(desc(column))
        
        return query
    
    @staticmethod
    def apply_pagination(query, pagination: Optional[PaginationInput]):
        """Aplica paginación a la query"""
        if not pagination:
            return query, 1, 20
        
        page = max(1, pagination.page)
        page_size = max(1, min(100, pagination.page_size))
        
        offset = (page - 1) * page_size
        query = query.limit(page_size).offset(offset)
        
        return query, page, page_size


# ==================== CRUD GENÉRICO MEJORADO ====================

class GenericCRUD(Generic[T]):
    """CRUD genérico para cualquier modelo SQLAlchemy con soporte para propiedades"""
    
    def __init__(
        self,
        model: Type[T],
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
    
    async def _convert_to_strawberry(self, obj: T) -> Any:
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
    
    async def get_by_id(self, db: AsyncSession, id: Any) -> Optional[T]:
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
    
    async def create(self, db: AsyncSession, data: dict) -> T:
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
    
    async def update(self, db: AsyncSession, id: Any, data: dict) -> Optional[T]:
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
    
    async def restore(self, db: AsyncSession, id: Any) -> Optional[T]:
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


# ==================== GENERADOR DE SCHEMA MEJORADO ====================

class SchemaGenerator:
    """Genera queries y mutaciones automáticamente con soporte para propiedades"""
    
    @staticmethod
    def generate_queries(crud: GenericCRUD, name_prefix: str):
        """Genera queries para un CRUD"""
        model_name = crud.model.__name__
        
        # Generar tipo de respuesta paginada específico
        response_name = f"Paginated{model_name}Response"
        
        @strawberry.type
        class SpecificPaginatedResponse:
            items: List[crud.strawberry_type]
            page_info: PageInfo
        
        # Registrar el tipo en globals para que Strawberry lo encuentre
        globals()[response_name] = SpecificPaginatedResponse
        
        async def get_one(info: Info, id: strawberry.ID) -> Optional[crud.strawberry_type]:
            db = info.context["db"]
            obj = await crud.get_by_id(db, id)
            return await crud._convert_to_strawberry(obj)
        
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
    def generate_mutations(crud: GenericCRUD, name_prefix: str):
        """Genera mutaciones para un CRUD"""
        
        async def create_one(info: Info, data: crud.create_input) -> crud.strawberry_type:
            db = info.context["db"]
            data_dict = {k: v for k, v in data.__dict__.items() if v is not None}
            obj = await crud.create(db, data_dict)
            return await crud._convert_to_strawberry(obj)
        
        async def update_one(
            info: Info,
            id: strawberry.ID,
            data: crud.update_input
        ) -> Optional[crud.strawberry_type]:
            db = info.context["db"]
            data_dict = {k: v for k, v in data.__dict__.items() if v is not None}
            obj = await crud.update(db, id, data_dict)
            return await crud._convert_to_strawberry(obj) if obj else None
        
        async def delete_one(info: Info, id: strawberry.ID) -> bool:
            db = info.context["db"]
            return await crud.delete(db, id)
        
        async def restore_one(info: Info, id: strawberry.ID) -> Optional[crud.strawberry_type]:
            db = info.context["db"]
            obj = await crud.restore(db, id)
            return await crud._convert_to_strawberry(obj) if obj else None
        
        return {
            f"create{name_prefix.capitalize()}": strawberry.mutation(resolver=create_one),
            f"update{name_prefix.capitalize()}": strawberry.mutation(resolver=update_one),
            f"delete{name_prefix.capitalize()}": strawberry.mutation(resolver=delete_one),
            f"restore{name_prefix.capitalize()}": strawberry.mutation(resolver=restore_one)
        }


# ==================== SCHEMA PRINCIPAL MEJORADO ====================

def get_all_models():
    """Obtiene automáticamente TODOS los modelos de la metadata de SQLAlchemy"""
    models = []
    
    for mapper in Base.registry.mappers:
        model_class = mapper.class_
        
        if hasattr(model_class, '__tablename__') and model_class.__tablename__ is not None:
            models.append(model_class)
    
    return models

# Obtener automáticamente TODOS los modelos
MODELOS = get_all_models()

# Generar queries y mutations para todos los modelos
query_fields = {}
mutation_fields = {}

# Estadísticas para el reporte
model_stats = []

for modelo in MODELOS:
    try:
        crud = GenericCRUD(modelo)
        name = modelo.__name__.lower()
        
        # Generar queries
        queries = SchemaGenerator.generate_queries(crud, name)
        query_fields.update(queries)
        
        # Generar mutations
        mutations = SchemaGenerator.generate_mutations(crud, name)
        mutation_fields.update(mutations)
        
        # Recolectar estadísticas
        model_stats.append({
            'name': modelo.__name__,
            'table': modelo.__tablename__,
            'properties': len(crud.properties),
            'property_names': list(crud.properties.keys()),
            'queries': list(queries.keys()),
            'mutations': [m for m in mutations.keys() if m.startswith('create') or m.startswith('update') or m.startswith('delete') or m.startswith('restore')]
        })
        
    except Exception as e:
        print(f"❌ Error en {modelo.__name__}: {e}")

# Crear clases Query y Mutation
if query_fields:
    Query = type('Query', (), query_fields)
else:
    @strawberry.type
    class Query:
        _dummy: str = "Schema vacío"

if mutation_fields:
    Mutation = type('Mutation', (), mutation_fields)
else:
    @strawberry.type
    class Mutation:
        _dummy: str = "Sin mutaciones"

# Crear schema final
schema = strawberry.Schema(query=Query, mutation=Mutation)

# ==================== GENERAR REPORTE TIPO GRAPHQL AUTODOC ====================

print("\n" + "="*80)
print("🚀 GRAPHQL SCHEMA AUTO-GENERATED")
print("="*80)

print(f"\n📊 SCHEMA STATISTICS:")
print(f"   • Total Models: {len(MODELOS)}")
print(f"   • Total Queries: {len(query_fields)}")
print(f"   • Total Mutations: {len(mutation_fields)}")

print(f"\n🔧 AVAILABLE TYPES:")

for stat in model_stats:
    prop_info = f" [+{stat['properties']} computed]" if stat['properties'] > 0 else ""
    print(f"\n   📋 {stat['name']} (table: {stat['table']}){prop_info}")
    
    # Mostrar propiedades calculadas
    if stat['properties'] > 0:
        props_display = stat['property_names'][:3]  # Mostrar solo las primeras 3
        if len(stat['property_names']) > 3:
            props_display.append(f"...+{len(stat['property_names']) - 3} more")
        print(f"      Computed: {', '.join(props_display)}")

print(f"\n🔍 QUERY OPERATIONS:")

# Agrupar queries por tipo
query_groups = {}
for stat in model_stats:
    for query in stat['queries']:
        if query.endswith('sBorrados'):
            query_type = 'DELETED'
        elif query.endswith('sTodos'):
            query_type = 'ALL'
        elif query.endswith('s'):
            query_type = 'LIST'
        else:
            query_type = 'SINGLE'
        
        if query_type not in query_groups:
            query_groups[query_type] = []
        query_groups[query_type].append(query)

for qtype, queries in query_groups.items():
    print(f"\n   {qtype.title()} QUERIES:")
    for query in sorted(queries):
        model_name = query.replace('sBorrados', '').replace('sTodos', '').replace('s', '').title()
        print(f"      • {query}: [{model_name}]")

print(f"\n⚡ MUTATION OPERATIONS:")

# Agrupar mutaciones por tipo
mutation_groups = {'CREATE': [], 'UPDATE': [], 'DELETE': [], 'RESTORE': []}
for stat in model_stats:
    for mutation in stat['mutations']:
        if mutation.startswith('create'):
            mutation_groups['CREATE'].append(mutation)
        elif mutation.startswith('update'):
            mutation_groups['UPDATE'].append(mutation)
        elif mutation.startswith('delete'):
            mutation_groups['DELETE'].append(mutation)
        elif mutation.startswith('restore'):
            mutation_groups['RESTORE'].append(mutation)

for mtype, mutations in mutation_groups.items():
    if mutations:
        print(f"\n   {mtype.title()} MUTATIONS:")
        for mutation in sorted(mutations):
            model_name = mutation[6:]  # Remover create/update/delete/restore
            print(f"      • {mutation}: [{model_name}]")

print(f"\n🎯 QUERY EXAMPLES:")

# Ejemplos de consultas para modelos con propiedades interesantes
interesting_models = [m for m in model_stats if m['properties'] > 2]
for model in interesting_models[:3]:  # Mostrar solo 3 ejemplos
    model_name_lower = model['name'].lower()
    print(f"\n   # {model['name']} with computed properties")
    print(f"   query Get{model['name']}WithComputed {{")
    print(f"     {model_name_lower}s {{")
    print(f"       items {{")
    print(f"         id")
    print(f"         nombre")
    for prop in model['property_names'][:3]:  # Mostrar primeras 3 propiedades
        print(f"         {prop}")
    print(f"       }}")
    print(f"     }}")
    print(f"   }}")

print(f"\n🔗 FILTERING & PAGINATION:")
print(f"   • All list queries support: filters, orderBy, pagination")
print(f"   • Filter operators: eq, ne, gt, lt, like, ilike, in, not_in, is_null, between")
print(f"   • Pagination: page, page_size (default: 1, 20)")

print(f"\n" + "="*80)
print("✅ SCHEMA GENERATION COMPLETE")
print("="*80)