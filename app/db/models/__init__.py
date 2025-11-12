from .base import Base
from .users import Usuario, Rol, usuario_rol
from .division_civil import ComunidadAutonoma, Provincia, Localidad
from .division_religiosa import Diocesis, DiocesisTitular
from .catalogos import (
    TipoInmueble, EstadoConservacion, EstadoTratamiento,
    TipoDocumento, TipoMimeDocumento, TipoAdquiriente,
    TipoTransmision, TipoCertificacionPropiedad,
    RolProfesional, ColegioProfesional, Administracion
)
from .proteccion import FiguraProteccion, InmuebleFiguraProteccion
from .documentos import Documento, InmuebleDocumento, ActuacionDocumento, TransmisionDocumento
from .inmuebles import Inmueble
from .agentes import Profesional, Colegiacion, RegistroPropiedad, Notaria, Notario, Adquiriente
from .historiales import Transmision, Actuacion, ActuacionParticipacion
from .historiografia import FuenteHistoriografica, CitaHistoriografica
from .subvenciones import ActuacionSubvencion, SubvencionAdministracion
from .extensiones_fuente import InmuebleOSMExt, InmuebleWDExt
