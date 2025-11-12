
from __future__ import annotations
from typing import Any, Optional
from app.db.session import SessionLocal
from .dataloaders import build_dataloaders

class RequestContext:
    def __init__(self):
        self.db = SessionLocal()
        self.loaders = build_dataloaders(self.db)

    def close(self):
        self.db.close()

def get_context() -> RequestContext:
    return RequestContext()

# Starlette/ASGI hook if needed
async def context_getter():
    ctx = get_context()
    try:
        yield ctx
    finally:
        ctx.close()
