from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Float, ForeignKey
from .base import Base, UUIDPKMixin, AuditMixin

class ActuacionSubvencion(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "actuaciones_subvenciones"
    actuacion_id: Mapped[str] = mapped_column(String(36), ForeignKey("actuaciones.id"))
    codigo_concesion: Mapped[str] = mapped_column(String(100))
    importe_aplicado: Mapped[float | None] = mapped_column(Float, nullable=True)
    porcentaje_financiacion: Mapped[float | None] = mapped_column(Float, nullable=True)
    fecha_aplicacion: Mapped[str | None] = mapped_column(String(20), nullable=True)
    justificacion_gasto: Mapped[str | None] = mapped_column(Text, nullable=True)
    observaciones: Mapped[str | None] = mapped_column(Text, nullable=True)

class SubvencionAdministracion(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "subvenciones_administraciones"
    subvencion_id: Mapped[str] = mapped_column(String(36), ForeignKey("actuaciones_subvenciones.id"))
    administracion_id: Mapped[str] = mapped_column(String(36), ForeignKey("administraciones.id"))
    importe_aportado: Mapped[float | None] = mapped_column(Float, nullable=True)
    porcentaje_participacion: Mapped[float | None] = mapped_column(Float, nullable=True)
