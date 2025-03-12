from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.gis.db.models import PointField
from django.core.validators import FileExtensionValidator


class ComunidadAutonoma(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name=_("Nombre"))

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = _("Comunidad Autónoma")
        verbose_name_plural = _("Comunidades Autónomas")


class Diocesis(models.Model):
    nombre = models.CharField(max_length=100, unique=True, blank=True, verbose_name=_("Nombre"))

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = _("Diócesis")
        verbose_name_plural = _("Diócesis")


class Documento(models.Model):
    fecha = models.DateField(verbose_name=_("Fecha del Documento"))
    tipo = models.ForeignKey(
        "TipoDocumento",
        on_delete=models.CASCADE,
        related_name="documentos",
        verbose_name=_("Tipo de Documento")
    )
    archivo = models.FileField(
        upload_to="documents/%Y/%m/%d/",
        validators=[FileExtensionValidator(allowed_extensions=["pdf", "txt", "doc", "docx", "odt", "rtf", "jpg", "mp4"])],
        null=True,
        blank=True,
        verbose_name=_("Archivo (PDF,Texto,Foto o Video)")
    )
    url = models.URLField(null=True, blank=True, verbose_name=_("URL del Documento (opcional)"))
    edificio = models.ForeignKey(
        "Edificio",
        on_delete=models.CASCADE,
        related_name="documentos_relacionados",  # Cambiamos el related_name para evitar conflictos
        verbose_name=_("Edificio"),
        null=True,  
        blank=True
    )
    grabado_por = models.ForeignKey(
        User,
        related_name="documentos_grabados",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        verbose_name=_("Grabado por")
    )
    fecha_grabacion = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_("Fecha de Grabación"))
    modificado_por = models.ForeignKey(
        User,
        related_name="documentos_modificados",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        verbose_name=_("Modificado por")
    )
    fecha_modificacion = models.DateTimeField(auto_now=True, editable=False, verbose_name=_("Fecha de Modificación"))

    def __str__(self):
        return f"{self.tipo.denominacion} - {self.fecha}"

    class Meta:
        verbose_name = _("Documento")
        verbose_name_plural = _("Documentos")
        indexes = [models.Index(fields=["fecha", "tipo"])]


class Edificio(models.Model):
    nombre = models.CharField(max_length=200, verbose_name=_("Nombre del Edificio"))
    comunidad_autonoma = models.ForeignKey(
        "ComunidadAutonoma",
        on_delete=models.CASCADE,
        related_name="edificios",
        verbose_name=_("Comunidad Autónoma")
    )
    provincia = models.ForeignKey(
        "Provincia",
        on_delete=models.CASCADE,
        related_name="edificios",
        verbose_name=_("Provincia")
    )
    municipio = models.CharField(max_length=100, verbose_name=_("Municipio"))
    diocesis = models.ForeignKey(
        "Diocesis",
        on_delete=models.CASCADE,
        related_name="edificios",
        verbose_name=_("Diócesis"),
        blank=True,
        null=True
    )
    direccion = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("Dirección"))
    coordenadas = PointField(blank=True, null=True, verbose_name=_("Coordenadas (lat, lon)"))
    referencia_catastral = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True,
        verbose_name=_("Referencia Catastral")
    )
    registro_propiedad = models.ForeignKey(
        "RegistroPropiedad",
        on_delete=models.CASCADE,
        related_name="edificios",
        verbose_name=_("Registro de Propiedad"),
        blank=True,
        null=True
    )
    numero_finca = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Número de Finca"))
    descripcion_registral = models.TextField(blank=True, null=True, verbose_name=_("Descripción Registral"))
    documentos = models.ManyToManyField(
        "Documento",
        related_name="edificios",
        blank=True,
        verbose_name=_("Documentos Asociados")
    )
    vendido = models.BooleanField(default=False, verbose_name=_("Vendido"))
    fecha_venta = models.DateField(null=True, blank=True, verbose_name=_("Fecha de Venta"))
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Precio (€)")
    )
    ciudad_venta = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Ciudad de Venta"))
    notario = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Notario"))
    incluye_bienes_muebles = models.BooleanField(default=False, verbose_name=_("Incluye Bienes Muebles"))
    grado_proteccion = models.ForeignKey(
        "GradoProteccion",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="edificios",
        verbose_name=_("Grado de Protección")
    )
    tipo_adquiriente = models.ForeignKey(
        "TipoAdquiriente",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="edificios",
        verbose_name=_("Tipo de Adquiriente")
    )
    observaciones = models.TextField(blank=True, null=True, verbose_name=_("Observaciones"))
    grabado_por = models.ForeignKey(
        User,
        related_name="edificios_grabados",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        verbose_name=_("Grabado por")
    )
    fecha_grabacion = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_("Fecha de Grabación"))
    modificado_por = models.ForeignKey(
        User,
        related_name="edificios_modificados",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        verbose_name=_("Modificado por")
    )
    fecha_modificacion = models.DateTimeField(auto_now=True, editable=False, verbose_name=_("Fecha de Modificación"))

    def __str__(self):
        return f"{self.municipio} - {self.direccion}" if self.direccion else f"{self.municipio}"

    class Meta:
        verbose_name = _("Edificio")
        verbose_name_plural = _("Edificios")


class GradoProteccion(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name=_("Nombre"))

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = _("Grado de Protección")
        verbose_name_plural = _("Grados de Protección")


class Provincia(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name=_("Nombre"))
    comunidad_autonoma = models.ForeignKey(
        "ComunidadAutonoma",
        on_delete=models.CASCADE,
        related_name="provincias",
        verbose_name=_("Comunidad Autónoma")
    )

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = _("Provincia")
        verbose_name_plural = _("Provincias")


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


class TipoAdquiriente(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name=_("Nombre"))

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = _("Tipo de Adquiriente")
        verbose_name_plural = _("Tipos de Adquirientes")


class TipoDocumento(models.Model):
    denominacion = models.CharField(max_length=100, unique=True, verbose_name=_("Denominación"))

    def __str__(self):
        return self.denominacion

    class Meta:
        verbose_name = _("Tipo de Documento")
        verbose_name_plural = _("Tipos de Documentos")