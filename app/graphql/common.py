import strawberry
from typing import Optional

@strawberry.type
class Error:
    code: str
    message: str
    field: Optional[str] = None

@strawberry.type
class PageInfo:
    total: int
    limit: int
    offset: int
    has_next_page: bool

def page_info(total: int, limit: int, offset: int) -> PageInfo:
    has_next = offset + limit < total
    return PageInfo(total=total, limit=limit, offset=offset, has_next_page=has_next)
