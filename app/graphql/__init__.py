# __init__.py
"""
Sistema automático de generación de GraphQL Schema
"""
from app.graphql.schema.schema_main import schema, Query, Mutation

__all__ = ['schema', 'Query', 'Mutation']