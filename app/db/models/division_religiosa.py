from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey
from .base import Base, UUIDPKMixin, AuditMixin

class Diocesis(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "diocesis"
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    wikidata_qid: Mapped[str | None] = mapped_column(String(32), unique=True, nullable=True)
    titulares = relationship("DiocesisTitular", back_populates="diocesis")

class DiocesisTitular(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "diocesis_titulares"
    diocesis_id: Mapped[str] = mapped_column(String(36), ForeignKey("diocesis.id"))
    profesional_id: Mapped[str] = mapped_column(String(36), nullable=False)
    fecha_inicio: Mapped[str | None] = mapped_column(String(20), nullable=True)
    fecha_fin: Mapped[str | None] = mapped_column(String(20), nullable=True)
    observaciones: Mapped[str | None] = mapped_column(Text, nullable=True)
    diocesis = relationship("Diocesis", back_populates="titulares")
