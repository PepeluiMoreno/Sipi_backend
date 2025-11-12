from __future__ import annotations
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from .base import Base, UUIDPKMixin, AuditMixin

class Transmision(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "transmisiones"
    inmueble_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("inmuebles.id"))
    adquiriente_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("adquirientes.id"))
    tipo_transmision_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("tipos_transmision.id"))
    tipo_certificacion_propiedad_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=False), ForeignKey("tipos_certificacion_propiedad.id"), nullable=True)
    fecha_transmision: Mapped[str]
    descripcion: Mapped[Optional[str]]

class Actuacion(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "actuaciones"
    inmueble_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("inmuebles.id"))
    nombre: Mapped[str]
    descripcion: Mapped[Optional[str]]
    fecha_inicio: Mapped[str]
    fecha_fin: Mapped[Optional[str]]
    presupuesto: Mapped[Optional[float]]

class ActuacionParticipacion(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "actuaciones_participaciones"
    actuacion_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("actuaciones.id"))
    profesional_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("profesionales.id"))
    rol_profesional_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("roles_profesional.id"))
    descripcion: Mapped[Optional[str]]
    fecha_inicio: Mapped[str]
    fecha_fin: Mapped[Optional[str]]
