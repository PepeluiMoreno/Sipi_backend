from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.gis.db.models import PointField
from django.core.validators import FileExtensionValidator


class ComunidadAutonoma(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name=_("Comunidad Autónoma"))

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = _("Comunidad Autónoma")
        verbose_name_plural = _("Comunidades Autónomas")


class Provincia(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name=_("Provincia"))
    comunidad_autonoma = models.ForeignKey(
        ComunidadAutonoma,
        on_delete=models.CASCADE,
        related_name="provincias",
        verbose_name=_("Comunidad Autónoma")
    )

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = _("Provincia")
        verbose_name_plural = _("Provincias")


class Diocesis(models.Model):
    nombre = models.CharField(max_length=100, unique=True, blank=True, verbose_name=_("Diócesis"))

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = _("Diócesis")
        verbose_name_plural = _("Diócesis")


class TipoDocumento(models.Model):
    denominacion = models.CharField(max_length=100, unique=True, verbose_name=_("Denominación"))

    def __str__(self):
        return self.denominacion

    class Meta:
        verbose_name = _("Tipo de Documento")
        verbose_name_plural = _("Tipos de Documentos")


class Documento(models.Model):
    fecha = models.DateField(verbose_name=_("Fecha del Documento"))
    tipo = models.ForeignKey(
        TipoDocumento,
        on_delete=models.CASCADE,
        related_name="documentos",
        verbose_name=_("Tipo de Documento")
    )
    archivo = models.FileField(
        upload_to="documents/%Y/%m/%d/",
        validators=[FileExtensionValidator(allowed_extensions=["pdf", "txt", "doc", "docx", "odt", "rtf", "jpg", "mp4"])],
        null=True,
        blank=True,
        verbose_name=_("Archivo (PDF, Texto, Foto o Video)")
    )
    url = models.URLField(null=True, blank=True, verbose_name=_("URL del Documento (opcional)"))
    edificio = models.ForeignKey(
        "Edificio",
        on_delete=models.CASCADE,
        related_name="documentos_relacionados",
        verbose_name=_("Edificio"),
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.tipo.denominacion} - {self.fecha}"

    class Meta:
        verbose_name = _("Documento")
        verbose_name_plural = _("Documentos")
        indexes = [models.Index(fields=["fecha", "tipo"])]


class RegistroPropiedad(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name=_("Nombre"))
    titular = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("Titular"))
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Teléfono"))
    correo_electronico = models.EmailField(blank=True, null=True, verbose_name=_("Correo Electrónico"))

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = _("Registro de Propiedad")
        verbose_name_plural = _("Registros de Propiedad")


class GradoProteccion(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name=_("Grado de Protección"))

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = _("Grado de Protección")
        verbose_name_plural = _("Grados de Protección")


class TipoAdquiriente(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name=_("Tipo de Adquiriente"))

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = _("Tipo de Adquiriente")
        verbose_name_plural = _("Tipos de Adquirientes")


class Edificio(models.Model):
    nombre = models.CharField(max_length=200, verbose_name=_("Nombre del Edificio"))
    comunidad_autonoma = models.ForeignKey(
        ComunidadAutonoma,
        on_delete=models.CASCADE,
        related_name="edificios",
        verbose_name=_("Comunidad Autónoma")
    )
    provincia = models.ForeignKey(
        Provincia,
        on_delete=models.CASCADE,
        related_name="edificios",
        verbose_name=_("Provincia")
    )
    municipio = models.CharField(max_length=100, verbose_name=_("Municipio"))
    diocesis = models.ForeignKey(
        Diocesis,
        on_delete=models.CASCADE,
        related_name="edificios",
        verbose_name=_("Diócesis"),
        blank=True,
        null=True
    )
    direccion = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("Dirección"))
    coordenadas = PointField(geography=True, blank=True, null=True, verbose_name=_("Coordenadas Geográficas"))
    
    
    referencia_catastral = models.CharField(
        max_length=20, unique=True, blank=True, null=True, verbose_name=_("Referencia Catastral")
    )
    
    registro_propiedad = models.ForeignKey(
        RegistroPropiedad,
        on_delete=models.CASCADE,
        related_name="edificios",
        verbose_name=_("Registro de Propiedad"),
        blank=True,
        null=True
    )
    
    descripcion_registral = models.TextField(blank=True, null=True, verbose_name=_("Descripción Registral"))
    fecha_venta = models.DateField(blank=True, null=True, verbose_name=_("Fecha de Venta"))
    precio = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name=_("Precio de Venta"))
    ciudad_venta = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Ciudad de Venta"))
    numero_finca = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Número de Finca"))
    notario = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Notario"))
    
    
    grado_proteccion = models.ForeignKey(
        GradoProteccion,
        on_delete=models.SET_NULL,
        related_name="edificios",
        verbose_name=_("Grado de Protección"),
        blank=True,
        null=True
    )
    tipo_adquiriente = models.ForeignKey(
        TipoAdquiriente,
        on_delete=models.SET_NULL,
        related_name="edificios",
        verbose_name=_("Tipo de Adquiriente"),
        blank=True,
        null=True
    )
    incluye_bienes_muebles =  models.BooleanField(default=False, verbose_name=_("Incluye Bienes Muebles"))
    desacralizado = models.BooleanField(default=False, verbose_name=_("Desacralizado"))
    vendido = models.BooleanField(default=False, verbose_name=_("Vendido"))
    observaciones = models.TextField(blank=True, null=True, verbose_name=_("Observaciones"))
    
    def __str__(self):
        return f"{self.municipio} - {self.direccion}" if self.direccion else f"{self.municipio}"

    class Meta:
        verbose_name = _("Edificio")
        verbose_name_plural = _("Edificios")


# NUEVOS MODELOS PARA BIBLIOGRAFÍA Y REFERENCIAS

class Bibliografia(models.Model):
    TIPO_IDENTIFICADOR_CHOICES = [
        ('ISBN', 'ISBN'),
        ('DOI', 'DOI'),
        ('ISSN', 'ISSN'),
    ]

    titulo = models.CharField(max_length=255, verbose_name=_("Título"))
    autor = models.CharField(max_length=255, verbose_name=_("Autor(es)"))
    tipo_identificador = models.CharField(
        max_length=10, choices=TIPO_IDENTIFICADOR_CHOICES, verbose_name=_("Tipo de Identificador")
    )
    identificador = models.CharField(max_length=100, unique=True, verbose_name=_("Identificador"))
    url = models.URLField(blank=True, null=True, verbose_name=_("URL"))

    def __str__(self):
        return f"{self.titulo} - {self.autor}"

    class Meta:
        verbose_name = _("Bibliografía")
        verbose_name_plural = _("Bibliografías")


class ReferenciaBibliografica(models.Model):
    edificio = models.ForeignKey(
        Edificio, on_delete=models.CASCADE, related_name="referencias_bibliograficas", verbose_name=_("Edificio")
    )
    bibliografia = models.ForeignKey(
        Bibliografia, on_delete=models.CASCADE, related_name="referencias", verbose_name=_("Bibliografía")
    )
    volumen = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Volumen"))
    paginas = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Intervalo de Páginas"))

    def __str__(self):
        return f"{self.bibliografia.titulo} - {self.edificio.nombre}"

    class Meta:
        verbose_name = _("Referencia Bibliográfica")
        verbose_name_plural = _("Referencias Bibliográficas")

