from __future__ import annotations
from typing import Optional, List
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from .base import Base, UUIDPKMixin, AuditMixin

class Diocesis(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "diocesis"
    __table_args__ = (UniqueConstraint("nombre", name="uq_diocesis_nombre"),)
    nombre: Mapped[str]
    wikidata_qid: Mapped[Optional[str]] = mapped_column(nullable=True, unique=True)
    titulares: Mapped[List["DiocesisTitular"]] = relationship(back_populates="diocesis")

class DiocesisTitular(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "diocesis_titulares"
    diocesis_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("diocesis.id"))
    profesional_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("profesionales.id"))
    fecha_inicio: Mapped[Optional[str]]
    fecha_fin: Mapped[Optional[str]]
    observaciones: Mapped[Optional[str]]
    diocesis: Mapped["Diocesis"] = relationship(back_populates="titulares")
