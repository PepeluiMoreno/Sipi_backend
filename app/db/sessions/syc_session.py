# Para ETL, scripts, migraciones
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL_SYNC", "postgresql://usuario:password@localhost/bd")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_sync_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()