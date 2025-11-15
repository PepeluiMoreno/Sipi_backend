# models/__init__.py
from .base import Base, UUIDPKMixin, AuditMixin
from .agentes import (
    Adquiriente, Administracion, AdministracionTitular, AgenciaInmobiliaria, AgenciaInmobiliariaTitular,
    ColegioProfesional, Diocesis, DiocesisTitular, Notaria, NotariaTitular,
    Tecnico, RegistroPropiedad, RegistroTitular, Transmitente
)
from .catalogos import (
    EstadoConservacion, EstadoTratamiento, FigurasProteccion, RolTecnico,
    TipoCertificacionPropiedad, TipoDocumento, TipoInmueble, TipoMimeDocumento,
    TipoPersona, TipoTransmision
)
from .geografia import ComunidadAutonoma, Provincia, Localidad
from .documentos import Documento, InmuebleDocumento, ActuacionDocumento, TransmisionDocumento
from .actuaciones import Actuacion, ActuacionTecnicos
from .transmisiones import Transmision, Inmatriculacion, TransmisionAnunciantes
from .inmuebles import Inmueble, InmuebleOSMExt, InmuebleWDExt

__all__ = [
    'Base', 'UUIDPKMixin', 'AuditMixin',
    'Adquiriente', 'Administracion', 'AdministracionTitular', 'AgenciaInmobiliaria', 'AgenciaInmobiliariaTitular',
    'ColegioProfesional', 'Diocesis', 'DiocesisTitular', 'Notaria', 'NotariaTitular',
    'Tecnico', 'RegistroPropiedad', 'RegistroTitular', 'Transmitente',
    'EstadoConservacion', 'EstadoTratamiento', 'FigurasProteccion', 'RolTecnico',
    'TipoCertificacionPropiedad', 'TipoDocumento', 'TipoInmueble', 'TipoMimeDocumento',
    'TipoPersona', 'TipoTransmision',
    'ComunidadAutonoma', 'Provincia', 'Localidad',
    'Documento', 'InmuebleDocumento', 'ActuacionDocumento', 'TransmisionDocumento',
    'Actuacion', 'ActuacionTecnicos',
    'Transmision', 'Inmatriculacion', 'TransmisionAnunciantes',
    'Inmueble', 'InmuebleOSMExt', 'InmuebleWDExt'
]