from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Float, ForeignKey
from .base import Base, UUIDPKMixin, AuditMixin

class Transmision(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "transmisiones"
    inmueble_id: Mapped[str] = mapped_column(String(36), ForeignKey("inmuebles.id"))
    adquiriente_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("adquirientes.id"), nullable=True)
    tipo_transmision_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("tipos_transmision.id"), nullable=True)
    tipo_certificacion_propiedad_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("tipos_certificacion_propiedad.id"), nullable=True)
    fecha_transmision: Mapped[str | None] = mapped_column(String(20), nullable=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    inmueble = relationship("Inmueble", back_populates="transmisiones")

class Actuacion(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "actuaciones"
    inmueble_id: Mapped[str] = mapped_column(String(36), ForeignKey("inmuebles.id"))
    nombre: Mapped[str] = mapped_column(String(255))
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    fecha_inicio: Mapped[str | None] = mapped_column(String(20), nullable=True)
    fecha_fin: Mapped[str | None] = mapped_column(String(20), nullable=True)
    presupuesto: Mapped[float | None] = mapped_column(Float, nullable=True)
    inmueble = relationship("Inmueble", back_populates="actuaciones")
    participaciones = relationship("ActuacionParticipacion", back_populates="actuacion")

class ActuacionParticipacion(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "actuaciones_participaciones"
    actuacion_id: Mapped[str] = mapped_column(String(36), ForeignKey("actuaciones.id"))
    profesional_id: Mapped[str] = mapped_column(String(36), ForeignKey("profesionales.id"))
    rol_profesional_id: Mapped[str] = mapped_column(String(36), ForeignKey("roles_profesional.id"))
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    fecha_inicio: Mapped[str | None] = mapped_column(String(20), nullable=True)
    fecha_fin: Mapped[str | None] = mapped_column(String(20), nullable=True)
    actuacion = relationship("Actuacion", back_populates="participaciones")
