from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum
import enum

class TipoIdentificacion(enum.Enum):
    DNI = "dni"
    NIE = "nie" 
    CIF = "cif"
    PASAPORTE = "pasaporte"
    NIF = "nif"
    CIF_EXTRANJERO = "cif_extranjero"
    OTRO = "otro"

class PersonaFisicaIdentMixin:
    """Identificación para personas físicas"""
    tipo_identificacion: Mapped[TipoIdentificacion | None] = mapped_column(
        Enum(TipoIdentificacion), nullable=True, index=True
    )
    identificacion: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100))
    apellidos: Mapped[str] = mapped_column(String(200))

class PersonaJuridicaIdentMixin:
    """Identificación para personas jurídicas"""
    tipo_identificacion: Mapped[TipoIdentificacion | None] = mapped_column(
        Enum(TipoIdentificacion), nullable=True, index=True
    )
    identificacion: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    nombre: Mapped[str] = mapped_column(String(255))
    identificacion_extranjera: Mapped[str | None] = mapped_column(String(50), nullable=True)