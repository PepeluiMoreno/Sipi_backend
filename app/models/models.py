# models.py 
from __future__ import annotations
from typing import Optional, List
from sqlalchemy import String, Integer, ForeignKey, Boolean, Date, Numeric, Text, UniqueConstraint, CheckConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from geoalchemy2 import Geometry
from app.db.base import Base

# Territorio
class ComunidadAutonoma(Base):
    __tablename__ = "comunidad_autonoma"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    provincias: Mapped[List["Provincia"]] = relationship(back_populates="comunidad_autonoma", cascade="all, delete-orphan")

class Provincia(Base):
    __tablename__ = "provincia"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    comunidad_autonoma_id: Mapped[int] = mapped_column(ForeignKey("comunidad_autonoma.id"), index=True)
    comunidad_autonoma: Mapped["ComunidadAutonoma"] = relationship(back_populates="provincias")
    inmuebles: Mapped[List["Inmueble"]] = relationship(back_populates="provincia")

class Diocesis(Base):
    __tablename__ = "diocesis"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    inmuebles: Mapped[List["Inmueble"]] = relationship(back_populates="diocesis")

# Catálogos
class RegistroPropiedad(Base):
    __tablename__ = "registro_propiedad"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    titular: Mapped[Optional[str]] = mapped_column(String(200))
    telefono: Mapped[Optional[str]] = mapped_column(String(50))
    correo_electronico: Mapped[Optional[str]] = mapped_column(String(255))
    inmuebles: Mapped[List["Inmueble"]] = relationship(back_populates="registro_propiedad")

class GradoProteccion(Base):
    __tablename__ = "grado_proteccion"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    inmuebles: Mapped[List["Inmueble"]] = relationship(back_populates="grado_proteccion")

class TipoAdquiriente(Base):
    __tablename__ = "tipo_adquiriente"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    adquirientes: Mapped[List["Adquiriente"]] = relationship(back_populates="tipo_adquiriente")

class TipoDocumento(Base):
    __tablename__ = "tipo_documento"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    denominacion: Mapped[str] = mapped_column(String(100), unique=True)
    documentos: Mapped[List["Documento"]] = relationship(back_populates="tipo")

class ColegioProfesional(Base):
    __tablename__ = "colegio_profesional"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    ambito: Mapped[Optional[str]] = mapped_column(String(50))
    comunidad_autonoma: Mapped[Optional[str]] = mapped_column(String(100))
    provincia: Mapped[Optional[str]] = mapped_column(String(100))
    url: Mapped[Optional[str]] = mapped_column(String(255))
    colegiados: Mapped[List["ProfesionalColegiacion"]] = relationship(back_populates="colegio")

class RolProfesional(Base):
    __tablename__ = "rol_profesional"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True)
    participaciones: Mapped[List["ActuacionParticipacion"]] = relationship(back_populates="rol")

# Documentos (metadatos)
class Documento(Base):
    __tablename__ = "documento"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fecha: Mapped[Optional[Date]] = mapped_column(Date)
    tipo_id: Mapped[int] = mapped_column(ForeignKey("tipo_documento.id"), index=True)
    tipo: Mapped["TipoDocumento"] = relationship(back_populates="documentos")
    archivo: Mapped[Optional[str]] = mapped_column(String)
    url: Mapped[Optional[str]] = mapped_column(String)
    inmuebles_rel: Mapped[List["InmuebleDocumento"]] = relationship(back_populates="documento", cascade="all, delete-orphan")
    transmisiones_rel: Mapped[List["TransmisionDocumento"]] = relationship(back_populates="documento", cascade="all, delete-orphan")

