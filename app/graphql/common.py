
from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, List, Optional, Sequence, TypeVar

T = TypeVar("T")

@dataclass
class Page(Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int

def clamp_limit(limit: Optional[int], default: int = 50, max_limit: int = 200) -> int:
    if limit is None:
        return default
    return max(1, min(limit, max_limit))

def clamp_offset(offset: Optional[int]) -> int:
    return max(0, offset or 0)
