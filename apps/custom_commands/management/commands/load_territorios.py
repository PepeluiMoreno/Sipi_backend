import csv
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.heritage_buildings.models import ComunidadAutonoma, Provincia

class Command(BaseCommand):
    help = 'Carga comunidades autónomas y provincias desde un archivo CSV en la carpeta data.'

    def handle(self, *args, **kwargs):
        # Calcular la ruta base del proyecto (donde está manage.py)
        base_dir = os.path.dirname(os.path.abspath(__file__))  # /code/apps/heritage_buildings/management/commands
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(base_dir))))  # Sube a /code/
        data_dir = os.path.join(base_dir, 'data')  # /code/data

        # Mostrar la ruta para depuración
        self.stdout.write(self.style.NOTICE(f'Ruta base calculada: {base_dir}'))
        self.stdout.write(self.style.NOTICE(f'Ruta de datos: {data_dir}'))

        # Ruta completa al archivo CSV
        csv_path = os.path.join(data_dir, 'comunidades_provincias.csv')
        self.stdout.write(self.style.NOTICE(f'Ruta del archivo CSV: {csv_path}'))

        # Verificar si el archivo CSV existe
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f'Archivo CSV no encontrado: {csv_path}'))
            return

        try:
            with transaction.atomic():
                self._cargar_datos(csv_path)
                self.stdout.write(self.style.SUCCESS('Datos cargados correctamente.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error durante la carga de datos: {str(e)}'))
            raise

    def _cargar_datos(self, csv_path):
        """
        Carga los datos desde el archivo CSV.
        """
        comunidades_provincias = {}  # Diccionario para agrupar provincias por comunidad

        # Leer el archivo CSV
        with open(csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                comunidad_nombre = row['comunidad_autonoma'].strip()
                provincia_nombre = row['provincia'].strip()

                # Agrupar provincias por comunidad
                if comunidad_nombre not in comunidades_provincias:
                    comunidades_provincias[comunidad_nombre] = []
                comunidades_provincias[comunidad_nombre].append(provincia_nombre)

        # Procesar cada comunidad y sus provincias
        for comunidad_nombre, provincias in comunidades_provincias.items():
            # Obtener o crear la comunidad autónoma
            comunidad, created = ComunidadAutonoma.objects.get_or_create(
                nombre=comunidad_nombre
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Creada la comunidad autónoma {comunidad_nombre} ({", ".join(provincias)})'))

            # Obtener o crear las provincias
            for provincia_nombre in provincias:
                provincia, created = Provincia.objects.get_or_create(
                    nombre=provincia_nombre,
                    comunidad_autonoma=comunidad
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'  - Creada provincia: {provincia_nombre}'))