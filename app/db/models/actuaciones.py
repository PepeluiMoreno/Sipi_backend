# models/actuaciones.py
from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Float, ForeignKey
from .base import Base, UUIDPKMixin, AuditMixin

if TYPE_CHECKING:
    from .inmuebles import Inmueble
    from .agentes import Tecnico
    from .catalogos import RolTecnico
    from .documentos import ActuacionDocumento

class Actuacion(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "actuaciones"
    
    inmueble_id: Mapped[str] = mapped_column(String(36), ForeignKey("inmuebles.id"))
    nombre: Mapped[str] = mapped_column(String(255))
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    fecha_inicio: Mapped[str | None] = mapped_column(String(20), nullable=True)
    fecha_fin: Mapped[str | None] = mapped_column(String(20), nullable=True)
    presupuesto: Mapped[float | None] = mapped_column(Float, nullable=True)
    
    # Relaciones
    inmueble: Mapped["Inmueble"] = relationship("Inmueble", back_populates="actuaciones")
    tecnicos: Mapped[list["ActuacionTecnicos"]] = relationship("ActuacionTecnicos", back_populates="actuacion")
    documentos: Mapped[list["ActuacionDocumento"]] = relationship("ActuacionDocumento", back_populates="actuacion")

class ActuacionTecnicos(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "actuaciones_tecnicos"
    
    actuacion_id: Mapped[str] = mapped_column(String(36), ForeignKey("actuaciones.id"))
    tecnico_id: Mapped[str] = mapped_column(String(36), ForeignKey("tecnicos.id"))
    rol_tecnico_id: Mapped[str] = mapped_column(String(36), ForeignKey("roles_tecnico.id"))
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    fecha_inicio: Mapped[str | None] = mapped_column(String(20), nullable=True)
    fecha_fin: Mapped[str | None] = mapped_column(String(20), nullable=True)
    
    # Relaciones
    actuacion: Mapped["Actuacion"] = relationship("Actuacion", back_populates="tecnicos")
    tecnico: Mapped["Tecnico"] = relationship("Tecnico", back_populates="actuaciones_tecnicos")
    rol_tecnico: Mapped["RolTecnico"] = relationship("RolTecnico", back_populates="actuaciones_tecnicos")