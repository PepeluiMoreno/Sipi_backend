# models/geografia.py
from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from app.db.base import Base
from app.db.mixins import UUIDPKMixin, AuditMixin

if TYPE_CHECKING:
    from .inmuebles import Inmueble
    from .agentes import Notaria, RegistroPropiedad, AgenciaInmobiliaria, Administracion

class ComunidadAutonoma(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "comunidades_autonomas"
    
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    
    # Relaciones
    provincias: Mapped[list["Provincia"]] = relationship("Provincia", back_populates="comunidad_autonoma")
    inmuebles: Mapped[list["Inmueble"]] = relationship("Inmueble", back_populates="comunidad_autonoma")
    administraciones: Mapped[list["Administracion"]] = relationship("Administracion", back_populates="comunidad_autonoma")

class Provincia(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "provincias"
    
    nombre: Mapped[str] = mapped_column(String(100))
    comunidad_autonoma_id: Mapped[str] = mapped_column(String(36), ForeignKey("comunidades_autonomas.id"))
    
    # Relaciones
    comunidad_autonoma: Mapped["ComunidadAutonoma"] = relationship("ComunidadAutonoma", back_populates="provincias")
    localidades: Mapped[list["Localidad"]] = relationship("Localidad", back_populates="provincia")
    inmuebles: Mapped[list["Inmueble"]] = relationship("Inmueble", back_populates="provincia")

class Localidad(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "localidades"
    
    nombre: Mapped[str] = mapped_column(String(100))
    provincia_id: Mapped[str] = mapped_column(String(36), ForeignKey("provincias.id"))
    
    # Relaciones
    provincia: Mapped["Provincia"] = relationship("Provincia", back_populates="localidades")
    inmuebles: Mapped[list["Inmueble"]] = relationship("Inmueble", back_populates="localidad")
    notarias: Mapped[list["Notaria"]] = relationship("Notaria", back_populates="localidad")
    registros_propiedad: Mapped[list["RegistroPropiedad"]] = relationship("RegistroPropiedad", back_populates="localidad")
    agencias_inmobiliarias: Mapped[list["AgenciaInmobiliaria"]] = relationship("AgenciaInmobiliaria", back_populates="localidad")