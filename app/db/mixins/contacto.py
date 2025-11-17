# app/db/mixins/contacto.py
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text
from .direccion import DireccionMixin

class ContactoMixin:
    """
    Mixin para datos de contacto estándar
    """
    email: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    telefono: Mapped[str | None] = mapped_column(String(20), nullable=True)
    telefono_movil: Mapped[str | None] = mapped_column(String(20), nullable=True)
    fax: Mapped[str | None] = mapped_column(String(20), nullable=True)
    sitio_web: Mapped[str | None] = mapped_column(String(500), nullable=True)
    # Campo notas (reemplaza observaciones)
    notas: Mapped[str | None] = mapped_column(String(200), nullable=True)

class ContactoDireccionMixin(ContactoMixin, DireccionMixin):
    """
    Mixin combinado con datos de contacto y dirección básica
    """
    pass