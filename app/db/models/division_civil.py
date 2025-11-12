from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from .base import Base, UUIDPKMixin, AuditMixin

class ComunidadAutonoma(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "comunidades_autonomas"
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    provincias = relationship("Provincia", back_populates="comunidad_autonoma")

class Provincia(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "provincias"
    nombre: Mapped[str] = mapped_column(String(100))
    comunidad_autonoma_id: Mapped[str] = mapped_column(String(36), ForeignKey("comunidades_autonomas.id"))
    comunidad_autonoma = relationship("ComunidadAutonoma", back_populates="provincias")
    localidades = relationship("Localidad", back_populates="provincia")

class Localidad(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "localidades"
    nombre: Mapped[str] = mapped_column(String(100))
    provincia_id: Mapped[str] = mapped_column(String(36), ForeignKey("provincias.id"))
    provincia = relationship("Provincia", back_populates="localidades")
