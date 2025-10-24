from typing import Any, Dict
from fastapi import Request

async def get_context(request: Request) -> Dict[str, Any]:
    return { 'db': getattr(request.state, 'db', None), 'env': getattr(request.app.state, 'env', 'production') }
