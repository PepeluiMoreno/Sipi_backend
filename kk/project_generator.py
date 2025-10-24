#!/usr/bin/env python3
"""
Script para generar la estructura completa del proyecto de inmuebles religiosos.
Uso: python generate_project.py
"""

import os
from pathlib import Path

# Estructura de directorios
DIRECTORIES = [
    "app",
    "app/db",
    "app/models",
    "app/schemas",
    "app/repositories",
    "app/services",
    "app/graphql",
    "app/graphql/queries",
    "app/graphql/mutations",
    "app/etl",
    "app/etl/transformers",
    "app/etl/loaders",
    "app/etl/pipelines",
    "app/utils",
    "app/cli",
    "alembic",
    "alembic/versions",
    "tests",
    "tests/test_repositories",
    "tests/test_services",
    "tests/test_graphql",
    "tests/test_etl",
    "scripts",
    "data",
]

# Contenido de archivos
FILES = {
    # ============================================================================
    # ROOT FILES
    # ============================================================================
    ".env.example": """# Database
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/inmuebles_db

# API
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# OpenStreetMap Overpass API
OSM_OVERPASS_URL=https://overpass-api.de/api/interpreter
OSM_TIMEOUT=300
""",
    
    ".gitignore": """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment
.env
.venv

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# Database
*.db
*.sqlite

# Alembic
alembic/versions/*.pyc

# Data
data/*.csv
data/*.xlsx
!data/.gitkeep

# Logs
*.log
""",

    "requirements.txt": """# Core
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-dotenv==1.0.0

# Database
sqlalchemy==2.0.25
psycopg2-binary==2.9.9
geoalchemy2==0.14.3
alembic==1.13.1

# GraphQL
strawberry-graphql[fastapi]==0.219.0

# ETL & Data Processing
requests==2.31.0
pandas==2.2.0
overpy==0.7

# Utils
pydantic==2.5.3
pydantic-settings==2.1.0
python-multipart==0.0.6
""",

    "README.md": """# Sistema de Gestión de Inmuebles Religiosos

Sistema para el seguimiento y registro de transmisiones patrimoniales de inmuebles religiosos inmatriculados en España.

## Características

- GraphQL API con Strawberry
- Base de datos PostgreSQL con PostGIS
- ETL desde OpenStreetMap
- Gestión de transmisiones y actuaciones
- Búsquedas geoespaciales

## Instalación

1. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate   # Windows
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

4. Crear base de datos PostgreSQL con PostGIS:
```sql
CREATE DATABASE inmuebles_db;
\\c inmuebles_db
CREATE EXTENSION postgis;
```

5. Ejecutar migraciones:
```bash
alembic upgrade head
```

6. Seed de datos territoriales:
```bash
python scripts/seed_territorio.py
```

7. ETL de iglesias desde OSM (opcional):
```bash
python scripts/run_etl_osm.py
```

## Ejecución

```bash
uvicorn app.main:app --reload
```

GraphQL Playground: http://localhost:8000/graphql

## Estructura del Proyecto

Ver `docs/ARCHITECTURE.md` para detalles de la arquitectura.
""",

    "docker-compose.yml": """version: '3.8'

services:
  postgres:
    image: postgis/postgis:15-3.3
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: inmuebles_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
""",

    "alembic.ini": """[alembic]
script_location = alembic
prepend_sys_path = .
version_path_separator = os

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
""",

    # ============================================================================
    # APP ROOT
    # ============================================================================
    "app/__init__.py": "",

    "app/config.py": """from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql+psycopg2://user:password@localhost:5432/inmuebles_db"
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True
    
    # CORS
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # OpenStreetMap
    osm_overpass_url: str = "https://overpass-api.de/api/interpreter"
    osm_timeout: int = 300
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    return Settings()
""",

    "app/main.py": """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from app.config import get_settings
from app.graphql.schema import schema
from app.graphql.context import get_context

settings = get_settings()

app = FastAPI(
    title="Inmuebles Religiosos API",
    description="Sistema de gestión de transmisiones patrimoniales",
    version="1.0.0",
    debug=settings.debug
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GraphQL
graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context,
)

app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
async def root():
    return {
        "message": "Inmuebles Religiosos API",
        "graphql": "/graphql",
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}
""",

    # ============================================================================
    # DATABASE
    # ============================================================================
    "app/db/__init__.py": "",

    "app/db/base.py": """from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
""",

    "app/db/session.py": """from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import get_settings
from typing import Generator

settings = get_settings()

engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
""",

    "app/db/init_db.py": """from sqlalchemy import text
from app.db.session import engine
from app.db.base import Base
from app.models import models  # noqa: F401

def init_db():
    \"\"\"Inicializar base de datos\"\"\"
    # Crear extensión PostGIS
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
        conn.commit()
    
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    print("✓ Base de datos inicializada")

if __name__ == "__main__":
    init_db()
""",

    # ============================================================================
    # MODELS (actualizado con Municipio y códigos INE)
    # ============================================================================
    "app/models/__init__.py": "",

    "app/models/models.py": """from __future__ import annotations
from typing import Optional, List
from sqlalchemy import String, Integer, ForeignKey, Boolean, Date, Numeric, Text, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from geoalchemy2 import Geometry
from app.db.base import Base

# Territorio
class ComunidadAutonoma(Base):
    __tablename__ = "comunidad_autonoma"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    codigo_ine: Mapped[str] = mapped_column(String(2), unique=True, nullable=False, index=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    provincias: Mapped[List["Provincia"]] = relationship(back_populates="comunidad_autonoma", cascade="all, delete-orphan")

class Provincia(Base):
    __tablename__ = "provincia"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    codigo_ine: Mapped[str] = mapped_column(String(2), unique=True, nullable=False, index=True)
    nombre: Mapped[str] = mapped_column(String(100), index=True)
    comunidad_autonoma_id: Mapped[int] = mapped_column(ForeignKey("comunidad_autonoma.id"), index=True)
    comunidad_autonoma: Mapped["ComunidadAutonoma"] = relationship(back_populates="provincias")
    municipios: Mapped[List["Municipio"]] = relationship(back_populates="provincia", cascade="all, delete-orphan")
    inmuebles: Mapped[List["Inmueble"]] = relationship(back_populates="provincia")

class Municipio(Base):
    __tablename__ = "municipio"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    codigo_ine: Mapped[str] = mapped_column(String(5), unique=True, nullable=False, index=True)
    nombre: Mapped[str] = mapped_column(String(100), index=True)
    provincia_id: Mapped[int] = mapped_column(ForeignKey("provincia.id"), index=True)
    provincia: Mapped["Provincia"] = relationship(back_populates="municipios")
    inmuebles: Mapped[List["Inmueble"]] = relationship(back_populates="municipio")
    __table_args__ = (Index("ix_municipio_provincia_nombre", "provincia_id", "nombre"),)

class Diocesis(Base):
    __tablename__ = "diocesis"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    inmuebles: Mapped[List["Inmueble"]] = relationship(back_populates="diocesis")

# Catálogos
class RegistroPropiedad(Base):
    __tablename__ = "registro_propiedad"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    titular: Mapped[Optional[str]] = mapped_column(String(200))
    telefono: Mapped[Optional[str]] = mapped_column(String(50))
    correo_electronico: Mapped[Optional[str]] = mapped_column(String(255))
    inmuebles: Mapped[List["Inmueble"]] = relationship(back_populates="registro_propiedad")

class GradoProteccion(Base):
    __tablename__ = "grado_proteccion"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    inmuebles: Mapped[List["Inmueble"]] = relationship(back_populates="grado_proteccion")

class TipoAdquiriente(Base):
    __tablename__ = "tipo_adquiriente"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    adquirientes: Mapped[List["Adquiriente"]] = relationship(back_populates="tipo_adquiriente")

class TipoDocumento(Base):
    __tablename__ = "tipo_documento"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    denominacion: Mapped[str] = mapped_column(String(100), unique=True)
    documentos: Mapped[List["Documento"]] = relationship(back_populates="tipo")

class ColegioProfesional(Base):
    __tablename__ = "colegio_profesional"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    ambito: Mapped[Optional[str]] = mapped_column(String(50))
    comunidad_autonoma: Mapped[Optional[str]] = mapped_column(String(100))
    provincia: Mapped[Optional[str]] = mapped_column(String(100))
    url: Mapped[Optional[str]] = mapped_column(String(255))
    colegiados: Mapped[List["ProfesionalColegiacion"]] = relationship(back_populates="colegio")

class RolProfesional(Base):
    __tablename__ = "rol_profesional"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    participaciones: Mapped[List["ActuacionParticipacion"]] = relationship(back_populates="rol")

# Documentos
class Documento(Base):
    __tablename__ = "documento"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha: Mapped[Optional[Date]] = mapped_column(Date)
    tipo_id: Mapped[int] = mapped_column(ForeignKey("tipo_documento.id"), index=True)
    tipo: Mapped["TipoDocumento"] = relationship(back_populates="documentos")
    archivo: Mapped[Optional[str]] = mapped_column(String)
    url: Mapped[Optional[str]] = mapped_column(String)
    inmuebles_rel: Mapped[List["InmuebleDocumento"]] = relationship(back_populates="documento", cascade="all, delete-orphan")
    transmisiones_rel: Mapped[List["TransmisionDocumento"]] = relationship(back_populates="documento", cascade="all, delete-orphan")

# Inmueble
class Inmueble(Base):
    __tablename__ = "inmueble"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(200))
    comunidad_autonoma_id: Mapped[int] = mapped_column(ForeignKey("comunidad_autonoma.id"), index=True)
    provincia_id: Mapped[int] = mapped_column(ForeignKey("provincia.id"), index=True)
    municipio_id: Mapped[int] = mapped_column(ForeignKey("municipio.id"), index=True)
    diocesis_id: Mapped[Optional[int]] = mapped_column(ForeignKey("diocesis.id"))
    direccion: Mapped[Optional[str]] = mapped_column(String(200))
    coordenadas = mapped_column(Geometry(geometry_type="POINT", srid=4326, spatial_index=True))
    referencia_catastral: Mapped[Optional[str]] = mapped_column(String(20), unique=True)
    registro_propiedad_id: Mapped[Optional[int]] = mapped_column(ForeignKey("registro_propiedad.id"))
    numero_finca: Mapped[Optional[str]] = mapped_column(String(50))
    descripcion_registral: Mapped[Optional[str]] = mapped_column(Text)
    vendido: Mapped[bool] = mapped_column(Boolean, default=False)
    fecha_venta: Mapped[Optional[Date]] = mapped_column(Date)
    precio: Mapped[Optional[Numeric]] = mapped_column(Numeric(12, 2))
    ciudad_venta: Mapped[Optional[str]] = mapped_column(String(255))
    notario: Mapped[Optional[str]] = mapped_column(String(255))
    incluye_bienes_muebles: Mapped[bool] = mapped_column(Boolean, default=False)
    grado_proteccion_id: Mapped[Optional[int]] = mapped_column(ForeignKey("grado_proteccion.id"))
    tipo_adquiriente_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tipo_adquiriente.id"))
    observaciones: Mapped[Optional[str]] = mapped_column(Text)

    provincia: Mapped["Provincia"] = relationship(back_populates="inmuebles")
    comunidad_autonoma: Mapped["ComunidadAutonoma"] = relationship()
    municipio: Mapped["Municipio"] = relationship(back_populates="inmuebles")
    diocesis: Mapped[Optional["Diocesis"]] = relationship(back_populates="inmuebles")
    registro_propiedad: Mapped[Optional["RegistroPropiedad"]] = relationship(back_populates="inmuebles")
    grado_proteccion: Mapped[Optional["GradoProteccion"]] = relationship(back_populates="inmuebles")
    tipo_adquiriente: Mapped[Optional["TipoAdquiriente"]] = relationship(back_populates="adquirientes")

    documentos_rel: Mapped[List["InmuebleDocumento"]] = relationship(back_populates="inmueble", cascade="all, delete-orphan")
    transmisiones: Mapped[List["Transmision"]] = relationship(back_populates="inmueble", cascade="all, delete-orphan")
    actuaciones: Mapped[List["Actuacion"]] = relationship(back_populates="inmueble", cascade="all, delete-orphan")
    referencias_bibliograficas: Mapped[List["ReferenciaBibliografica"]] = relationship(back_populates="inmueble", cascade="all, delete-orphan")

    __table_args__ = (Index("ix_inmueble_prov_mun", "provincia_id", "municipio_id"),)

class InmuebleDocumento(Base):
    __tablename__ = "inmueble_documento"
    inmueble_id: Mapped[int] = mapped_column(ForeignKey("inmueble.id"), primary_key=True)
    documento_id: Mapped[int] = mapped_column(ForeignKey("documento.id"), primary_key=True)
    inmueble: Mapped["Inmueble"] = relationship(back_populates="documentos_rel")
    documento: Mapped["Documento"] = relationship(back_populates="inmuebles_rel")

# Transmisión y Adquiriente
class Adquiriente(Base):
    __tablename__ = "adquiriente"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(255), index=True)
    tipo_adquiriente_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tipo_adquiriente.id"))
    nif_cif: Mapped[Optional[str]] = mapped_column(String(32))
    representante: Mapped[Optional[str]] = mapped_column(String(255))
    email: Mapped[Optional[str]] = mapped_column(String(255))
    telefono: Mapped[Optional[str]] = mapped_column(String(50))
    direccion: Mapped[Optional[str]] = mapped_column(String(255))
    tipo_adquiriente: Mapped[Optional["TipoAdquiriente"]] = relationship(back_populates="adquirientes")
    transmisiones: Mapped[List["Transmision"]] = relationship(back_populates="adquiriente")

class Transmision(Base):
    __tablename__ = "transmision"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    inmueble_id: Mapped[int] = mapped_column(ForeignKey("inmueble.id"), index=True)
    tipo: Mapped[str] = mapped_column(String(20))
    fecha: Mapped[Optional[Date]] = mapped_column(Date)
    ciudad: Mapped[Optional[str]] = mapped_column(String(255))
    notario: Mapped[Optional[str]] = mapped_column(String(255))
    precio: Mapped[Optional[Numeric]] = mapped_column(Numeric(12, 2))
    adquiriente_id: Mapped[int] = mapped_column(ForeignKey("adquiriente.id"), index=True)
    observaciones: Mapped[Optional[str]] = mapped_column(Text)
    inmueble: Mapped["Inmueble"] = relationship(back_populates="transmisiones")
    adquiriente: Mapped["Adquiriente"] = relationship(back_populates="transmisiones")
    documentos_rel: Mapped[List["TransmisionDocumento"]] = relationship(back_populates="transmision", cascade="all, delete-orphan")
    __table_args__ = (Index("ix_transmision_tipo_fecha", "tipo", "fecha"),)

class TransmisionDocumento(Base):
    __tablename__ = "transmision_documento"
    transmision_id: Mapped[int] = mapped_column(ForeignKey("transmision.id"), primary_key=True)
    documento_id: Mapped[int] = mapped_column(ForeignKey("documento.id"), primary_key=True)
    transmision: Mapped["Transmision"] = relationship(back_populates="documentos_rel")
    documento: Mapped["Documento"] = relationship(back_populates="transmisiones_rel")

# Actuaciones
class Actuacion(Base):
    __tablename__ = "actuacion"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    inmueble_id: Mapped[int] = mapped_column(ForeignKey("inmueble.id"), index=True)
    tipo: Mapped[str] = mapped_column(String(30))
    titulo: Mapped[Optional[str]] = mapped_column(String(255))
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    organismo_responsable: Mapped[Optional[str]] = mapped_column(String(255))
    fecha_inicio: Mapped[Optional[Date]] = mapped_column(Date)
    fecha_fin: Mapped[Optional[Date]] = mapped_column(Date)
    importe_total: Mapped[Optional[Numeric]] = mapped_column(Numeric(12, 2))
    inmueble: Mapped["Inmueble"] = relationship(back_populates="actuaciones")
    fotos_antes_rel: Mapped[List["ActuacionFotoAntes"]] = relationship(back_populates="actuacion", cascade="all, delete-orphan")
    fotos_despues_rel: Mapped[List["ActuacionFotoDespues"]] = relationship(back_populates="actuacion", cascade="all, delete-orphan")
    participaciones: Mapped[List["ActuacionParticipacion"]] = relationship(back_populates="actuacion", cascade="all, delete-orphan")

class ActuacionFotoAntes(Base):
    __tablename__ = "actuacion_foto_antes"
    actuacion_id: Mapped[int] = mapped_column(ForeignKey("actuacion.id"), primary_key=True)
    documento_id: Mapped[int] = mapped_column(ForeignKey("documento.id"), primary_key=True)
    actuacion: Mapped["Actuacion"] = relationship(back_populates="fotos_antes_rel")
    documento: Mapped["Documento"] = relationship()

class ActuacionFotoDespues(Base):
    __tablename__ = "actuacion_foto_despues"
    actuacion_id: Mapped[int] = mapped_column(ForeignKey("actuacion.id"), primary_key=True)
    documento_id: Mapped[int] = mapped_column(ForeignKey("documento.id"), primary_key=True)
    actuacion: Mapped["Actuacion"] = relationship(back_populates="fotos_despues_rel")
    documento: Mapped["Documento"] = relationship()

# Profesionales
class Profesional(Base):
    __tablename__ = "profesional"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(255), index=True)
    telefono: Mapped[Optional[str]] = mapped_column(String(50))
    correo_electronico: Mapped[Optional[str]] = mapped_column(String(255))
    direccion_profesional: Mapped[Optional[str]] = mapped_column(String(255))
    colegiaciones: Mapped[List["ProfesionalColegiacion"]] = relationship(back_populates="profesional", cascade="all, delete-orphan")
    participaciones: Mapped[List["ActuacionParticipacion"]] = relationship(back_populates="profesional", cascade="all, delete-orphan")

class ProfesionalColegiacion(Base):
    __tablename__ = "profesional_colegiacion"
    profesional_id: Mapped[int] = mapped_column(ForeignKey("profesional.id"), primary_key=True)
    colegio_id: Mapped[int] = mapped_column(ForeignKey("colegio_profesional.id"), primary_key=True)
    numero_colegiado: Mapped[Optional[str]] = mapped_column(String(100))
    profesional: Mapped["Profesional"] = relationship(back_populates="colegiaciones")
    colegio: Mapped["ColegioProfesional"] = relationship(back_populates="colegiados")

class ActuacionParticipacion(Base):
    __tablename__ = "actuacion_participacion"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    actuacion_id: Mapped[int] = mapped_column(ForeignKey("actuacion.id"), index=True)
    profesional_id: Mapped[int] = mapped_column(ForeignKey("profesional.id"), index=True)
    rol_id: Mapped[int] = mapped_column(ForeignKey("rol_profesional.id"), index=True)
    colegio_nombre: Mapped[Optional[str]] = mapped_column(String(255))
    numero_colegiado: Mapped[Optional[str]] = mapped_column(String(100))
    fecha_inicio: Mapped[Optional[Date]] = mapped_column(Date)
    fecha_fin: Mapped[Optional[Date]] = mapped_column(Date)
    observaciones: Mapped[Optional[str]] = mapped_column(Text)
    actuacion: Mapped["Actuacion"] = relationship(back_populates="participaciones")
    profesional: Mapped["Profesional"] = relationship(back_populates="participaciones")
    rol: Mapped["RolProfesional"] = relationship(back_populates="participaciones")
    __table_args__ = (UniqueConstraint("actuacion_id", "profesional_id", "rol_id", name="uq_participacion_act_prof_rol"),)

# Bibliografía
class Bibliografia(Base):
    __tablename__ = "bibliografia"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    titulo: Mapped[str] = mapped_column(String(300))
    autores: Mapped[str] = mapped_column(Text)
    tipo_identificador: Mapped[str] = mapped_column(String(10))
    identificador: Mapped[str] = mapped_column(String(100), unique=True)
    url: Mapped[Optional[str]] = mapped_column(String(255))
    referencias: Mapped[List["ReferenciaBibliografica"]] = relationship(back_populates="bibliografia", cascade="all, delete-orphan")
    __table_args__ = (Index("ix_biblio_identificador", "tipo_identificador", "identificador"),)

class ReferenciaBibliografica(Base):
    __tablename__ = "referencia_bibliografica"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    inmueble_id: Mapped[int] = mapped_column(ForeignKey("inmueble.id"), index=True)
    bibliografia_id: Mapped[int] = mapped_column(ForeignKey("bibliografia.id"), index=True)
    volumen: Mapped[Optional[str]] = mapped_column(String(50))
    paginas: Mapped[Optional[str]] = mapped_column(String(50))
    inmueble: Mapped["Inmueble"] = relationship(back_populates="referencias_bibliograficas")
    bibliografia: Mapped["Bibliografia"] = relationship(back_populates="referencias")
    __table_args__ = (UniqueConstraint("inmueble_id", "bibliografia_id", "volumen", "paginas", name="uq_ref_biblio"),)
""",

    # ============================================================================
    # GRAPHQL BASE
    # ============================================================================
    "app/graph