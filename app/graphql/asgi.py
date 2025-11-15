# app/graphql/asgi.py
from strawberry.asgi import GraphQL
from .context import get_context
import traceback
import sys

try:
    from .schema import schema
except Exception as e:
    print(f"❌ Error cargando el schema GraphQL: {e}", file=sys.stderr)
    # Salir inmediatamente si el schema no se puede cargar
    sys.exit(1)

app = GraphQL(schema, context_getter=get_context)