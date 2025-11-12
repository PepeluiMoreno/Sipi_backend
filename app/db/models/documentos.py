from __future__ import annotations
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from .base import Base, UUIDPKMixin, AuditMixin

class Documento(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "documentos"
    url: Mapped[str]
    nombre_archivo: Mapped[Optional[str]] = mapped_column(nullable=True)
    tipo_mime: Mapped[Optional[str]] = mapped_column(nullable=True)
    tamano_bytes: Mapped[Optional[int]] = mapped_column(nullable=True)
    hash_sha256: Mapped[Optional[str]] = mapped_column(nullable=True)

class InmuebleDocumento(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "inmuebles_documentos"
    inmueble_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("inmuebles.id"))
    documento_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("documentos.id"))
    tipo_documento_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("tipos_documento.id"))
    descripcion: Mapped[Optional[str]] = mapped_column(nullable=True)
    fecha_documento: Mapped[Optional[str]] = mapped_column(nullable=True)

class ActuacionDocumento(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "actuaciones_documentos"
    actuacion_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("actuaciones.id"))
    documento_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("documentos.id"))
    tipo_documento_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("tipos_documento.id"))
    descripcion: Mapped[Optional[str]] = mapped_column(nullable=True)

class TransmisionDocumento(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "transmisiones_documentos"
    transmision_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("transmisiones.id"))
    documento_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("documentos.id"))
    tipo_documento_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("tipos_documento.id"))
    descripcion: Mapped[Optional[str]] = mapped_column(nullable=True)
