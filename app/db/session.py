# session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configuración de la base de datos - actualiza con tu cadena de conexión
SQLALCHEMY_DATABASE_URL = "postgresql://usuario:password@localhost/nombre_bd"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()