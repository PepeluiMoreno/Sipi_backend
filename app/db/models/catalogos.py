from __future__ import annotations
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UniqueConstraint
from .base import Base, UUIDPKMixin, AuditMixin

class TipoInmueble(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "tipos_inmueble"
    __table_args__ = (UniqueConstraint("nombre", name="uq_tipo_inmueble_nombre"),)
    nombre: Mapped[str]
    descripcion: Mapped[Optional[str]]
    activo: Mapped[bool] = mapped_column(default=True)
    wikidata_qid: Mapped[Optional[str]] = mapped_column(nullable=True, unique=True)

class EstadoConservacion(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "estados_conservacion"
    __table_args__ = (UniqueConstraint("nombre", name="uq_estado_conservacion_nombre"),)
    nombre: Mapped[str]
    descripcion: Mapped[Optional[str]]
    activo: Mapped[bool] = mapped_column(default=True)

class EstadoTratamiento(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "estados_tratamiento"
    __table_args__ = (UniqueConstraint("nombre", name="uq_estado_tratamiento_nombre"),)
    nombre: Mapped[str]
    descripcion: Mapped[Optional[str]]
    activo: Mapped[bool] = mapped_column(default=True)

class TipoDocumento(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "tipos_documento"
    __table_args__ = (UniqueConstraint("nombre", name="uq_tipo_documento_nombre"),)
    nombre: Mapped[str]
    descripcion: Mapped[Optional[str]]
    activo: Mapped[bool] = mapped_column(default=True)

class TipoMimeDocumento(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "tipos_mime_documento"
    __table_args__ = (UniqueConstraint("tipo_mime", name="uq_tipo_mime"),)
    tipo_mime: Mapped[str]
    extension: Mapped[str]
    descripcion: Mapped[Optional[str]]
    activo: Mapped[bool] = mapped_column(default=True)

class TipoAdquiriente(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "tipos_adquiriente"
    __table_args__ = (UniqueConstraint("nombre", name="uq_tipo_adquiriente_nombre"),)
    nombre: Mapped[str]
    descripcion: Mapped[Optional[str]]
    activo: Mapped[bool] = mapped_column(default=True)

class TipoTransmision(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "tipos_transmision"
    __table_args__ = (UniqueConstraint("nombre", name="uq_tipo_transmision_nombre"),)
    nombre: Mapped[str]
    descripcion: Mapped[Optional[str]]
    activo: Mapped[bool] = mapped_column(default=True)

class TipoCertificacionPropiedad(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "tipos_certificacion_propiedad"
    __table_args__ = (UniqueConstraint("nombre", name="uq_tipo_certificacion_propiedad_nombre"),)
    nombre: Mapped[str]
    descripcion: Mapped[Optional[str]]
    activo: Mapped[bool] = mapped_column(default=True)

class RolProfesional(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "roles_profesional"
    __table_args__ = (UniqueConstraint("nombre", name="uq_rol_profesional_nombre"),)
    nombre: Mapped[str]
    descripcion: Mapped[Optional[str]]
    activo: Mapped[bool] = mapped_column(default=True)

class ColegioProfesional(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "colegios_profesionales"
    __table_args__ = (UniqueConstraint("nombre", name="uq_colegio_profesional_nombre"),)
    nombre: Mapped[str]
    codigo: Mapped[Optional[str]]
    direccion: Mapped[Optional[str]]
    telefono: Mapped[Optional[str]]
    email: Mapped[Optional[str]]
    activo: Mapped[bool] = mapped_column(default=True)
    wikidata_qid: Mapped[Optional[str]] = mapped_column(nullable=True, unique=True)

class Administracion(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "administraciones"
    __table_args__ = (UniqueConstraint("nombre", name="uq_administracion_nombre"),)
    nombre: Mapped[str]
    ambito: Mapped[Optional[str]]
    wikidata_qid: Mapped[Optional[str]] = mapped_column(nullable=True, unique=True)
