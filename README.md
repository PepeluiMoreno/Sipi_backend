# SIPI · Bundle GraphQL + ETL
Generado: 2025-11-11 22:39:17 UTC

- Sin REST. Servidor **Strawberry GraphQL** en `app/graphql/asgi.py`.
- Modelos SQLAlchemy completos con UUID y `AuditMixin`.
- ETL con extract/transform/load y workflows n8n stub.

## Arranque
```bash
pip install -e .
cp .env.example .env
python -m app.graphql.asgi
# http://localhost:8040/graphql
```
