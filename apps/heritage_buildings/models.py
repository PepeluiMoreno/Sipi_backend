# heritage_defense/apps/heritage_buildings/models.py

from django.db import models
from django.contrib.auth.models import User
class ComunidadAutonoma(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Provincia(models.Model):
    nombre = models.CharField(max_length=100)
    comunidad_autonoma = models.ForeignKey(ComunidadAutonoma, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Diocesis(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class RegistroPropiedad(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class TipoDocument(models.Model):
    denominacion = models.CharField(max_length=100)

    def __str__(self):
        return self.denominacion

class document(models.Model):
    fecha = models.DateField()
    tipo = models.ForeignKey(TipoDocument, on_delete=models.CASCADE)
    url = models.URLField()
    grabado_por = models.ForeignKey(User, related_name='documents_grabados', on_delete=models.SET_NULL, null=True)
    fecha_grabacion = models.DateTimeField(auto_now_add=True)
    modificado_por = models.ForeignKey(User, related_name='documents_modificados', on_delete=models.SET_NULL, null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tipo.denominacion} - {self.fecha}"

class building(models.Model):
    comunidad_autonoma = models.ForeignKey(ComunidadAutonoma, on_delete=models.CASCADE)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    municipio = models.CharField(max_length=100)
    diocesis = models.ForeignKey(Diocesis, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=200)
    coordenadas = models.CharField(max_length=50)
    referencia_catastral = models.CharField(max_length=20)
    registro_propiedad = models.ForeignKey(RegistroPropiedad, on_delete=models.CASCADE)
    numero_finca = models.CharField(max_length=20)
    descripcion_registral = models.TextField()
    documents = models.ManyToManyField(document)
    vendido = models.BooleanField(default=False)
    fecha_venta = models.DateField(null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ciudad_venta = models.CharField(max_length=100, null=True, blank=True)
    notario = models.CharField(max_length=100, null=True, blank=True)
    incluye_bienes_muebles = models.BooleanField(default=False)
    grado_proteccion = models.CharField(max_length=100, blank=True, verbose_name="Grado de Protección")
    tipo_adquiriente = models.CharField(max_length=100, blank=True, verbose_name="Tipo de Adquiriente")
    observaciones = models.TextField(blank=True)
    grabado_por = models.ForeignKey(User, related_name='buildings_grabados', on_delete=models.SET_NULL, null=True)
    fecha_grabacion = models.DateTimeField(auto_now_add=True)
    modificado_por = models.ForeignKey(User, related_name='buildings_modificados', on_delete=models.SET_NULL, null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.municipio} - {self.direccion}"