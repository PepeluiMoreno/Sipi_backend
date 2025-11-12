"""Habilita extensión pgcrypto para UUIDs y funciones criptográficas."""
from alembic import op

# Revisions
revision = "0001_create_pgcrypto"
down_revision = "0000_init_base"
branch_labels = None
depends_on = None

def upgrade() -> None:
    # pgcrypto para generar UUIDs seguros y cifrado opcional
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")

def downgrade() -> None:
    op.execute("DROP EXTENSION IF EXISTS pgcrypto;")
