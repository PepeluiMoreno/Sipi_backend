# models/transmisiones.py
from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Float, ForeignKey
from .base import Base, UUIDPKMixin, AuditMixin

if TYPE_CHECKING:
    from .inmuebles import Inmueble
    from .agentes import Adquiriente, Transmitente, Notaria, RegistroPropiedad, AgenciaInmobiliaria
    from .catalogos import TipoTransmision, TipoCertificacionPropiedad
    from .documentos import TransmisionDocumento

class Transmision(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "transmisiones"
    
    inmueble_id: Mapped[str] = mapped_column(String(36), ForeignKey("inmuebles.id"))
    transmitente_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("transmitentes.id"), nullable=True)
    adquiriente_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("adquirientes.id"), nullable=True)
    notaria_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("notarias.id"), nullable=True)
    registro_propiedad_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("registros_propiedad.id"), nullable=True)
    tipo_transmision_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("tipos_transmision.id"), nullable=True)
    tipo_certificacion_propiedad_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("tipos_certificacion_propiedad.id"), nullable=True)
    fecha_transmision: Mapped[str | None] = mapped_column(String(20), nullable=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    precio_venta: Mapped[float | None] = mapped_column(Float, nullable=True)
    
    # Relaciones
    inmueble: Mapped["Inmueble"] = relationship("Inmueble", back_populates="transmisiones", foreign_keys=[inmueble_id])
    transmitente: Mapped["Transmitente"] = relationship("Transmitente", back_populates="transmisiones")
    adquiriente: Mapped["Adquiriente"] = relationship("Adquiriente", back_populates="transmisiones")
    notaria: Mapped["Notaria"] = relationship("Notaria", back_populates="transmisiones")
    registro_propiedad: Mapped["RegistroPropiedad"] = relationship("RegistroPropiedad", back_populates="transmisiones")
    tipo_transmision: Mapped["TipoTransmision"] = relationship("TipoTransmision", back_populates="transmisiones")
    tipo_certificacion_propiedad: Mapped["TipoCertificacionPropiedad"] = relationship("TipoCertificacionPropiedad", back_populates="transmisiones")
    documentos: Mapped[list["TransmisionDocumento"]] = relationship("TransmisionDocumento", back_populates="transmision")
    anunciantes: Mapped[list["TransmisionAnunciantes"]] = relationship("TransmisionAnunciantes", back_populates="transmision")

class Inmatriculacion(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "inmatriculaciones"
    
    inmueble_id: Mapped[str] = mapped_column(String(36), ForeignKey("inmuebles.id"), unique=True, nullable=False)
    # notaria_id eliminado
    registro_propiedad_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("registros_propiedad.id"), nullable=True)
    tipo_certificacion_propiedad_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("tipos_certificacion_propiedad.id"), nullable=True)
    fecha: Mapped[str | None] = mapped_column(String(20), nullable=True)
    
    # Relaciones
    inmueble: Mapped["Inmueble"] = relationship("Inmueble", back_populates="inmatriculacion", uselist=False)
    # notaria eliminada
    registro_propiedad: Mapped["RegistroPropiedad"] = relationship("RegistroPropiedad", back_populates="inmatriculaciones")
    tipo_certificacion_propiedad: Mapped["TipoCertificacionPropiedad"] = relationship("TipoCertificacionPropiedad", back_populates="inmatriculaciones")

class TransmisionAnunciantes(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "transmision_anunciantes"
    
    transmision_id: Mapped[str] = mapped_column(String(36), ForeignKey("transmisiones.id"))
    agencia_inmobiliaria_id: Mapped[str] = mapped_column(String(36), ForeignKey("agencias_inmobiliarias.id"))
    
    # Relaciones
    transmision: Mapped["Transmision"] = relationship("Transmision", back_populates="anunciantes")
    agencia_inmobiliaria: Mapped["AgenciaInmobiliaria"] = relationship("AgenciaInmobiliaria", back_populates="transmisiones_anunciadas")