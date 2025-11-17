# models/catalogos.py
from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text
from app.db.base import Base
from app.db.mixins import UUIDPKMixin, AuditMixin

if TYPE_CHECKING:
    from .inmuebles import Inmueble
    from .agentes import Tecnico, Adquiriente, Transmitente
    from .transmisiones import Transmision, Inmatriculacion
    from .actuaciones import ActuacionTecnicos
    from .documentos import InmuebleDocumento, ActuacionDocumento, TransmisionDocumento

class EstadoConservacion(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "estados_conservacion"
    
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Relaciones
    inmuebles: Mapped[list["Inmueble"]] = relationship("Inmueble", back_populates="estado_conservacion")

class EstadoTratamiento(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "estados_tratamiento"
    
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Relaciones
    inmuebles: Mapped[list["Inmueble"]] = relationship("Inmueble", back_populates="estado_tratamiento")

class FigurasProteccion(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "figuras_proteccion"
    
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)

class RolTecnico(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "roles_tecnico"
    
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Relaciones
    tecnicos: Mapped[list["Tecnico"]] = relationship("Tecnico", back_populates="rol_tecnico")
    actuaciones_tecnicos: Mapped[list["ActuacionTecnicos"]] = relationship("ActuacionTecnicos", back_populates="rol_tecnico")

class TipoCertificacionPropiedad(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "tipos_certificacion_propiedad"
    
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Relaciones
    transmisiones: Mapped[list["Transmision"]] = relationship("Transmision", back_populates="tipo_certificacion_propiedad")
    inmatriculaciones: Mapped[list["Inmatriculacion"]] = relationship("Inmatriculacion", back_populates="tipo_certificacion_propiedad")

class TipoDocumento(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "tipos_documento"
    
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Relaciones
    inmuebles_documentos: Mapped[list["InmuebleDocumento"]] = relationship("InmuebleDocumento", back_populates="tipo_documento")
    actuaciones_documentos: Mapped[list["ActuacionDocumento"]] = relationship("ActuacionDocumento", back_populates="tipo_documento")
    transmisiones_documentos: Mapped[list["TransmisionDocumento"]] = relationship("TransmisionDocumento", back_populates="tipo_documento")

class TipoInmueble(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "tipos_inmueble"
    
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Relaciones
    inmuebles: Mapped[list["Inmueble"]] = relationship("Inmueble", back_populates="tipo_inmueble")

class TipoMimeDocumento(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "tipos_mime_documento"
    
    tipo_mime: Mapped[str] = mapped_column(String(100), unique=True)
    extension: Mapped[str] = mapped_column(String(10))
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)

class TipoPersona(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "tipos_persona"
    
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Relaciones
    adquirientes: Mapped[list["Adquiriente"]] = relationship("Adquiriente", back_populates="tipo_persona")
    transmitentes: Mapped[list["Transmitente"]] = relationship("Transmitente", back_populates="tipo_persona")

class TipoTransmision(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "tipos_transmision"
    
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Relaciones
    transmisiones: Mapped[list["Transmision"]] = relationship("Transmision", back_populates="tipo_transmision")

class TipoVia(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "tipos_via"
    
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Relaciones
    inmuebles: Mapped[list["Inmueble"]] = relationship("Inmueble", back_populates="tipo_via")