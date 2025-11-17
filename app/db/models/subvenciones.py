# models/subvenciones.py
from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Float, ForeignKey
from app.db.base import Base
from app.db.mixins import  UUIDPKMixin, AuditMixin

if TYPE_CHECKING:
    from .actuaciones import Actuacion
    from .agentes import Administracion

class ActuacionSubvencion(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "actuaciones_subvenciones"
    
    actuacion_id: Mapped[str] = mapped_column(String(36), ForeignKey("actuaciones.id"))
    codigo_concesion: Mapped[str] = mapped_column(String(100))
    importe_aplicado: Mapped[float | None] = mapped_column(Float, nullable=True)
    porcentaje_financiacion: Mapped[float | None] = mapped_column(Float, nullable=True)
    fecha_aplicacion: Mapped[str | None] = mapped_column(String(20), nullable=True)
    justificacion_gasto: Mapped[str | None] = mapped_column(Text, nullable=True)
    observaciones: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Relaciones
    actuacion: Mapped["Actuacion"] = relationship("Actuacion")
    administraciones: Mapped[list["SubvencionAdministracion"]] = relationship("SubvencionAdministracion", back_populates="subvencion")

class SubvencionAdministracion(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "subvenciones_administraciones"
    
    subvencion_id: Mapped[str] = mapped_column(String(36), ForeignKey("actuaciones_subvenciones.id"))
    administracion_id: Mapped[str] = mapped_column(String(36), ForeignKey("administraciones.id"))
    importe_aportado: Mapped[float | None] = mapped_column(Float, nullable=True)
    porcentaje_participacion: Mapped[float | None] = mapped_column(Float, nullable=True)
    
    # Relaciones
    subvencion: Mapped["ActuacionSubvencion"] = relationship("ActuacionSubvencion", back_populates="administraciones")
    administracion: Mapped["Administracion"] = relationship("Administracion")
