from __future__ import annotations
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from .base import Base, UUIDPKMixin, AuditMixin

class ActuacionSubvencion(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "actuaciones_subvenciones"
    actuacion_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("actuaciones.id"))
    codigo_concesion: Mapped[str]
    importe_aplicado: Mapped[Optional[float]]
    porcentaje_financiacion: Mapped[Optional[float]]
    fecha_aplicacion: Mapped[Optional[str]]
    justificacion_gasto: Mapped[Optional[str]]
    observaciones: Mapped[Optional[str]]

class SubvencionAdministracion(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "subvenciones_administraciones"
    subvencion_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("actuaciones_subvenciones.id"))
    administracion_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("administraciones.id"))
    importe_aportado: Mapped[Optional[float]]
    porcentaje_participacion: Mapped[Optional[float]]
