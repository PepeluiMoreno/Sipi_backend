# schema_main.py
"""
Schema principal - Ensamblaje final del GraphQL Schema
"""
import strawberry

from .base_types import PageInfo, PaginatedResponse
from .type_generator import StrawberryTypeGenerator, PropertyDetector, PropertyResolver
from .query_builder import DynamicQueryBuilder
from .crud_generator import GenericCRUD
from .schema_generator import SchemaGenerator, get_all_models

# Obtener automáticamente TODOS los modelos
MODELOS = get_all_models()

# Generar queries y mutations para todos los modelos
query_fields = {}
mutation_fields = {}

# Estadísticas para el reporte
model_stats = []

for modelo in MODELOS:
    try:
        crud = GenericCRUD(modelo)
        name = modelo.__name__.lower()
        
        # Generar queries
        queries = SchemaGenerator.generate_queries(crud, name)
        query_fields.update(queries)
        
        # Generar mutations
        mutations = SchemaGenerator.generate_mutations(crud, name)
        mutation_fields.update(mutations)
        
        # Recolectar estadísticas
        model_stats.append({
            'name': modelo.__name__,
            'table': modelo.__tablename__,
            'properties': len(crud.properties),
            'property_names': list(crud.properties.keys()),
            'queries': list(queries.keys()),
            'mutations': [m for m in mutations.keys() if m.startswith('create') or m.startswith('update') or m.startswith('delete') or m.startswith('restore')]
        })
        
    except Exception as e:
        print(f"❌ Error en {modelo.__name__}: {e}")

# Crear clases Query y Mutation
if query_fields:
    Query = type('Query', (), query_fields)
else:
    @strawberry.type
    class Query:
        _dummy: str = "Schema vacío"

if mutation_fields:
    Mutation = type('Mutation', (), mutation_fields)
else:
    @strawberry.type
    class Mutation:
        _dummy: str = "Sin mutaciones"

# Crear schema final
schema = strawberry.Schema(query=Query, mutation=Mutation)

# ==================== GENERAR REPORTE TIPO GRAPHQL AUTODOC ====================

print("\n" + "="*80)
print("🚀 GRAPHQL SCHEMA AUTO-GENERATED")
print("="*80)

print(f"\n📊 SCHEMA STATISTICS:")
print(f"   • Total Models: {len(MODELOS)}")
print(f"   • Total Queries: {len(query_fields)}")
print(f"   • Total Mutations: {len(mutation_fields)}")

print(f"\n🔧 AVAILABLE TYPES:")

for stat in model_stats:
    prop_info = f" [+{stat['properties']} computed]" if stat['properties'] > 0 else ""
    print(f"\n   📋 {stat['name']} (table: {stat['table']}){prop_info}")
    
    # Mostrar propiedades calculadas
    if stat['properties'] > 0:
        props_display = stat['property_names'][:3]  # Mostrar solo las primeras 3
        if len(stat['property_names']) > 3:
            props_display.append(f"...+{len(stat['property_names']) - 3} more")
        print(f"      Computed: {', '.join(props_display)}")

print(f"\n🔍 QUERY OPERATIONS:")

# Agrupar queries por tipo
query_groups = {}
for stat in model_stats:
    for query in stat['queries']:
        if query.endswith('sBorrados'):
            query_type = 'DELETED'
        elif query.endswith('sTodos'):
            query_type = 'ALL'
        elif query.endswith('s'):
            query_type = 'LIST'
        else:
            query_type = 'SINGLE'
        
        if query_type not in query_groups:
            query_groups[query_type] = []
        query_groups[query_type].append(query)

for qtype, queries in query_groups.items():
    print(f"\n   {qtype.title()} QUERIES:")
    for query in sorted(queries):
        model_name = query.replace('sBorrados', '').replace('sTodos', '').replace('s', '').title()
        print(f"      • {query}: [{model_name}]")

print(f"\n⚡ MUTATION OPERATIONS:")

# Agrupar mutaciones por tipo
mutation_groups = {'CREATE': [], 'UPDATE': [], 'DELETE': [], 'RESTORE': []}
for stat in model_stats:
    for mutation in stat['mutations']:
        if mutation.startswith('create'):
            mutation_groups['CREATE'].append(mutation)
        elif mutation.startswith('update'):
            mutation_groups['UPDATE'].append(mutation)
        elif mutation.startswith('delete'):
            mutation_groups['DELETE'].append(mutation)
        elif mutation.startswith('restore'):
            mutation_groups['RESTORE'].append(mutation)

for mtype, mutations in mutation_groups.items():
    if mutations:
        print(f"\n   {mtype.title()} MUTATIONS:")
        for mutation in sorted(mutations):
            model_name = mutation[6:]  # Remover create/update/delete/restore
            print(f"      • {mutation}: [{model_name}]")

print(f"\n🎯 QUERY EXAMPLES:")

# Ejemplos de consultas para modelos con propiedades interesantes
interesting_models = [m for m in model_stats if m['properties'] > 2]
for model in interesting_models[:3]:  # Mostrar solo 3 ejemplos
    model_name_lower = model['name'].lower()
    print(f"\n   # {model['name']} with computed properties")
    print(f"   query Get{model['name']}WithComputed {{")
    print(f"     {model_name_lower}s {{")
    print(f"       items {{")
    print(f"         id")
    print(f"         nombre")
    for prop in model['property_names'][:3]:  # Mostrar primeras 3 propiedades
        print(f"         {prop}")
    print(f"       }}")
    print(f"     }}")
    print(f"   }}")

print(f"\n🔗 FILTERING & PAGINATION:")
print(f"   • All list queries support: filters, orderBy, pagination")
print(f"   • Filter operators: eq, ne, gt, lt, like, ilike, in, not_in, is_null, between")
print(f"   • Pagination: page, page_size (default: 1, 20)")

print(f"\n" + "="*80)
print("✅ SCHEMA GENERATION COMPLETE")
print("="*80)