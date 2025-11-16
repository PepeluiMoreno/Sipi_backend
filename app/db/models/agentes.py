from __future__ import annotations
from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey
from app.db.base import Base
from app.db.mixins import (
    AuditMixin, UUIDPKMixin, PersonaFisicaIdentMixin, 
    PersonaJuridicaIdentMixin, ContactoDireccionMixin, TitularidadMixin
)

if TYPE_CHECKING:
    from .inmuebles import Inmueble
    from .catalogos import TipoPersona, RolTecnico
    from .transmisiones import Transmision, TransmisionAnunciantes, Inmatriculacion
    from .actuaciones import ActuacionTecnicos
    from .geografia import Localidad, ComunidadAutonoma

class Adquiriente(UUIDPKMixin, AuditMixin, PersonaJuridicaIdentMixin, Base):
    __tablename__ = "adquirientes"
    
    tipo_persona_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("tipos_persona.id"), nullable=True)
   
    # Relaciones
    tipo_persona: Mapped["TipoPersona"] = relationship("TipoPersona", back_populates="adquirientes")
    transmisiones: Mapped[list["Transmision"]] = relationship("Transmision", back_populates="adquiriente")

class Administracion(UUIDPKMixin, AuditMixin, ContactoDireccionMixin, Base):
    __tablename__ = "administraciones"
    
    nombre: Mapped[str] = mapped_column(String(255), unique=True)
    ambito: Mapped[str | None] = mapped_column(String(100), nullable=True)
    
    # Relaciones
    titulares: Mapped[list["AdministracionTitular"]] = relationship("AdministracionTitular", back_populates="administracion")
    comunidad_autonoma: Mapped["ComunidadAutonoma"] = relationship("ComunidadAutonoma", back_populates="administraciones")

class AdministracionTitular(UUIDPKMixin, AuditMixin, PersonaFisicaIdentMixin, Base):
    __tablename__ = "administraciones_titulares"
    
    administracion_id: Mapped[str] = mapped_column(String(36), ForeignKey("administraciones.id"))
    cargo: Mapped[str | None] = mapped_column(String(100), nullable=True)
    fecha_inicio: Mapped[str] = mapped_column(String(20))
    fecha_fin: Mapped[str | None] = mapped_column(String(20), nullable=True)
    
    # Relación
    administracion: Mapped["Administracion"] = relationship("Administracion", back_populates="titulares")

class AgenciaInmobiliaria(UUIDPKMixin, AuditMixin, ContactoDireccionMixin, Base):
    __tablename__ = "agencias_inmobiliarias"
    
    nombre: Mapped[str] = mapped_column(String(255))
    
    # Relaciones
    titulares: Mapped[list["AgenciaInmobiliariaTitular"]] = relationship("AgenciaInmobiliariaTitular", back_populates="agencia_inmobiliaria")
    transmisiones_anunciadas: Mapped[list["TransmisionAnunciantes"]] = relationship("TransmisionAnunciantes", back_populates="agencia_inmobiliaria")
    localidad: Mapped["Localidad"] = relationship("Localidad", back_populates="agencias_inmobiliarias")

class AgenciaInmobiliariaTitular(UUIDPKMixin, AuditMixin, PersonaFisicaIdentMixin, Base):
    __tablename__ = "agencias_inmobiliarias_titulares"
    
    agencia_inmobiliaria_id: Mapped[str] = mapped_column(String(36), ForeignKey("agencias_inmobiliarias.id"))
    fecha_inicio: Mapped[str] = mapped_column(String(20))
    fecha_fin: Mapped[str | None] = mapped_column(String(20), nullable=True)
    
    # Relación
    agencia_inmobiliaria: Mapped["AgenciaInmobiliaria"] = relationship("AgenciaInmobiliaria", back_populates="titulares")

class ColegioProfesional(UUIDPKMixin, AuditMixin, ContactoDireccionMixin, Base):
    __tablename__ = "colegios_profesionales"
    
    nombre: Mapped[str] = mapped_column(String(255), unique=True)
    codigo: Mapped[str | None] = mapped_column(String(50), nullable=True)
    
    # Relaciones
    tecnicos: Mapped[list["Tecnico"]] = relationship("Tecnico", back_populates="colegio_profesional")

class Diocesis(UUIDPKMixin, AuditMixin, ContactoDireccionMixin, Base):
    __tablename__ = "diocesis"
    
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    wikidata_qid: Mapped[str | None] = mapped_column(String(32), unique=True, nullable=True)
    
    # Relaciones
    titulares: Mapped[list["DiocesisTitular"]] = relationship("DiocesisTitular", back_populates="diocesis")
    inmuebles: Mapped[list["Inmueble"]] = relationship("Inmueble", back_populates="diocesis")

