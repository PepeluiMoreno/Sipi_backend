# app/graphql/context.py

from app.db.session import SessionLocal
from .dataloaders import build_dataloaders

from app.db.session import SessionLocal

async def get_context():
    db = SessionLocal()
    try:
        return {"db": db}
    except Exception:
        db.close()
        raise

context_getter = get_context


