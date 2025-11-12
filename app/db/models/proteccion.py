from __future__ import annotations
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from .base import Base, UUIDPKMixin, AuditMixin

class FiguraProteccion(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "figuras_proteccion"
    __table_args__ = (
        UniqueConstraint("nombre", name="uq_figura_proteccion_nombre"),
        UniqueConstraint("nombre_normalizado", name="uq_figura_proteccion_normalizado"),
    )
    nombre: Mapped[str]
    nombre_normalizado: Mapped[str]
    descripcion: Mapped[Optional[str]]
    ambito: Mapped[Optional[str]]
    wikidata_qid: Mapped[Optional[str]] = mapped_column(nullable=True, unique=True)

class InmuebleFiguraProteccion(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "inmuebles_figuras_proteccion"
    inmueble_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("inmuebles.id"))
    figura_proteccion_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("figuras_proteccion.id"))
    administracion_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=False), ForeignKey("administraciones.id"), nullable=True)
    bic_id: Mapped[Optional[str]] = mapped_column(nullable=True)
    norma: Mapped[Optional[str]] = mapped_column(nullable=True)
    fecha_declaracion: Mapped[Optional[str]] = mapped_column(nullable=True)
