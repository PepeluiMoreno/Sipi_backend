from __future__ import annotations
from fastapi import FastAPI
from app.db.session import engine
from app.models.models import Base

app = FastAPI(title="Inmueble Backend")

@app.on_event("startup")
def on_startup():
    # For demo-only: create tables if not exist. Replace with Alembic in real deployments.
    Base.metadata.create_all(bind=engine)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}
