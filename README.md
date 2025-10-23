# Sipi Backend (SQLAlchemy + FastAPI)

Minimal skeleton to run on a free-tier with Docker + PostGIS.

## Quickstart
1) Create `.env` from `.env.example` and set values.
2) `docker compose up -d --build`
3) Visit `http://localhost:8000/healthz`

> Only core pieces included. Alembic/GraphQL/ETL can be added later.
