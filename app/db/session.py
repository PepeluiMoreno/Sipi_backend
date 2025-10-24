from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.utils.config import DATABASE_URL_RUNTIME
if not DATABASE_URL_RUNTIME:
    raise RuntimeError('DATABASE_URL or DATABASE_URL_POOLER must be set.')
engine = create_engine(DATABASE_URL_RUNTIME, pool_pre_ping=True, pool_size=5, max_overflow=5, pool_recycle=1800, pool_timeout=30)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
