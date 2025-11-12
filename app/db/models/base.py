from __future__ import annotations
from typing import Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime, Boolean, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

class Base(DeclarativeBase):
    pass

class UUIDPKMixin:
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, server_default=text("gen_random_uuid()"))

class AuditMixin:
    creado_por: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=False), ForeignKey("usuarios.id"), nullable=True)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    editado_por: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=False), ForeignKey("usuarios.id"), nullable=True)
    fecha_edicion: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    eliminado: Mapped[bool] = mapped_column(Boolean, default=False)
    fecha_eliminacion: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    eliminado_por: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=False), ForeignKey("usuarios.id"), nullable=True)
