#!/bin/sh
set -e

# 1) Asegura la revision 0001 (pgcrypto)
if [ ! -f "alembic/versions/0001_create_pgcrypto.py" ]; then
  cat > alembic/versions/0001_create_pgcrypto.py <<'PY'
"""create pgcrypto extension

Revision ID: 0001_create_pgcrypto
Revises: 
Create Date: 2025-11-12 00:00:00
"""
from alembic import op
revision = "0001_create_pgcrypto"
down_revision = None
branch_labels = None
depends_on = None
def upgrade(): op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")
def downgrade(): op.execute("DROP EXTENSION IF EXISTS pgcrypto;")
PY
fi

# 2) Sube a 0001
alembic upgrade 0001_create_pgcrypto || true

# 3) Autogenera la init si no existe ninguna otra revision
if [ -z "$(ls -1 alembic/versions | grep -v 0001_create_pgcrypto.py || true)" ]; then
  alembic revision --autogenerate -m "init models" || true
fi

# 4) Sube a head
alembic upgrade head || true

# 5) Arranca GraphQL
exec python -m app.graphql.asgi

