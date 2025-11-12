from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Float, Boolean, ForeignKey
from .base import Base, UUIDPKMixin, AuditMixin

class Inmueble(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "inmuebles"
    nombre: Mapped[str | None] = mapped_column(String(255), nullable=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    direccion: Mapped[str | None] = mapped_column(Text, nullable=True)
    latitud: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitud: Mapped[float | None] = mapped_column(Float, nullable=True)

    provincia_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("provincias.id"), nullable=True)
    localidad_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("localidades.id"), nullable=True)
    diocesis_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("diocesis.id"), nullable=True)

    tipo_inmueble_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("tipos_inmueble.id"), nullable=True)
    estado_conservacion_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("estados_conservacion.id"), nullable=True)
    estado_tratamiento_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("estados_tratamiento.id"), nullable=True)

    es_bic: Mapped[bool] = mapped_column(Boolean, default=False)
    es_ruina: Mapped[bool] = mapped_column(Boolean, default=False)
    esta_inmatriculado: Mapped[bool] = mapped_column(Boolean, default=False)
    id_inmatriculacion: Mapped[str | None] = mapped_column(String(36), ForeignKey("transmisiones.id"), nullable=True)

    transmisiones = relationship("Transmision", back_populates="inmueble")
    actuaciones = relationship("Actuacion", back_populates="inmueble")
