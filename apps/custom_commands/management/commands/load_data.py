import csv
import json
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.heritage_buildings.models import (
    Diocesis,
    TipoDocumento, TipoAdquiriente, GradoProteccion
)


class Command(BaseCommand):
    help = 'Importa comunidades autónomas, provincias, diócesis, tipos de documento, tipos de adquiriente y grados de protección desde archivos CSV en la carpeta data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--data-dir',
            type=str,
            default='data',
            help='Directorio donde se encuentran los archivos CSV (relativo a la raíz del proyecto)'
        )

    def handle(self, *args, **kwargs):
        # Calcular la raíz del proyecto (donde está manage.py)
        base_dir = os.path.dirname(os.path.abspath(__file__))  # /code/apps/heritage_buildings/management/commands
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(base_dir))))  # Sube a /code/
        data_dir = os.path.join(base_dir, kwargs['data_dir'])  # /code/data por defecto

        # Mostrar la ruta para depuración
        self.stdout.write(self.style.NOTICE(f'Load_data: Ruta base calculada: {base_dir}'))
        self.stdout.write(self.style.NOTICE(f'Load_data: Ruta de datos: {data_dir}'))

        try:
            with transaction.atomic():
                # Borrar archivos JSON existentes
                self._borrar_json_existente(data_dir)

                # Convertir CSV a JSON
                self._convert_csv_to_json(data_dir)

                # Cargar datos desde JSON evitando duplicados
                self._load_data_from_json(data_dir)

            self.stdout.write(self.style.SUCCESS('Load_data: Proceso de importación completado.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Load_data: Error durante la importación: {str(e)}'))
            raise

    def _borrar_json_existente(self, data_dir):
        """
        Borra archivos JSON existentes en la carpeta de datos.
        """
        archivos_json = [
            'diocesis.json',
            'tipos_documento.json',
            'tipos_adquiriente.json',
            'grados_proteccion.json',
        ]

        for json_file in archivos_json:
            json_path = os.path.join(data_dir, json_file)
            if os.path.exists(json_path):
                os.remove(json_path)
                self.stdout.write(self.style.WARNING(f'Load_data: Archivo JSON borrado: {json_path}'))

    def _convert_csv_to_json(self, data_dir):
        """
        Convierte archivos CSV a JSON.
        """
        archivos_csv = [
            ('diocesis.csv', 'diocesis.json'),
            ('tipos_documento.csv', 'tipos_documento.json'),
            ('tipos_adquiriente.csv', 'tipos_adquiriente.json'),
            ('grados_proteccion.csv', 'grados_proteccion.json'),
        ]

        for csv_file, json_file in archivos_csv:
            csv_path = os.path.join(data_dir, csv_file)
            json_path = os.path.join(data_dir, json_file)

            if not os.path.exists(csv_path):
                self.stdout.write(self.style.WARNING(f'Load_data: Archivo CSV no encontrado: {csv_path}'))
                continue

            try:
                # Leer CSV y convertir a JSON
                with open(csv_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    datos = [fila for fila in reader]

                # Escribir JSON
                with open(json_path, 'w', encoding='utf-8') as jsonfile:
                    json.dump(datos, jsonfile, indent=4, ensure_ascii=False)

                self.stdout.write(self.style.SUCCESS(f'Load_data: Archivo JSON generado: {json_path}'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Load_data: Error convirtiendo {csv_path} a JSON: {str(e)}'))
                raise

    def _load_data_from_json(self, data_dir):
        """
        Carga datos desde archivos JSON usando get_or_create para evitar duplicados.
        """
        archivos_json = [
            'diocesis.json',
            'tipos_documento.json',
            'tipos_adquiriente.json',
            'grados_proteccion.json',
        ]

        for json_file in archivos_json:
            json_path = os.path.join(data_dir, json_file)

            if not os.path.exists(json_path):
                self.stdout.write(self.style.WARNING(f'Load_data: Archivo JSON no encontrado: {json_path}'))
                continue

            try:
                # Leer el archivo JSON
                with open(json_path, 'r', encoding='utf-8') as jsonfile:
                    datos = json.load(jsonfile)

                # Cargar datos usando get_or_create
                for registro in datos:
                    if json_file == 'diocesis.json':
                        _, created = Diocesis.objects.get_or_create(
                            nombre=registro['nombre'],  # Campo único
                            defaults={}  # No necesitamos defaults si no hay 'id'
                        )
                    elif json_file == 'tipos_documento.json':
                        _, created = TipoDocumento.objects.get_or_create(
                            denominacion=registro['denominacion'],  # Campo único
                            defaults={}  # No necesitamos defaults si no hay 'id'
                        )
                    elif json_file == 'tipos_adquiriente.json':
                        _, created = TipoAdquiriente.objects.get_or_create(
                            nombre=registro['nombre'],  # Campo único
                            defaults={}  # No necesitamos defaults si no hay 'id'
                        )
                    elif json_file == 'grados_proteccion.json':
                        _, created = GradoProteccion.objects.get_or_create(
                            nombre=registro['nombre'],  # Campo único
                            defaults={}  # No necesitamos defaults si no hay 'id'
                        )

                    if not created:
                        self.stdout.write(self.style.WARNING(f'Load_data: Registro duplicado: {registro}'))

                self.stdout.write(self.style.SUCCESS(f'Load_data: Datos cargados desde: {json_path}'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Load_data: Error cargando {json_path}: {str(e)}'))
                raise