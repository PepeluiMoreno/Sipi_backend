# base_types.py
"""
Tipos base, enums, inputs y utilidades para el schema GraphQL
"""
from typing import List, Optional
import strawberry
import enum
import sys
from functools import wraps

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

@strawberry.type
class PaginatedResponse:
    """Respuesta paginada genérica"""
    items: List[str]  # Usar str en lugar de strawberry.scalars.JSON
    page_info: PageInfo

# ==================== ENUMS GENÉRICOS ====================

@strawberry.enum
class OrderDirection(enum.Enum):
    ASC = "asc"
    DESC = "desc"

@strawberry.enum
class FilterOperator(enum.Enum):
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
    value: Optional[str] = None  # Usar str en lugar de strawberry.scalars.JSON
    values: Optional[List[str]] = None  # Usar str en lugar de strawberry.scalars.JSON

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

# ==================== UTILIDADES ====================

def clamp_limit(limit: Optional[int], default: int = 50, max_limit: int = 200) -> int:
    """Limita el valor de límite entre 1 y max_limit"""
    if limit is None:
        return default
    return max(1, min(limit, max_limit))

def clamp_offset(offset: Optional[int]) -> int:
    """Asegura que el offset no sea negativo"""
    return max(0, offset or 0)

def suppress_traceback_continue(func):
    """Decorador para suprimir tracebacks pero continuar la ejecución"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_type = type(e).__name__
            print(f"⚠️  {error_type} en {func.__name__}: {str(e)}", file=sys.stderr)
            return None
    return wrapper