"""enable pg_trgm and helpful indexes

Revision ID: 0002_pgtrgm_indexes
Revises: 0001_create_pgcrypto
Create Date: 2025-11-12 01:00:00
"""
from alembic import op

revision = "0002_pgtrgm_indexes"
down_revision = "0001_create_pgcrypto"
branch_labels = None
depends_on = None

def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
    op.execute("CREATE INDEX IF NOT EXISTS ix_inmuebles_nombre_trgm ON inmuebles USING gin (nombre gin_trgm_ops);")
    op.execute("CREATE INDEX IF NOT EXISTS ix_inmuebles_direccion_trgm ON inmuebles USING gin (direccion gin_trgm_ops);")
    op.execute("CREATE INDEX IF NOT EXISTS ix_inmuebles_provincia ON inmuebles (provincia_id);")
    op.execute("CREATE INDEX IF NOT EXISTS ix_inmuebles_localidad ON inmuebles (localidad_id);")
    op.execute("CREATE INDEX IF NOT EXISTS ix_inmuebles_diocesis ON inmuebles (diocesis_id);")
    op.execute("CREATE INDEX IF NOT EXISTS ix_inmuebles_flags ON inmuebles (es_bic, es_ruina, esta_inmatriculado);")

def downgrade():
    op.execute("DROP INDEX IF EXISTS ix_inmuebles_flags;")
    op.execute("DROP INDEX IF EXISTS ix_inmuebles_diocesis;")
    op.execute("DROP INDEX IF EXISTS ix_inmuebles_localidad;")
    op.execute("DROP INDEX IF EXISTS ix_inmuebles_provincia;")
    op.execute("DROP INDEX IF EXISTS ix_inmuebles_direccion_trgm;")
    op.execute("DROP INDEX IF EXISTS ix_inmuebles_nombre_trgm;")
