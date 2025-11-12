# SIPI ·  Servicio de Información sobre el Patrimonio Inmatriculado por la Iglesia Católica en España
Generado: 2025-11-11 22:39:17 UTC

## Contenido
- Servidor **Strawberry GraphQL** en `app/graphql/asgi.py`.
- ETL con extract/transform/load y workflows n8n stub, con datos obtendidos de OSM y Wikidata
  

## Arranque
```bash
pip install -e .
cp .env.example .env
python -m app.graphql.asgi
# http://localhost:8040/graphql
```
