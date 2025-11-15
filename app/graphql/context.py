# app/graphql/context.py
from app.db.session_async import get_db

async def get_context():
    """
    Contexto asíncrono para GraphQL
    """
    async for db_session in get_db():
        return {"db": db_session}

context_getter = get_context
