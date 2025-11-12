from __future__ import annotations
from typing import Optional, List
from sqlalchemy import Table, Column, UniqueConstraint, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from .base import Base, UUIDPKMixin, AuditMixin

usuario_rol = Table(
    "usuario_rol",
    Base.metadata,
    Column("usuario_id", UUID(as_uuid=False), ForeignKey("usuarios.id"), primary_key=True),
    Column("rol_id", UUID(as_uuid=False), ForeignKey("roles.id"), primary_key=True),
    Column("fecha_asignacion", DateTime, default=datetime.utcnow),
    Column("asignado_por", UUID(as_uuid=False), ForeignKey("usuarios.id"))
)

class Usuario(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "usuarios"
    email: Mapped[str] = mapped_column(unique=True, index=True)
    nombre: Mapped[str]
    apellidos: Mapped[str]
    activo: Mapped[bool] = mapped_column(default=True)
    email_verificado: Mapped[bool] = mapped_column(default=False)
    roles: Mapped[List["Rol"]] = relationship("Rol", secondary=usuario_rol, back_populates="usuarios")

class Rol(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "roles"
    __table_args__ = (UniqueConstraint("nombre", name="uq_roles_nombre"),)
    nombre: Mapped[str]
    descripcion: Mapped[Optional[str]]
    activo: Mapped[bool] = mapped_column(default=True)
    usuarios: Mapped[List["Usuario"]] = relationship("Usuario", secondary=usuario_rol, back_populates="roles")