class DiocesisTitular(UUIDPKMixin, AuditMixin, PersonaFisicaIdentMixin, Base):
    __tablename__ = "diocesis_titulares"
    
    diocesis_id: Mapped[str] = mapped_column(String(36), ForeignKey("diocesis.id"))
    cargo: Mapped[str | None] = mapped_column(String(100), nullable=True)
    fecha_inicio: Mapped[str] = mapped_column(String(20))
    fecha_fin: Mapped[str | None] = mapped_column(String(20), nullable=True)
    
    # Relación
    diocesis: Mapped["Diocesis"] = relationship("Diocesis", back_populates="titulares")

class Notaria(UUIDPKMixin, AuditMixin, ContactoDireccionMixin, Base):
    __tablename__ = "notarias"
    
    nombre: Mapped[str] = mapped_column(String(255))
    
    # Relaciones
    titulares: Mapped[list["NotariaTitular"]] = relationship("NotariaTitular", back_populates="notaria")
    transmisiones: Mapped[list["Transmision"]] = relationship("Transmision", back_populates="notaria")
    localidad: Mapped["Localidad"] = relationship("Localidad", back_populates="notarias")

class NotariaTitular(UUIDPKMixin, AuditMixin, PersonaFisicaIdentMixin, Base):
    __tablename__ = "notarias_titulares"
    
    notaria_id: Mapped[str] = mapped_column(String(36), ForeignKey("notarias.id"))
    fecha_inicio: Mapped[str] = mapped_column(String(20))
    fecha_fin: Mapped[str | None] = mapped_column(String(20), nullable=True)
    
    # Relación
    notaria: Mapped["Notaria"] = relationship("Notaria", back_populates="titulares")

class Tecnico(UUIDPKMixin, AuditMixin, PersonaFisicaIdentMixin, ContactoDireccionMixin, Base):
    __tablename__ = "tecnicos"
    
    rol_tecnico_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("roles_tecnico.id"), nullable=True)
    colegio_profesional_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("colegios_profesionales.id"), nullable=True)
    numero_colegiado: Mapped[str | None] = mapped_column(String(50), nullable=True)
    fecha_colegiacion: Mapped[str | None] = mapped_column(String(20), nullable=True)
    
    # Relaciones
    rol_tecnico: Mapped["RolTecnico"] = relationship("RolTecnico", back_populates="tecnicos")
    colegio_profesional: Mapped["ColegioProfesional"] = relationship("ColegioProfesional", back_populates="tecnicos")
    actuaciones_tecnicos: Mapped[list["ActuacionTecnicos"]] = relationship("ActuacionTecnicos", back_populates="tecnico")

class RegistroPropiedad(UUIDPKMixin, AuditMixin, PersonaJuridicaIdentMixin, ContactoDireccionMixin, TitularidadMixin, Base):
    __tablename__ = 'registros_propiedad'
    
    localidad_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("localidades.id"), nullable=True)
    
    # Configuración para TitularidadMixin
    DENOMINACION_TITULARIDAD = "registrador"
    
    # Relaciones
    localidad: Mapped["Localidad"] = relationship("Localidad", back_populates="registros_propiedad")
    titulares: Mapped[list["RegistroTitular"]] = relationship("RegistroTitular", back_populates="registro_propiedad")

class RegistroTitular(UUIDPKMixin, AuditMixin, PersonaFisicaIdentMixin, Base):
    __tablename__ = "registros_titulares"
    
    registro_propiedad_id: Mapped[str] = mapped_column(String(36), ForeignKey("registros_propiedad.id"))
    fecha_inicio: Mapped[str] = mapped_column(String(20))
    fecha_fin: Mapped[str | None] = mapped_column(String(20), nullable=True)
    
    # Relación
    registro_propiedad: Mapped["RegistroPropiedad"] = relationship("RegistroPropiedad", back_populates="titulares")

class Transmitente(UUIDPKMixin, AuditMixin, PersonaJuridicaIdentMixin, ContactoDireccionMixin, Base):
    __tablename__ = "transmitentes"
    
    tipo_persona_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("tipos_persona.id"), nullable=True)
    
    # Relaciones
    tipo_persona: Mapped["TipoPersona"] = relationship("TipoPersona", back_populates="transmitentes")
    transmisiones: Mapped[list["Transmision"]] = relationship("Transmision", back_populates="transmitente")