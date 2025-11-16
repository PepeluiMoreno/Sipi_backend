# app/db/mixins/__init__.py
from .base import UUIDPKMixin, AuditMixin
from .identificacion import TipoIdentificacion, IdentificacionMixin
from .contacto import ContactoMixin, ContactoDireccionMixin
from .direccion import TipoVia, DireccionMixin, DireccionGeoMixin

__all__ = [
    'UUIDPKMixin',
    'AuditMixin',
    'TipoIdentificacion',
    'IdentificacionMixin',
    'ContactoMixin',
    'ContactoDireccionMixin',
    'TipoVia',
    'DireccionMixin',
    'DireccionGeoMixin'
]