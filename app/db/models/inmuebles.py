# models/inmuebles.py
from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Float, Boolean, ForeignKey, Integer, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
from geoalchemy2 import Geometry
from .base import Base, UUIDPKMixin, AuditMixin

if TYPE_CHECKING:
    from .geografia import Provincia, Localidad, ComunidadAutonoma
    from .agentes import Diocesis
    from .catalogos import TipoInmueble, EstadoConservacion, EstadoTratamiento
    from .transmisiones import Transmision, Inmatriculacion
    from .actuaciones import Actuacion
    from .documentos import InmuebleDocumento
    from .historiografia import CitaHistoriografica
class Inmueble(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "inmuebles"
    
    nombre: Mapped[str | None] = mapped_column(String(255), nullable=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    direccion: Mapped[str | None] = mapped_column(Text, nullable=True)
    latitud: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitud: Mapped[float | None] = mapped_column(Float, nullable=True)
    comunidad_autonoma_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("comunidades_autonomas.id"), nullable=True)
    provincia_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("provincias.id"), nullable=True)
    localidad_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("localidades.id"), nullable=True)
    diocesis_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("diocesis.id"), nullable=True)
    tipo_inmueble_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("tipos_inmueble.id"), nullable=True)
    estado_conservacion_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("estados_conservacion.id"), nullable=True)
    estado_tratamiento_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("estados_tratamiento.id"), nullable=True)
    es_bic: Mapped[bool] = mapped_column(Boolean, default=False)
    es_ruina: Mapped[bool] = mapped_column(Boolean, default=False)
    # Eliminados: esta_inmatriculado e id_inmatriculacion
    
    # Relaciones
    comunidad_autonoma: Mapped["ComunidadAutonoma"] = relationship("ComunidadAutonoma", back_populates="inmuebles")
    provincia: Mapped["Provincia"] = relationship("Provincia", back_populates="inmuebles")
    localidad: Mapped["Localidad"] = relationship("Localidad", back_populates="inmuebles")
    diocesis: Mapped["Diocesis"] = relationship("Diocesis", back_populates="inmuebles")
    tipo_inmueble: Mapped["TipoInmueble"] = relationship("TipoInmueble", back_populates="inmuebles")
    estado_conservacion: Mapped["EstadoConservacion"] = relationship("EstadoConservacion", back_populates="inmuebles")
    estado_tratamiento: Mapped["EstadoTratamiento"] = relationship("EstadoTratamiento", back_populates="inmuebles")
    transmisiones: Mapped[list["Transmision"]] = relationship("Transmision", back_populates="inmueble", foreign_keys="[Transmision.inmueble_id]")
    actuaciones: Mapped[list["Actuacion"]] = relationship("Actuacion", back_populates="inmueble")
    documentos: Mapped[list["InmuebleDocumento"]] = relationship("InmuebleDocumento", back_populates="inmueble")
    inmatriculacion: Mapped["Inmatriculacion"] = relationship("Inmatriculacion", back_populates="inmueble", uselist=False, cascade="all, delete-orphan")
    citas_historiograficas: Mapped[list["CitaHistoriografica"]] = relationship("CitaHistoriografica", back_populates="inmueble")

    # Relaciones 1:1 con datos externos
    osm_ext: Mapped["InmuebleOSMExt"] = relationship("InmuebleOSMExt", back_populates="inmueble", uselist=False, cascade="all, delete-orphan")
    wd_ext: Mapped["InmuebleWDExt"] = relationship("InmuebleWDExt", back_populates="inmueble", uselist=False, cascade="all, delete-orphan")

class InmuebleOSMExt(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "inmuebles_osm_ext"
    
    inmueble_id: Mapped[str] = mapped_column(String(36), ForeignKey("inmuebles.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    osm_id: Mapped[str | None] = mapped_column(String(50), nullable=True, unique=True, index=True)
    osm_type: Mapped[str | None] = mapped_column(String(10), nullable=True)
    version: Mapped[int | None] = mapped_column(Integer, nullable=True)
    name: Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    inferred_type: Mapped[str | None] = mapped_column(String, nullable=True)
    denomination: Mapped[str | None] = mapped_column(String, nullable=True)
    diocese: Mapped[str | None] = mapped_column(String, nullable=True)
    operator: Mapped[str | None] = mapped_column(String, nullable=True)
    geom: Mapped[Geometry | None] = mapped_column(Geometry('POINT', srid=4326), nullable=True)
    heritage_status: Mapped[str | None] = mapped_column(String, nullable=True)
    historic: Mapped[str | None] = mapped_column(String, nullable=True)
    ruins: Mapped[bool] = mapped_column(Boolean, default=False)
    has_polygon: Mapped[bool] = mapped_column(Boolean, default=False)
    address_street: Mapped[str | None] = mapped_column(String, nullable=True)
    address_city: Mapped[str | None] = mapped_column(String, nullable=True)
    address_postcode: Mapped[str | None] = mapped_column(String, nullable=True)
    source_updated_at: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)
    tags: Mapped[dict | None] = mapped_column(MutableDict.as_mutable(JSONB), nullable=True)
    raw: Mapped[dict | None] = mapped_column(MutableDict.as_mutable(JSONB), nullable=True)
    qa_flags: Mapped[dict | None] = mapped_column(MutableDict.as_mutable(JSONB), nullable=True)
    source_refs: Mapped[dict | None] = mapped_column(MutableDict.as_mutable(JSONB), nullable=True)
    
    inmueble: Mapped["Inmueble"] = relationship("Inmueble", back_populates="osm_ext", uselist=False)
  

class InmuebleWDExt(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "inmuebles_wd_ext"
    
    inmueble_id: Mapped[str] = mapped_column(String(36), ForeignKey("inmuebles.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    wikidata_qid: Mapped[str | None] = mapped_column(String(32), nullable=True, unique=True, index=True)
    commons_category: Mapped[str | None] = mapped_column(String(255), nullable=True)
    inception: Mapped[str | None] = mapped_column(String, nullable=True)
    source_updated_at: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)
    claims: Mapped[dict | None] = mapped_column(MutableDict.as_mutable(JSONB), nullable=True)
    sitelinks: Mapped[dict | None] = mapped_column(MutableDict.as_mutable(JSONB), nullable=True)
    raw: Mapped[dict | None] = mapped_column(MutableDict.as_mutable(JSONB), nullable=True)
    
    inmueble: Mapped["Inmueble"] = relationship("Inmueble", back_populates="wd_ext", uselist=False)