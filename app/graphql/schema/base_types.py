# base_types.py
"""
Tipos base y utilidades comunes para GraphQL
"""
from typing import List, Optional, Callable, Any
from enum import Enum
from functools import wraps


class FilterOperator(str, Enum):
    eq = "eq"
    ne = "ne"
    gt = "gt"
    gte = "gte"
    lt = "lt"
    lte = "lte"
    like = "like"
    ilike = "ilike"
    in_ = "in"
    not_in = "not_in"
    is_null = "is_null"
    between = "between"


class FilterCondition:
    field: str
    operator: FilterOperator
    value: Any = None
    values: Optional[List[Any]] = None

    def __init__(self, field: str, operator: FilterOperator, value: Any = None, values: Optional[List[Any]] = None):
        self.field = field
        self.operator = operator
        self.value = value
        self.values = values


class OrderDirection(str, Enum):
    asc = "asc"
    desc = "desc"


class OrderBy:
    field: str
    direction: OrderDirection

    def __init__(self, field: str, direction: OrderDirection = OrderDirection.asc):
        self.field = field
        self.direction = direction


class PaginationInput:
    page: int
    page_size: int

    def __init__(self, page: int = 1, page_size: int = 20):
        self.page = max(1, page)
        self.page_size = clamp_limit(page_size, 20, 100)


class PageInfo:
    page: int
    page_size: int
    total: int
    total_pages: int

    def __init__(self, page: int, page_size: int, total: int):
        self.page = page
        self.page_size = page_size
        self.total = total
        self.total_pages = (total + page_size - 1) // page_size


def clamp_limit(value: int, min_value: int, max_value: int) -> int:
    return max(min_value, min(max_value, value))


def suppress_traceback_continue(func: Callable):
    """Decorador para que los errores en resolvers no rompan todo el schema"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            print(f"[Resolver Error] {e}")
            return None
    return wrapper

