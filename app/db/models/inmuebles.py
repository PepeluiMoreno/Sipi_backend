from __future__ import annotations
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from .base import Base, UUIDPKMixin, AuditMixin

class Inmueble(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "inmuebles"
    nombre: Mapped[str]
    descripcion: Mapped[Optional[str]]
    direccion: Mapped[str]
    latitud: Mapped[Optional[float]]
    longitud: Mapped[Optional[float]]
    wikidata_qid: Mapped[Optional[str]] = mapped_column(nullable=True, unique=True)
    provincia_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("provincias.id"))
    localidad_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("localidades.id"))
    diocesis_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("diocesis.id"))
    tipo_inmueble_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("tipos_inmueble.id"))
    estado_conservacion_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("estados_conservacion.id"))
    estado_tratamiento_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("estados_tratamiento.id"))
    es_bic: Mapped[bool] = mapped_column(default=False)
    es_ruina: Mapped[bool] = mapped_column(default=False)
    esta_inmatriculado: Mapped[bool] = mapped_column(default=False)
    id_inmatriculacion: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=False), ForeignKey("transmisiones.id"), nullable=True)
