from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Integer, DateTime, ForeignKey
from .base import Base, UUIDPKMixin, AuditMixin

class Documento(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "documentos"
    url: Mapped[str] = mapped_column(Text)
    nombre_archivo: Mapped[str | None] = mapped_column(String(255), nullable=True)
    tipo_mime: Mapped[str | None] = mapped_column(String(100), nullable=True)
    tamano_bytes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    hash_sha256: Mapped[str | None] = mapped_column(String(64), nullable=True)

class InmuebleDocumento(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "inmuebles_documentos"
    inmueble_id: Mapped[str] = mapped_column(String(36), ForeignKey("inmuebles.id"))
    documento_id: Mapped[str] = mapped_column(String(36), ForeignKey("documentos.id"))
    tipo_documento_id: Mapped[str] = mapped_column(String(36), ForeignKey("tipos_documento.id"))
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    fecha_documento: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)

class ActuacionDocumento(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "actuaciones_documentos"
    actuacion_id: Mapped[str] = mapped_column(String(36), ForeignKey("actuaciones.id"))
    documento_id: Mapped[str] = mapped_column(String(36), ForeignKey("documentos.id"))
    tipo_documento_id: Mapped[str] = mapped_column(String(36), ForeignKey("tipos_documento.id"))
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)

class TransmisionDocumento(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "transmisiones_documentos"
    transmision_id: Mapped[str] = mapped_column(String(36), ForeignKey("transmisiones.id"))
    documento_id: Mapped[str] = mapped_column(String(36), ForeignKey("documentos.id"))
    tipo_documento_id: Mapped[str] = mapped_column(String(36), ForeignKey("tipos_documento.id"))
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
