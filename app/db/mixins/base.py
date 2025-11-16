from sqlalchemy import String, DateTime, Boolean
from datetime import datetime
import uuid
from sqlalchemy.orm import Mapped, mapped_column, Optional, Column, ForeignKey, relationship, declared_attr, Integer    


class UUIDPKMixin:
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))


class AuditMixin:
    """
    Mixin para campos de auditoría
    Tracking de quién y cuándo crea/modifica/elimina registros
    """
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, onupdate=datetime.utcnow, index=True)
    deleted_at = Column(DateTime, index=True)  # Soft delete
    
    # Usuarios responsables
    @declared_attr
    def created_by_id(cls):
        return Column(Integer, ForeignKey("usuarios.id"))
    
    @declared_attr
    def updated_by_id(cls):
        return Column(Integer, ForeignKey("usuarios.id"))
    
    @declared_attr
    def deleted_by_id(cls):
        return Column(Integer, ForeignKey("usuarios.id"))
    
    # Relaciones a usuarios
    @declared_attr
    def created_by(cls):
        return relationship(
            "Usuario",
            foreign_keys=[cls.created_by_id],
            primaryjoin=f"Usuario.id == {cls.__name__}.created_by_id"
        )
    
    @declared_attr
    def updated_by(cls):
        return relationship(
            "Usuario",
            foreign_keys=[cls.updated_by_id],
            primaryjoin=f"Usuario.id == {cls.__name__}.updated_by_id"
        )
    
    @declared_attr
    def deleted_by(cls):
        return relationship(
            "Usuario",
            foreign_keys=[cls.deleted_by_id],
            primaryjoin=f"Usuario.id == {cls.__name__}.deleted_by_id"
        )
    
    # IP de origen (opcional)
    created_from_ip = Column(String(45))  # IPv6 = 45 caracteres
    updated_from_ip = Column(String(45))
    
    @property
    def esta_eliminado(self) -> bool:
        """¿Está marcado como eliminado?"""
        return self.deleted_at is not None
    
    def soft_delete(self, deleted_by_id: Optional[int] = None):
        """Marcar como eliminado (soft delete)"""
        self.deleted_at = datetime.utcnow()
        if deleted_by_id:
            self.deleted_by_id = deleted_by_id
    
    def restore(self):
        """Restaurar registro eliminado"""
        self.deleted_at = None
        self.deleted_by_id = None