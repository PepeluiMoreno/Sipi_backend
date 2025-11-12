from strawberry.asgi import GraphQL
from .schema import schema

async def get_context():
    from app.db.session import SessionLocal
    return {"db": SessionLocal()}

app = GraphQL(schema, context_getter=get_context)
