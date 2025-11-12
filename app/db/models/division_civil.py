from __future__ import annotations
from typing import List, Optional
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from .base import Base, UUIDPKMixin, AuditMixin

class ComunidadAutonoma(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "comunidades_autonomas"
    __table_args__ = (UniqueConstraint("nombre", name="uq_comunidad_nombre"),)
    nombre: Mapped[str]
    wikidata_qid: Mapped[Optional[str]] = mapped_column(nullable=True, unique=True)
    provincias: Mapped[List["Provincia"]] = relationship(back_populates="comunidad_autonoma")

class Provincia(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "provincias"
    __table_args__ = (UniqueConstraint("nombre", "comunidad_autonoma_id", name="uq_provincia_nombre_comunidad"),)
    nombre: Mapped[str]
    wikidata_qid: Mapped[Optional[str]] = mapped_column(nullable=True, unique=True)
    comunidad_autonoma_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("comunidades_autonomas.id"))
    comunidad_autonoma: Mapped["ComunidadAutonoma"] = relationship(back_populates="provincias")
    localidades: Mapped[List["Localidad"]] = relationship(back_populates="provincia")

class Localidad(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "localidades"
    __table_args__ = (UniqueConstraint("nombre", "provincia_id", name="uq_localidad_nombre_provincia"),)
    nombre: Mapped[str]
    wikidata_qid: Mapped[Optional[str]] = mapped_column(nullable=True, unique=True)
    provincia_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("provincias.id"))
    provincia: Mapped["Provincia"] = relationship(back_populates="localidades")
