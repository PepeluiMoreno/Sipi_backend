# heritage_defense/apps/heritage_buildings/forms.py

from django import forms
from .models import building, document
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

class BuildingForm(forms.ModelForm):
    class Meta:
        model = building
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
        model = document
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