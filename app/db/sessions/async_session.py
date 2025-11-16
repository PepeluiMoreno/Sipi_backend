# Para GraphQL API
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL_ASYNC", "postgresql+asyncpg://usuario:password@localhost/bd")

engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()