# Inmueble (antes Edificio)
class Inmueble(Base):
    __tablename__ = "inmueble"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(200))
    comunidad_autonoma_id: Mapped[int] = mapped_column(ForeignKey("comunidad_autonoma.id"), index=True)
    provincia_id: Mapped[int] = mapped_column(ForeignKey("provincia.id"), index=True)
    municipio: Mapped[str] = mapped_column(String(100))
    diocesis_id: Mapped[Optional[int]] = mapped_column(ForeignKey("diocesis.id"))
    direccion: Mapped[Optional[str]] = mapped_column(String(200))
    coordenadas = mapped_column(Geometry(geometry_type="POINT", srid=4326, spatial_index=True))
    referencia_catastral: Mapped[Optional[str]] = mapped_column(String(20), unique=True)
    registro_propiedad_id: Mapped[Optional[int]] = mapped_column(ForeignKey("registro_propiedad.id"))
    numero_finca: Mapped[Optional[str]] = mapped_column(String(50))
    descripcion_registral: Mapped[Optional[str]] = mapped_column(Text)
    vendido: Mapped[bool] = mapped_column(Boolean, default=False)
    fecha_venta: Mapped[Optional[Date]] = mapped_column(Date)
    precio: Mapped[Optional[Numeric]] = mapped_column(Numeric(12, 2))
    ciudad_venta: Mapped[Optional[str]] = mapped_column(String(255))
    notario: Mapped[Optional[str]] = mapped_column(String(255))
    incluye_bienes_muebles: Mapped[bool] = mapped_column(Boolean, default=False)
    grado_proteccion_id: Mapped[Optional[int]] = mapped_column(ForeignKey("grado_proteccion.id"))
    tipo_adquiriente_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tipo_adquiriente.id"))
    observaciones: Mapped[Optional[str]] = mapped_column(Text)

    provincia: Mapped["Provincia"] = relationship(back_populates="inmuebles")
    comunidad_autonoma: Mapped["ComunidadAutonoma"] = relationship()
    diocesis: Mapped[Optional["Diocesis"]] = relationship(back_populates="inmuebles")
    registro_propiedad: Mapped[Optional["RegistroPropiedad"]] = relationship(back_populates="inmuebles")
    grado_proteccion: Mapped[Optional["GradoProteccion"]] = relationship(back_populates="inmuebles")
    tipo_adquiriente: Mapped[Optional["TipoAdquiriente"]] = relationship(back_populates="adquirientes")

    documentos_rel: Mapped[List["InmuebleDocumento"]] = relationship(back_populates="inmueble", cascade="all, delete-orphan")
    transmisiones: Mapped[List["Transmision"]] = relationship(back_populates="inmueble", cascade="all, delete-orphan")
    actuaciones: Mapped[List["Actuacion"]] = relationship(back_populates="inmueble", cascade="all, delete-orphan")
    referencias_bibliograficas: Mapped[List["ReferenciaBibliografica"]] = relationship(back_populates="inmueble", cascade="all, delete-orphan")

    __table_args__ = (Index("ix_inmueble_prov_mun", "provincia_id", "municipio"), )

class InmuebleDocumento(Base):
    __tablename__ = "inmueble_documento"
    inmueble_id: Mapped[int] = mapped_column(ForeignKey("inmueble.id"), primary_key=True)
    documento_id: Mapped[int] = mapped_column(ForeignKey("documento.id"), primary_key=True)
    inmueble: Mapped["Inmueble"] = relationship(back_populates="documentos_rel")
    documento: Mapped["Documento"] = relationship(back_populates="inmuebles_rel")

# Transmisión y Adquiriente
class Adquiriente(Base):
    __tablename__ = "adquiriente"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(255), index=True)
    tipo_adquiriente_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tipo_adquiriente.id"))
    nif_cif: Mapped[Optional[str]] = mapped_column(String(32))
    representante: Mapped[Optional[str]] = mapped_column(String(255))
    email: Mapped[Optional[str]] = mapped_column(String(255))
    telefono: Mapped[Optional[str]] = mapped_column(String(50))
    direccion: Mapped[Optional[str]] = mapped_column(String(255))
    tipo_adquiriente: Mapped[Optional["TipoAdquiriente"]] = relationship(back_populates="adquirientes")
    transmisiones: Mapped[List["Transmision"]] = relationship(back_populates="adquiriente")

