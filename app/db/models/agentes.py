from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Boolean, ForeignKey
from .base import Base, UUIDPKMixin, AuditMixin

class Profesional(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "profesionales"
    nombre: Mapped[str] = mapped_column(String(100))
    apellidos: Mapped[str] = mapped_column(String(200))
    identificacion: Mapped[str | None] = mapped_column(String(50), nullable=True)
    direccion: Mapped[str | None] = mapped_column(Text, nullable=True)
    telefono: Mapped[str | None] = mapped_column(String(20), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    rol_profesional_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("roles_profesional.id"))

class Colegiacion(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "colegiaciones"
    profesional_id: Mapped[str] = mapped_column(String(36), ForeignKey("profesionales.id"))
    colegio_profesional_id: Mapped[str] = mapped_column(String(36), ForeignKey("colegios_profesionales.id"))
    numero_colegiado: Mapped[str] = mapped_column(String(50))
    fecha_colegiacion: Mapped[str | None] = mapped_column(String(20), nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

class RegistroPropiedad(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "registros_propiedad"
    nombre: Mapped[str] = mapped_column(String(255))
    direccion: Mapped[str | None] = mapped_column(Text, nullable=True)
    telefono: Mapped[str | None] = mapped_column(String(20), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    profesional_registrador_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("profesionales.id"), nullable=True)

class Notaria(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "notarias"
    nombre: Mapped[str] = mapped_column(String(255))
    direccion: Mapped[str | None] = mapped_column(Text, nullable=True)
    telefono: Mapped[str | None] = mapped_column(String(20), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

class Notario(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "notarios"
    notaria_id: Mapped[str] = mapped_column(String(36), ForeignKey("notarias.id"))
    profesional_id: Mapped[str] = mapped_column(String(36), ForeignKey("profesionales.id"))
    fecha_inicio: Mapped[str | None] = mapped_column(String(20), nullable=True)
    fecha_fin: Mapped[str | None] = mapped_column(String(20), nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

class Adquiriente(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "adquirientes"
    nombre: Mapped[str] = mapped_column(String(255))
    tipo_adquiriente_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("tipos_adquiriente.id"))
    identificacion: Mapped[str | None] = mapped_column(String(50), nullable=True)
    direccion: Mapped[str | None] = mapped_column(Text, nullable=True)
    telefono: Mapped[str | None] = mapped_column(String(20), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
