"""
Sistema genérico para generar automáticamente CRUD completo con Strawberry GraphQL
Soporta SQLAlchemy, filtros dinámicos, paginación y relaciones
"""
from typing import TypeVar, Generic, Type, Optional, List, Any, Dict, get_args, get_origin
from datetime import datetime, date
from decimal import Decimal
import strawberry
from strawberry.types import Info
from sqlalchemy import select, func, and_, or_, asc, desc
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.inspection import inspect
import enum
import uuid


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
class OrderDirection:
    ASC = "asc"
    DESC = "desc"


@strawberry.enum
class FilterOperator:
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


# ==================== GENERADOR DE TIPOS STRAWBERRY ====================

class StrawberryTypeGenerator:
    """Genera tipos Strawberry desde modelos SQLAlchemy"""
    
    _type_mapping = {
        int: strawberry.ID if lambda x: x.primary_key else int,
        str: strawberry.ID if lambda x: x.primary_key else str,
        float: float,
        bool: bool,
        datetime: datetime,
        date: date,
        Decimal: float,  # Decimal se mapea a float en GraphQL
        uuid.UUID: strawberry.ID,
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
        """Genera un tipo Strawberry desde un modelo SQLAlchemy"""
        if type_name is None:
            type_name = f"{model.__name__}Type"
        
        mapper = inspect(model)
        fields = {}
        
        for column in mapper.columns:
            col_name = column.name
            python_type = column.type.python_type
            strawberry_type = cls.python_type_to_strawberry(python_type, column)
            
            # Manejar nullable
            if column.nullable:
                fields[col_name] = Optional[strawberry_type]
            else:
                fields[col_name] = strawberry_type
        
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


# ==================== CRUD GENÉRICO ====================

class GenericCRUD(Generic[T]):
    """CRUD genérico para cualquier modelo SQLAlchemy"""
    
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
        pagination: Optional[PaginationInput] = None
    ) -> Dict[str, Any]:
        """Obtener todos con filtros, ordenamiento y paginación"""
        # Query base
        query = select(self.model)
        
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
        """Eliminar registro"""
        obj = await self.get_by_id(db, id)
        if not obj:
            return False
        
        await db.delete(obj)
        await db.commit()
        return True


# ==================== GENERADOR DE SCHEMA ====================

class SchemaGenerator:
    """Genera queries y mutaciones automáticamente"""
    
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
            if not obj:
                return None
            
            # Convertir a tipo Strawberry
            data = {}
            for column in inspect(crud.model).columns:
                col_name = column.name
                if hasattr(obj, col_name):
                    data[col_name] = getattr(obj, col_name)
            
            return crud.strawberry_type(**data)
        
        async def get_many(
            info: Info,
            filters: Optional[List[FilterCondition]] = None,
            order_by: Optional[List[OrderBy]] = None,
            pagination: Optional[PaginationInput] = None
        ) -> SpecificPaginatedResponse:
            db = info.context["db"]
            result = await crud.get_all(db, filters, order_by, pagination)
            
            # Convertir items a tipos Strawberry
            strawberry_items = []
            for item in result["items"]:
                data = {}
                for column in inspect(crud.model).columns:
                    col_name = column.name
                    if hasattr(item, col_name):
                        data[col_name] = getattr(item, col_name)
                strawberry_items.append(crud.strawberry_type(**data))
            
            return SpecificPaginatedResponse(
                items=strawberry_items,
                page_info=result["page_info"]
            )
        
        return {
            f"{name_prefix}": strawberry.field(resolver=get_one),
            f"{name_prefix}s": strawberry.field(resolver=get_many)
        }
    
    @staticmethod
    def generate_mutations(crud: GenericCRUD, name_prefix: str):
        """Genera mutaciones para un CRUD"""
        
        async def create_one(info: Info, data: crud.create_input) -> crud.strawberry_type:
            db = info.context["db"]
            data_dict = {k: v for k, v in data.__dict__.items() if v is not None}
            obj = await crud.create(db, data_dict)
            
            # Convertir a tipo Strawberry
            result_data = {}
            for column in inspect(crud.model).columns:
                col_name = column.name
                if hasattr(obj, col_name):
                    result_data[col_name] = getattr(obj, col_name)
            
            return crud.strawberry_type(**result_data)
        
        async def update_one(
            info: Info,
            id: strawberry.ID,
            data: crud.update_input
        ) -> Optional[crud.strawberry_type]:
            db = info.context["db"]
            data_dict = {k: v for k, v in data.__dict__.items() if v is not None}
            obj = await crud.update(db, id, data_dict)
            
            if not obj:
                return None
            
            # Convertir a tipo Strawberry
            result_data = {}
            for column in inspect(crud.model).columns:
                col_name = column.name
                if hasattr(obj, col_name):
                    result_data[col_name] = getattr(obj, col_name)
            
            return crud.strawberry_type(**result_data)
        
        async def delete_one(info: Info, id: strawberry.ID) -> bool:
            db = info.context["db"]
            return await crud.delete(db, id)
        
        return {
            f"create{name_prefix.capitalize()}": strawberry.mutation(resolver=create_one),
            f"update{name_prefix.capitalize()}": strawberry.mutation(resolver=update_one),
            f"delete{name_prefix.capitalize()}": strawberry.mutation(resolver=delete_one)
        }


# ==================== SCHEMA PRINCIPAL ====================

# Importar todos tus modelos
from app.db.models import (
    Usuario, Rol, Inmueble, Provincia, Localidad, ComunidadAutonoma,
    Diocesis, Actuacion, Tecnico, Transmision, FuenteHistoriografica,
    CitaHistoriografica, Documento, TipoInmueble, EstadoConservacion,
    Adquiriente, Transmitente, Notaria, RegistroPropiedad, AgenciaInmobiliaria
)

# Lista de todos los modelos para generar CRUDs
MODELOS = [
    Usuario, Rol, Inmueble, Provincia, Localidad, ComunidadAutonoma,
    Diocesis, Actuacion, Tecnico, Transmision, FuenteHistoriografica,
    CitaHistoriografica, Documento, TipoInmueble, EstadoConservacion,
    Adquiriente, Transmitente, Notaria, RegistroPropiedad, AgenciaInmobiliaria
]

# Generar queries y mutations para todos los modelos
query_fields = {}
mutation_fields = {}

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
        
        print(f"✅ Generado CRUD para {modelo.__name__}")
        
    except Exception as e:
        print(f"❌ Error generando CRUD para {modelo.__name__}: {e}")

# Crear clases Query y Mutation dinámicamente
Query = type('Query', (), query_fields)
Mutation = type('Mutation', (), mutation_fields)

# Crear schema final
schema = strawberry.Schema(query=Query, mutation=Mutation)

print("🚀 Schema GraphQL generado exitosamente!")