from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Integer, ForeignKey
from .base import Base, UUIDPKMixin, AuditMixin

class FuenteHistoriografica(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "fuentes_historiograficas"
    titulo: Mapped[str] = mapped_column(String(500))
    autor: Mapped[str | None] = mapped_column(String(255), nullable=True)
    editorial: Mapped[str | None] = mapped_column(String(255), nullable=True)
    año_publicacion: Mapped[int | None] = mapped_column(Integer, nullable=True)
    isbn: Mapped[str | None] = mapped_column(String(20), nullable=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)

class CitaHistoriografica(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "citas_historiograficas"
    fuente_id: Mapped[str] = mapped_column(String(36), ForeignKey("fuentes_historiograficas.id"))
    inmueble_id: Mapped[str] = mapped_column(String(36), ForeignKey("inmuebles.id"))
    paginas: Mapped[str | None] = mapped_column(String(100), nullable=True)
    texto_cita: Mapped[str] = mapped_column(Text)
    notas: Mapped[str | None] = mapped_column(Text, nullable=True)
