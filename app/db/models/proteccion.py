from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, DateTime, Boolean, ForeignKey
from .base import Base, UUIDPKMixin, AuditMixin

class FiguraProteccion(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "figuras_proteccion"
    nombre: Mapped[str] = mapped_column(String(150), unique=True)
    nombre_normalizado: Mapped[str | None] = mapped_column(String(150), nullable=True, index=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    ambito: Mapped[str | None] = mapped_column(String(50), nullable=True)
    wikidata_qid: Mapped[str | None] = mapped_column(String(32), nullable=True, unique=True)

class InmuebleFiguraProteccion(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "inmuebles_figuras_proteccion"
    inmueble_id: Mapped[str] = mapped_column(String(36), ForeignKey("inmuebles.id"))
    figura_proteccion_id: Mapped[str] = mapped_column(String(36), ForeignKey("figuras_proteccion.id"))
    administracion_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("administraciones.id"), nullable=True)
    bic_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    norma: Mapped[str | None] = mapped_column(Text, nullable=True)
    fecha_declaracion: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True)
