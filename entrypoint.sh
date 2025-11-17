#!/bin/sh
set -e

# Configurar puerto
GRAPHQL_PORT=${GRAPHQL_PORT:-8000}
echo "== Starting GraphQL on port: $GRAPHQL_PORT"

[ -d alembic/versions ] || mkdir -p alembic/versions
if ! ls -1 alembic/versions/*.py >/dev/null 2>&1; then
  echo "Autogenerating initial Alembic revision..."
  alembic revision --autogenerate -m "initial"
fi
alembic upgrade head

exec uvicorn app.graphql.asgi:app --host 0.0.0.0 --port $GRAPHQL_PORT