class Transmision(Base):
    __tablename__ = "transmision"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    inmueble_id: Mapped[int] = mapped_column(ForeignKey("inmueble.id"), index=True)
    tipo: Mapped[str] = mapped_column(String(20))
    fecha: Mapped[Optional[Date]] = mapped_column(Date)
    ciudad: Mapped[Optional[str]] = mapped_column(String(255))
    notario: Mapped[Optional[str]] = mapped_column(String(255))
    precio: Mapped[Optional[Numeric]] = mapped_column(Numeric(12, 2))
    adquiriente_id: Mapped[int] = mapped_column(ForeignKey("adquiriente.id"), index=True)
    observaciones: Mapped[Optional[str]] = mapped_column(Text)
    inmueble: Mapped["Inmueble"] = relationship(back_populates="transmisiones")
    adquiriente: Mapped["Adquiriente"] = relationship(back_populates="transmisiones")
    documentos_rel: Mapped[List["TransmisionDocumento"]] = relationship(back_populates="transmision", cascade="all, delete-orphan")
    __table_args__ = (Index("ix_transmision_tipo_fecha", "tipo", "fecha"), )

class TransmisionDocumento(Base):
    __tablename__ = "transmision_documento"
    transmision_id: Mapped[int] = mapped_column(ForeignKey("transmision.id"), primary_key=True)
    documento_id: Mapped[int] = mapped_column(ForeignKey("documento.id"), primary_key=True)
    transmision: Mapped["Transmision"] = relationship(back_populates="documentos_rel")
    documento: Mapped["Documento"] = relationship(back_populates="transmisiones_rel")

# Actuaciones (metadatos, sin carga automática por ahora)
class Actuacion(Base):
    __tablename__ = "actuacion"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    inmueble_id: Mapped[int] = mapped_column(ForeignKey("inmueble.id"), index=True)
    tipo: Mapped[str] = mapped_column(String(30))
    titulo: Mapped[Optional[str]] = mapped_column(String(255))
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    organismo_responsable: Mapped[Optional[str]] = mapped_column(String(255))
    fecha_inicio: Mapped[Optional[Date]] = mapped_column(Date)
    fecha_fin: Mapped[Optional[Date]] = mapped_column(Date)
    importe_total: Mapped[Optional[Numeric]] = mapped_column(Numeric(12, 2))
    inmueble: Mapped["Inmueble"] = relationship(back_populates="actuaciones")
    fotos_antes_rel: Mapped[List["ActuacionFotoAntes"]] = relationship(back_populates="actuacion", cascade="all, delete-orphan")
    fotos_despues_rel: Mapped[List["ActuacionFotoDespues"]] = relationship(back_populates="actuacion", cascade="all, delete-orphan")
    participaciones: Mapped[List["ActuacionParticipacion"]] = relationship(back_populates="actuacion", cascade="all, delete-orphan")

class ActuacionFotoAntes(Base):
    __tablename__ = "actuacion_foto_antes"
    actuacion_id: Mapped[int] = mapped_column(ForeignKey("actuacion.id"), primary_key=True)
    documento_id: Mapped[int] = mapped_column(ForeignKey("documento.id"), primary_key=True)
    actuacion: Mapped["Actuacion"] = relationship(back_populates="fotos_antes_rel")
    documento: Mapped["Documento"] = relationship()

class ActuacionFotoDespues(Base):
    __tablename__ = "actuacion_foto_despues"
    actuacion_id: Mapped[int] = mapped_column(ForeignKey("actuacion.id"), primary_key=True)
    documento_id: Mapped[int] = mapped_column(ForeignKey("documento.id"), primary_key=True)
    actuacion: Mapped["Actuacion"] = relationship(back_populates="fotos_despues_rel")
    documento: Mapped["Documento"] = relationship()

