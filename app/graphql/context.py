# app/graphql/context.py
from sqlalchemy.orm import Session
from app.db.session import SessionLocal  # O como tengas tu sesión síncrona

def get_context() -> dict:
    """Contexto síncrono para GraphQL"""
    return {
        "db": SessionLocal()
    }