from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Boolean
from .base import Base, UUIDPKMixin, AuditMixin

class TipoInmueble(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "tipos_inmueble"
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

class EstadoConservacion(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "estados_conservacion"
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

class EstadoTratamiento(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "estados_tratamiento"
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

class TipoDocumento(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "tipos_documento"
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

class TipoMimeDocumento(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "tipos_mime_documento"
    tipo_mime: Mapped[str] = mapped_column(String(100), unique=True)
    extension: Mapped[str] = mapped_column(String(10))
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

class TipoAdquiriente(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "tipos_adquiriente"
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

class TipoTransmision(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "tipos_transmision"
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

class TipoCertificacionPropiedad(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "tipos_certificacion_propiedad"
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

class RolProfesional(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "roles_profesional"
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

class ColegioProfesional(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "colegios_profesionales"
    nombre: Mapped[str] = mapped_column(String(255), unique=True)
    codigo: Mapped[str | None] = mapped_column(String(50), nullable=True)
    direccion: Mapped[str | None] = mapped_column(Text, nullable=True)
    telefono: Mapped[str | None] = mapped_column(String(20), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

class Administracion(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "administraciones"
    nombre: Mapped[str] = mapped_column(String(255), unique=True)
    ambito: Mapped[str | None] = mapped_column(String(100), nullable=True)
