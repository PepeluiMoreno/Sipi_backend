# app/graphql/asgi.py
from strawberry.asgi import GraphQL
from .context import get_context
import traceback
import sys

try:
    from .schema import schema
    print("✅ Schema GraphQL genérico asíncrono cargado correctamente")
    
    # Debug: mostrar tipos disponibles
    print(f"✅ Tipos en el schema: {list(schema._schema.type_map.keys())[:10]}...")
    
except Exception as e:
    print(f"❌ Error cargando el schema GraphQL genérico: {e}", file=sys.stderr)
    traceback.print_exc()
    sys.exit(1)

app = GraphQL(
    schema, 
    context_getter=get_context,
    debug=True
)

print("🚀 Servidor GraphQL asíncrono iniciado correctamente")