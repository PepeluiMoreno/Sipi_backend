
# models/proteccion.py
from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, DateTime, Boolean, ForeignKey
from app.db.base import Base, UUIDPKMixin, AuditMixin

if TYPE_CHECKING:
    from .inmuebles import Inmueble
    from .catalogos import FigurasProteccion
    from .agentes import Administracion

class InmuebleFiguraProteccion(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "inmuebles_figuras_proteccion"
    
    inmueble_id: Mapped[str] = mapped_column(String(36), ForeignKey("inmuebles.id"))
    figura_proteccion_id: Mapped[str] = mapped_column(String(36), ForeignKey("figuras_proteccion.id"))
    administracion_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("administraciones.id"), nullable=True)
    bic_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    norma: Mapped[str | None] = mapped_column(Text, nullable=True)
    fecha_declaracion: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)
    
    # Relaciones
    inmueble: Mapped["Inmueble"] = relationship("Inmueble")
    figura_proteccion: Mapped["FigurasProteccion"] = relationship("FigurasProteccion")
    administracion: Mapped["Administracion"] = relationship("Administracion")