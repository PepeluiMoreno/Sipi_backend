from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    ComunidadAutonoma, Provincia, Diocesis, TipoDocumento, Documento, RegistroPropiedad,
    GradoProteccion, TipoAdquiriente, Edificio, Bibliografia, ReferenciaBibliografica
)
from .forms import EdificioForm


# Inline para Documento
class DocumentoInline(admin.TabularInline):
    model = Documento
    extra = 1
    fields = ("tipo", "fecha", "archivo", "url", "edificio")
    raw_id_fields = ("edificio",)


# Inline para ReferenciaBibliografica
class ReferenciaBibliograficaInline(admin.TabularInline):
    model = ReferenciaBibliografica
    extra = 1
    fields = ("bibliografia", "volumen", "paginas")
    raw_id_fields = ("bibliografia",)


@admin.register(Edificio)
class EdificioAdmin(admin.ModelAdmin):
    form = EdificioForm
    list_display = (
        "nombre", "municipio", "provincia", "comunidad_autonoma", "diocesis", "vendido", "desacralizado"
    )
    list_filter = ("provincia", "comunidad_autonoma", "vendido", "desacralizado")
    search_fields = ("nombre", "municipio", "direccion", "referencia_catastral")
    ordering = ("nombre",)
    fieldsets = (
        (_("Información General"), {
            "fields": (
                "nombre", "municipio", "provincia", "comunidad_autonoma", "diocesis", "direccion", "coordenadas_texto"
            )
        }),
        (_("Información Registral"), {
            "fields": (
                "referencia_catastral", "registro_propiedad", "descripcion_registral", "notario"
            )
        }),
        (_("Información Patrimonial"), {
            "fields": (
                "grado_proteccion", "incluye_bienes_muebles"
            )
        }),
        (_("Venta y Adquisición"), {
            "fields": (
                "tipo_adquiriente", "fecha_venta", "precio", "ciudad_venta", "numero_finca"
            )
        }),
        (_("Estado"), {
            "fields": (
                "vendido", "desacralizado"
            )
        }),
        (_("Observaciones"), {
            "fields": (
                "observaciones",
            )
        }),
    )
    inlines = [DocumentoInline, ReferenciaBibliograficaInline]  # Asegúrate de que esté aquí


# Registro de los demás modelos
@admin.register(ComunidadAutonoma)
class ComunidadAutonomaAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)


@admin.register(Provincia)
class ProvinciaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "comunidad_autonoma")
    list_filter = ("comunidad_autonoma",)
    search_fields = ("nombre",)


@admin.register(Diocesis)
class DiocesisAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)


@admin.register(TipoDocumento)
class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = ("denominacion",)
    search_fields = ("denominacion",)


@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ("tipo", "fecha", "edificio", "archivo", "url")
    search_fields = ("tipo__denominacion", "edificio__nombre")
    list_filter = ("tipo", "fecha")
    raw_id_fields = ("edificio",)


@admin.register(RegistroPropiedad)
class RegistroPropiedadAdmin(admin.ModelAdmin):
    list_display = ("nombre", "titular", "telefono", "correo_electronico")
    search_fields = ("nombre", "titular")
    list_filter = ("titular",)


@admin.register(GradoProteccion)
class GradoProteccionAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)


@admin.register(TipoAdquiriente)
class TipoAdquirienteAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)


@admin.register(Bibliografia)
class BibliografiaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "autor", "tipo_identificador", "identificador", "url")
    search_fields = ("titulo", "autor", "identificador")
    list_filter = ("tipo_identificador",)


@admin.register(ReferenciaBibliografica)
class ReferenciaBibliograficaAdmin(admin.ModelAdmin):
    list_display = ("bibliografia", "edificio", "volumen", "paginas")
    search_fields = ("bibliografia__titulo", "edificio__nombre")
    list_filter = ("edificio",)
    raw_id_fields = ("edificio", "bibliografia")


# Personalización del encabezado de Django Admin
admin.site.site_header = _("Administración del Patrimonio")
admin.site.site_title = _("Panel de Administración")
admin.site.index_title = _("Gestión de Datos")