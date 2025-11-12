from __future__ import annotations
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from .base import Base, UUIDPKMixin, AuditMixin

class Profesional(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "profesionales"
    nombre: Mapped[str]
    apellidos: Mapped[str]
    identificacion: Mapped[Optional[str]]
    direccion: Mapped[Optional[str]]
    telefono: Mapped[Optional[str]]
    email: Mapped[Optional[str]]
    activo: Mapped[bool] = mapped_column(default=True)
    rol_profesional_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("roles_profesional.id"))

class Colegiacion(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "colegiaciones"
    profesional_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("profesionales.id"))
    colegio_profesional_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("colegios_profesionales.id"))
    numero_colegiado: Mapped[str]
    fecha_colegiacion: Mapped[Optional[str]]
    activo: Mapped[bool] = mapped_column(default=True)

class RegistroPropiedad(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "registros_propiedad"
    nombre: Mapped[str]
    direccion: Mapped[Optional[str]]
    telefono: Mapped[Optional[str]]
    email: Mapped[Optional[str]]
    activo: Mapped[bool] = mapped_column(default=True)
    profesional_registrador_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=False), ForeignKey("profesionales.id"), nullable=True)

class Notaria(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "notarias"
    nombre: Mapped[str]
    direccion: Mapped[Optional[str]]
    telefono: Mapped[Optional[str]]
    email: Mapped[Optional[str]]
    activo: Mapped[bool] = mapped_column(default=True)

class Notario(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "notarios"
    notaria_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("notarias.id"))
    profesional_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("profesionales.id"))
    fecha_inicio: Mapped[Optional[str]]
    fecha_fin: Mapped[Optional[str]]
    activo: Mapped[bool] = mapped_column(default=True)

class Adquiriente(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "adquirientes"
    nombre: Mapped[str]
    tipo_adquiriente_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("tipos_adquiriente.id"))
    identificacion: Mapped[Optional[str]]
    direccion: Mapped[Optional[str]]
    telefono: Mapped[Optional[str]]
    email: Mapped[Optional[str]]
