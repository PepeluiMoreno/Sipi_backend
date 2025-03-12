# heritage_defense/apps/heritage_buildings/forms.py

from django import forms
from .models import Edificio, Documento
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

class EdificioForm(forms.ModelForm):
    coordenadas_texto = forms.CharField(
        label="Coordenadas (lat, lon)",
        required=False,
        help_text="Ingrese las coordenadas en formato 'latitud, longitud'. Ejemplo: 40.4168, -3.7038"
    )

    class Meta:
        model = Edificio
        fields = '__all__'  # Incluye todos los campos
        exclude = ['coordenadas']  # Excluye explícitamente el campo 'coordenadas'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si hay coordenadas en la instancia, mostrarlas como texto
        if self.instance and self.instance.coordenadas:
            self.initial['coordenadas_texto'] = f"{self.instance.coordenadas.y}, {self.instance.coordenadas.x}"

    def clean_coordenadas_texto(self):
        """Convierte el texto de coordenadas en un objeto Point."""
        coordenadas_texto = self.cleaned_data.get('coordenadas_texto')
        if coordenadas_texto:
            try:
                lat, lon = map(float, coordenadas_texto.split(','))
                return Point(lon, lat)  # Point espera (longitud, latitud)
            except (ValueError, AttributeError):
                raise forms.ValidationError("Formato inválido. Use 'latitud, longitud'.")
        return None

    def save(self, commit=True):
        """Guarda las coordenadas como un objeto Point."""
        instance = super().save(commit=False)
        coordenadas = self.clean_coordenadas_texto()  # Obtener el Point validado
        instance.coordenadas = coordenadas
        if commit:
            instance.save()
        return instance

class BuildingForm(forms.ModelForm):
    class Meta:
        model = Edificio
        exclude = ['grabado_por', 'fecha_grabacion', 'modificado_por', 'fecha_modificacion']
        widgets = {
            'fecha_venta': forms.DateInput(attrs={'type': 'date', 'class': 'form-input mt-1 block w-full'}),
            'descripcion_registral': forms.Textarea(attrs={'rows': 4, 'class': 'form-textarea mt-1 block w-full'}),
            'precio': forms.NumberInput(attrs={'class': 'form-input mt-1 block w-full'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('comunidad_autonoma', css_class='w-full md:w-1/2 px-2'),
                Column('provincia', css_class='w-full md:w-1/2 px-2'),
            ),
            Row(
                Column('municipio', css_class='w-full md:w-1/2 px-2'),
                Column('diocesis', css_class='w-full md:w-1/2 px-2'),
            ),
            'direccion',
            'coordenadas',
            'referencia_catastral',
            'registro_propiedad',
            'numero_finca',
            'descripcion_registral',
            'documents',
            Row(
                Column('vendido', css_class='w-full md:w-1/2 px-2'),
                Column('fecha_venta', css_class='w-full md:w-1/2 px-2'),
            ),
            Row(
                Column('precio', css_class='w-full md:w-1/2 px-2'),
                Column('ciudad_venta', css_class='w-full md:w-1/2 px-2'),
            ),
            'tipo_adquiriente',
            'notario',
            'grado_proteccion',
            'incluye_bienes_muebles',
            'observaciones',
            Submit('submit', 'Guardar', css_class='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded')
        )

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Documento
        exclude = ['grabado_por', 'fecha_grabacion', 'modificado_por', 'fecha_modificacion']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-input mt-1 block w-full'}),
            'url': forms.URLInput(attrs={'class': 'form-input mt-1 block w-full'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'fecha',
            'tipo',
            'url',
            Submit('submit', 'Guardar', css_class='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded')
        )