from __future__ import annotations
from typing import Optional, Dict, Any
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from .base import Base, UUIDPKMixin, AuditMixin

class InmuebleOSMExt(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "inmuebles_osm_ext"
    inmueble_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("inmuebles.id"), unique=True, nullable=True)
    osm_id: Mapped[Optional[int]]
    osm_tipo: Mapped[Optional[str]]
    tags: Mapped[Optional[dict]]
    source_url: Mapped[Optional[str]]
    etag: Mapped[Optional[str]]
    hash_contenido: Mapped[Optional[str]]
    fecha_extraccion: Mapped[Optional[str]]
    fecha_fuente: Mapped[Optional[str]]

class InmuebleWDExt(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "inmuebles_wd_ext"
    inmueble_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("inmuebles.id"), unique=True, nullable=True)
    wikidata_qid: Mapped[Optional[str]]
    label_es: Mapped[Optional[str]]
    descripcion_es: Mapped[Optional[str]]
    claims: Mapped[Optional[dict]]
    image_url: Mapped[Optional[str]]
    inception: Mapped[Optional[str]]
    source_url: Mapped[Optional[str]]
    etag: Mapped[Optional[str]]
    hash_contenido: Mapped[Optional[str]]
    fecha_extraccion: Mapped[Optional[str]]
    fecha_fuente: Mapped[Optional[str]]
