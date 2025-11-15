# base.py
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, DateTime, Boolean
from datetime import datetime
import uuid

class Base(DeclarativeBase):
    pass

class UUIDPKMixin:
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

class AuditMixin:
    creado_por: Mapped[str | None] = mapped_column(String(36), nullable=True)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    editado_por: Mapped[str | None] = mapped_column(String(36), nullable=True)
    fecha_edicion: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    eliminado: Mapped[bool] = mapped_column(Boolean, default=False)
    fecha_eliminacion: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    eliminado_por: Mapped[str | None] = mapped_column(String(36), nullable=True)