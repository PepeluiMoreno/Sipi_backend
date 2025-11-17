from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Boolean, DateTime, ForeignKey, Table, Column
from datetime import datetime
from app.db.base import Base
from app.db.mixins import UUIDPKMixin, AuditMixin

usuario_rol = Table(
    "usuario_rol",
    Base.metadata,
    Column("usuario_id", String(36), ForeignKey("usuarios.id"), primary_key=True),
    Column("rol_id", String(36), ForeignKey("roles.id"), primary_key=True),
    Column("fecha_asignacion", DateTime, default=datetime.utcnow),
    Column("asignado_por", String(36), ForeignKey("usuarios.id"), nullable=True),
)

class Usuario(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "usuarios"
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100))
    apellidos: Mapped[str] = mapped_column(String(200))
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    email_verificado: Mapped[bool] = mapped_column(Boolean, default=False)
    roles = relationship(
        "Rol",
        secondary=usuario_rol,
        primaryjoin="Usuario.id == usuario_rol.c.usuario_id",
        secondaryjoin="usuario_rol.c.rol_id == Rol.id",
        back_populates="usuarios"
    )

class Rol(UUIDPKMixin, AuditMixin, Base):
    __tablename__ = "roles"
    nombre: Mapped[str] = mapped_column(String(50), unique=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    usuarios = relationship(
        "Usuario",
        secondary=usuario_rol,
        primaryjoin="Rol.id == usuario_rol.c.rol_id",
        secondaryjoin="usuario_rol.c.usuario_id == Usuario.id",
        back_populates="roles"
    )
