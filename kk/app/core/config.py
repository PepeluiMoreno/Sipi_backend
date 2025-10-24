from __future__ import annotations
import os

class Settings:
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "dev")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@db:5432/sipi_db")

settings = Settings()
