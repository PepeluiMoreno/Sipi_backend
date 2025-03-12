from django.contrib import admin
from django import forms
from django.contrib.gis.geos import Point
from .models import (
    ComunidadAutonoma, Provincia, Diocesis, RegistroPropiedad,
    TipoDocumento, Documento, GradoProteccion, TipoAdquiriente, Edificio
)
from .models import Edificio
from .forms import EdificioForm
# Inlines para los modelos relacionados

class ProvinciaInline(admin.TabularInline):
    model = Provincia
    extra = 1
    fields = ('nombre',)

class EdificioInline(admin.TabularInline):
    model = Edificio
    extra = 1
    fields = ('nombre', 'municipio', 'direccion')

class DocumentoInline(admin.TabularInline):
    model = Documento
    extra = 1
    fields = ('fecha', 'tipo', 'archivo', 'url')



class ComunidadAutonomaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    inlines = [ProvinciaInline]

class ProvinciaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'comunidad_autonoma')
    search_fields = ('nombre', 'comunidad_autonoma__nombre')
    list_filter = ('comunidad_autonoma',)
    inlines = [EdificioInline]

class DiocesisAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    inlines = [EdificioInline]

class RegistroPropiedadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'titular', 'telefono')
    search_fields = ('nombre', 'titular')
    inlines = [EdificioInline]

class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = ('denominacion',)
    search_fields = ('denominacion',)
    inlines = [DocumentoInline]

class GradoProteccionAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    inlines = [EdificioInline]

class TipoAdquirienteAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    inlines = [EdificioInline]


class EdificioAdmin(admin.ModelAdmin):
    form = EdificioForm  # Usar el formulario personalizado
    list_display = ('nombre', 'municipio', 'provincia', 'comunidad_autonoma')
    search_fields = ('nombre', 'municipio', 'provincia__nombre', 'comunidad_autonoma__nombre')
    list_filter = ('comunidad_autonoma', 'provincia')
    # Especificar explícitamente los campos que queremos en el formulario
    fields = [
        'nombre', 'municipio', 'provincia', 'comunidad_autonoma', 'direccion', 
        'descripcion_registral', 'referencia_catastral', 'numero_finca', 'registro_propiedad', 
        'diocesis', 'grado_proteccion', 'incluye_bienes_muebles', 'vendido', 'tipo_adquiriente', 
        'fecha_venta', 'ciudad_venta', 'precio', 'notario', 'observaciones', 'coordenadas_texto'
    ]
    inlines = [DocumentoInline]

class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'tipo', 'edificio')
    search_fields = ('tipo__denominacion', 'edificio__nombre')
    list_filter = ('tipo', 'edificio')

# Registrar los modelos en el admin

admin.site.register(ComunidadAutonoma, ComunidadAutonomaAdmin)
admin.site.register(Provincia, ProvinciaAdmin)
admin.site.register(Diocesis, DiocesisAdmin)
admin.site.register(RegistroPropiedad, RegistroPropiedadAdmin)
admin.site.register(TipoDocumento, TipoDocumentoAdmin)
admin.site.register(GradoProteccion, GradoProteccionAdmin)
admin.site.register(TipoAdquiriente, TipoAdquirienteAdmin)
admin.site.register(Edificio,EdificioAdmin)
admin.site.register(Documento, DocumentoAdmin)