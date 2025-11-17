# asgi.py
from strawberry.asgi import GraphQL
from .schema.schema_main import schema
from app.db.sessions.async_session import get_async_db

async def get_context(request):
    async for db in get_async_db():
        return {"db": db}

app = GraphQL(schema)
app.context_getter = get_context