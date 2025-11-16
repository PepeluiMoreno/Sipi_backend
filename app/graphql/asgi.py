# app/graphql/asgi.py
from strawberry.asgi import GraphQL
from .schema import schema

# Si todo es síncrono, mejor usar la versión síncrona
app = GraphQL(schema, debug=True)