# Profesionales
class Profesional(Base):
    __tablename__ = "profesional"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(255), index=True)
    telefono: Mapped[Optional[str]] = mapped_column(String(50))
    correo_electronico: Mapped[Optional[str]] = mapped_column(String(255))
    direccion_profesional: Mapped[Optional[str]] = mapped_column(String(255))
    colegiaciones: Mapped[List["ProfesionalColegiacion"]] = relationship(back_populates="profesional", cascade="all, delete-orphan")
    participaciones: Mapped[List["ActuacionParticipacion"]] = relationship(back_populates="profesional", cascade="all, delete-orphan")

class ProfesionalColegiacion(Base):
    __tablename__ = "profesional_colegiacion"
    profesional_id: Mapped[int] = mapped_column(ForeignKey("profesional.id"), primary_key=True)
    colegio_id: Mapped[int] = mapped_column(ForeignKey("colegio_profesional.id"), primary_key=True)
    numero_colegiado: Mapped[Optional[str]] = mapped_column(String(100))
    profesional: Mapped["Profesional"] = relationship(back_populates="colegiaciones")
    colegio: Mapped["ColegioProfesional"] = relationship(back_populates="colegiados")

class ActuacionParticipacion(Base):
    __tablename__ = "actuacion_participacion"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    actuacion_id: Mapped[int] = mapped_column(ForeignKey("actuacion.id"), index=True)
    profesional_id: Mapped[int] = mapped_column(ForeignKey("profesional.id"), index=True)
    rol_id: Mapped[int] = mapped_column(ForeignKey("rol_profesional.id"), index=True)
    colegio_nombre: Mapped[Optional[str]] = mapped_column(String(255))
    numero_colegiado: Mapped[Optional[str]] = mapped_column(String(100))
    fecha_inicio: Mapped[Optional[Date]] = mapped_column(Date)
    fecha_fin: Mapped[Optional[Date]] = mapped_column(Date)
    observaciones: Mapped[Optional[str]] = mapped_column(Text)
    actuacion: Mapped["Actuacion"] = relationship(back_populates="participaciones")
    profesional: Mapped["Profesional"] = relationship(back_populates="participaciones")
    rol: Mapped["RolProfesional"] = relationship(back_populates="participaciones")
    __table_args__ = (UniqueConstraint("actuacion_id", "profesional_id", "rol_id", name="uq_participacion_act_prof_rol"), )

# Bibliografía
class Bibliografia(Base):
    __tablename__ = "bibliografia"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    titulo: Mapped[str] = mapped_column(String(300))
    autores: Mapped[str] = mapped_column(Text)
    tipo_identificador: Mapped[str] = mapped_column(String(10))
    identificador: Mapped[str] = mapped_column(String(100), unique=True)
    url: Mapped[Optional[str]] = mapped_column(String(255))
    referencias: Mapped[List["ReferenciaBibliografica"]] = relationship(back_populates="bibliografia", cascade="all, delete-orphan")
    __table_args__ = (Index("ix_biblio_identificador", "tipo_identificador", "identificador"), )

class ReferenciaBibliografica(Base):
    __tablename__ = "referencia_bibliografica"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    inmueble_id: Mapped[int] = mapped_column(ForeignKey("inmueble.id"), index=True)
    bibliografia_id: Mapped[int] = mapped_column(ForeignKey("bibliografia.id"), index=True)
    volumen: Mapped[Optional[str]] = mapped_column(String(50))
    paginas: Mapped[Optional[str]] = mapped_column(String(50))
    inmueble: Mapped["Inmueble"] = relationship(back_populates="referencias_bibliograficas")
    bibliografia: Mapped["Bibliografia"] = relationship(back_populates="referencias")
    __table_args__ = (UniqueConstraint("inmueble_id", "bibliografia_id", "volumen", "paginas", name="uq_ref_biblio"), )
