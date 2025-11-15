# app/db/session_async.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
print(f"🔗 URL de BD original: {DATABASE_URL}")

# Convertir a asyncpg
ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql+psycopg2://", "postgresql+asyncpg://")
print(f"🔗 URL de BD asíncrona: {ASYNC_DATABASE_URL}")

# Crear motor asíncrono
engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,  # Muestra queries en consola (útil para desarrollo)
    future=True,
    pool_pre_ping=True,  # Verifica conexiones antes de usarlas
    pool_recycle=300,     # Recicla conexiones cada 5 minutos
)

# Session maker asíncrono
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

async def get_db():
    """
    Dependency para obtener sesión de base de datos asíncrona
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()  # Commit automático si no hay errores
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()