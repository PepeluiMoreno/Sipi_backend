import os
import sys
from logging.config import fileConfig

from alembic import context

# Hacer que el proyecto sea importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Importación crítica - si falla, mostrar error real y salir
try:
    from app.db.session import engine
    from app.db.models.base import Base 
    target_metadata = Base.metadata
except Exception as e:
    print(f"❌ ERROR importando modelos SQLAlchemy: {e}")
    print("💡 Revise la sintaxis de los modelos (back_populates, relaciones, etc.)")
    sys.exit(1)

def run_migrations_offline():
    raise RuntimeError("Offline migrations not supported")

def run_migrations_online():
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()