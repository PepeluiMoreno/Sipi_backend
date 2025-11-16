# app/db/mixins/direccion.py
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.geografia import Provincia, Localidad, ComunidadAutonoma
    from app.db.models.catalogos import TipoVia

class DireccionMixin:
    # Tipo de vía como relación a catálogo
    tipo_via_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("tipos_via.id"), nullable=True, index=True
    )
    nombre_via: Mapped[str | None] = mapped_column(String(255), nullable=True)
    numero: Mapped[str | None] = mapped_column(String(10), nullable=True)
    bloque: Mapped[str | None] = mapped_column(String(10), nullable=True)
    escalera: Mapped[str | None] = mapped_column(String(10), nullable=True)
    piso: Mapped[str | None] = mapped_column(String(10), nullable=True)
    puerta: Mapped[str | None] = mapped_column(String(10), nullable=True)
    
    # Eliminado: direccion_completa (ahora es propiedad calculada)
    codigo_postal: Mapped[str | None] = mapped_column(String(10), nullable=True, index=True)
    
    # Coordenadas geográficas
    latitud: Mapped[float | None] = mapped_column(nullable=True)
    longitud: Mapped[float | None] = mapped_column(nullable=True)
    
    # Relaciones geográficas
    comunidad_autonoma_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("comunidades_autonomas.id"), nullable=True, index=True
    )
    provincia_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("provincias.id"), nullable=True, index=True
    )
    localidad_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("localidades.id"), nullable=True, index=True
    )
    
    # Relaciones (solo para TYPE_CHECKING)
    if TYPE_CHECKING:
        tipo_via: Mapped["TipoVia | None"]
        comunidad_autonoma: Mapped["ComunidadAutonoma | None"]
        provincia: Mapped["Provincia | None"] 
        localidad: Mapped["Localidad | None"]
    
    @property
    def direccion_completa(self) -> str:
        """Dirección completa calculada automáticamente"""
        partes = []
        
        # Tipo de vía y nombre
        if self.tipo_via and self.nombre_via:
            partes.append(f"{self.tipo_via.nombre} {self.nombre_via}")
        elif self.nombre_via:
            partes.append(self.nombre_via)
        
        # Número
        if self.numero:
            partes.append(self.numero)
        
        # Bloque, escalera, piso, puerta
        detalles = []
        if self.bloque:
            detalles.append(f"Bloque {self.bloque}")
        if self.escalera:
            detalles.append(f"Esc. {self.escalera}")
        if self.piso:
            detalles.append(f"{self.piso}º")
        if self.puerta:
            detalles.append(self.puerta)
        
        if detalles:
            partes.append(", ".join(detalles))
        
        # Código postal y localidad
        if self.codigo_postal and self.localidad:
            partes.append(f"{self.codigo_postal} {self.localidad.nombre}")
        elif self.codigo_postal:
            partes.append(self.codigo_postal)
        elif self.localidad:
            partes.append(self.localidad.nombre)
        
        return ", ".join(partes) if partes else ""
    
    @property
    def direccion_corta(self) -> str:
        """Dirección corta (tipo vía + nombre + número)"""
        partes = []
        if self.tipo_via and self.nombre_via:
            partes.append(f"{self.tipo_via.nombre} {self.nombre_via}")
        if self.numero:
            partes.append(self.numero)
        return " ".join(partes) if partes else ""