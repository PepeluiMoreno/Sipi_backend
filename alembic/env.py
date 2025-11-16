import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine

# Hacer que el proyecto sea importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Obtener la URL de la base de datos
database_url = os.getenv("DATABASE_URL")
if not database_url:
    database_url = config.get_main_option("sqlalchemy.url")
    if not database_url:
        raise Exception("❌ No se encontró DATABASE_URL")

# ✅ Crear engine directamente aquí
engine = create_engine(database_url)

# Importar solo lo necesario
try:
    from app.db.base import Base 
    target_metadata = Base.metadata
except Exception as e:
    print(f"❌ ERROR importando modelos: {e}")
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