from __future__ import annotations
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base, UUIDPKMixin, AuditMixin

class FuenteHistoriografica(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "fuentes_historiograficas"
    titulo: Mapped[str]
    autor: Mapped[Optional[str]]
    editorial: Mapped[Optional[str]]
    año_publicacion: Mapped[Optional[int]]
    isbn: Mapped[Optional[str]]
    descripcion: Mapped[Optional[str]]

class CitaHistoriografica(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "citas_historiograficas"
    fuente_id: Mapped[str]
    inmueble_id: Mapped[str]
    paginas: Mapped[Optional[str]]
    texto_cita: Mapped[str]
    notas: Mapped[Optional[str]]
