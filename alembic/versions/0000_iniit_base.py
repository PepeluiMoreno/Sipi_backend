"""Inicializa base de datos: crea esquema y tablas audit básicas."""
from alembic import op
import sqlalchemy as sa

# Revisions
revision = "0000_init_base"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Crea extensión UUID si no existe
    op.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")

    # Ejemplo de tabla de auditoría global si no existe
    op.execute("""
    CREATE TABLE IF NOT EXISTS audit_log (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        tabla TEXT NOT NULL,
        operacion TEXT NOT NULL,
        usuario TEXT,
        fecha TIMESTAMP WITHOUT TIME ZONE DEFAULT now(),
        datos JSONB
    );
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS audit_log;")
    op.execute("DROP EXTENSION IF EXISTS \"uuid-ossp\";")
