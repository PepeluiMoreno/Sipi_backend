# heritage_defense/apps/heritage_buildings/management/commands/import_data.py
import csv
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.heritage_buildings.models import (
    ComunidadAutonoma, Provincia, Diocesis,
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
        self.stdout.write(self.style.NOTICE(f'Ruta base calculada: {base_dir}'))
        self.stdout.write(self.style.NOTICE(f'Ruta de datos: {data_dir}'))

        # Contadores para el resumen
        comunidades_creadas = 0
        provincias_creadas = 0
        diocesis_creadas = 0
        tipos_documento_creados = 0
        tipos_adquiriente_creados = 0
        grados_proteccion_creados = 0

        try:
            with transaction.atomic():
                comunidades_creadas = self._import_comunidades(data_dir)
                provincias_creadas = self._import_provincias(data_dir)
                diocesis_creadas = self._import_diocesis(data_dir)
                tipos_documento_creados = self._import_tipos_documento(data_dir)
                tipos_adquiriente_creados = self._import_tipos_adquiriente(data_dir)
                grados_proteccion_creados = self._import_grados_proteccion(data_dir)

            # Resumen final
            self.stdout.write(self.style.SUCCESS('Proceso de importación completado:'))
            self.stdout.write(self.style.SUCCESS(f'- Comunidades autónomas: {comunidades_creadas} nuevas'))
            self.stdout.write(self.style.SUCCESS(f'- Provincias: {provincias_creadas} nuevas'))
            self.stdout.write(self.style.SUCCESS(f'- Diócesis: {diocesis_creadas} nuevas'))
            self.stdout.write(self.style.SUCCESS(f'- Tipos de documento: {tipos_documento_creados} nuevos'))
            self.stdout.write(self.style.SUCCESS(f'- Tipos de adquiriente: {tipos_adquiriente_creados} nuevos'))
            self.stdout.write(self.style.SUCCESS(f'- Grados de protección: {grados_proteccion_creados} nuevos'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error durante la importación: {str(e)}'))
            raise

    def _import_comunidades(self, data_dir):
        comunidades_path = os.path.join(data_dir, 'comunidades_autonomas.csv')
        self.stdout.write(self.style.HTTP_INFO(f'Importando comunidades autónomas desde {comunidades_path}...'))
        comunidades_creadas = 0

        try:
            with open(comunidades_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if not row.get('id') or not row.get('nombre'):
                        self.stdout.write(self.style.WARNING(f'Fila inválida en comunidades: {row}'))
                        continue
                    _, created = ComunidadAutonoma.objects.get_or_create(
                        id=row['id'],
                        defaults={'nombre': row['nombre'].strip()}
                    )
                    if created:
                        comunidades_creadas += 1
            self.stdout.write(self.style.SUCCESS(f'Comunidades autónomas importadas: {comunidades_creadas} nuevas'))
            return comunidades_creadas
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'No se encontró el archivo {comunidades_path}'))
            raise
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importando comunidades: {str(e)}'))
            raise

    def _import_provincias(self, data_dir):
        provincias_path = os.path.join(data_dir, 'provincias.csv')
        self.stdout.write(self.style.HTTP_INFO(f'Importando provincias desde {provincias_path}...'))
        provincias_creadas = 0

        try:
            with open(provincias_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if not row.get('id') or not row.get('nombre') or not row.get('comunidad_autonoma_id'):
                        self.stdout.write(self.style.WARNING(f'Fila inválida en provincias: {row}'))
                        continue
                    try:
                        comunidad_autonoma = ComunidadAutonoma.objects.get(id=row['comunidad_autonoma_id'])
                        _, created = Provincia.objects.get_or_create(
                            id=row['id'],
                            defaults={
                                'nombre': row['nombre'].strip(),
                                'comunidad_autonoma': comunidad_autonoma
                            }
                        )
                        if created:
                            provincias_creadas += 1
                    except ComunidadAutonoma.DoesNotExist:
                        self.stdout.write(self.style.WARNING(
                            f'Comunidad autónoma {row["comunidad_autonoma_id"]} no encontrada para provincia {row["nombre"]}'
                        ))
            self.stdout.write(self.style.SUCCESS(f'Provincias importadas: {provincias_creadas} nuevas'))
            return provincias_creadas
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'No se encontró el archivo {provincias_path}'))
            raise
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importando provincias: {str(e)}'))
            raise

    def _import_diocesis(self, data_dir):
        diocesis_path = os.path.join(data_dir, 'diocesis.csv')
        self.stdout.write(self.style.HTTP_INFO(f'Importando diócesis desde {diocesis_path}...'))
        diocesis_creadas = 0

        try:
            with open(diocesis_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if not row.get('id') or not row.get('nombre'):
                        self.stdout.write(self.style.WARNING(f'Fila inválida en diócesis: {row}'))
                        continue
                    _, created = Diocesis.objects.get_or_create(
                        id=row['id'],
                        defaults={'nombre': row['nombre'].strip()}
                    )
                    if created:
                        diocesis_creadas += 1
            self.stdout.write(self.style.SUCCESS(f'Diócesis importadas: {diocesis_creadas} nuevas'))
            return diocesis_creadas
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'No se encontró el archivo {diocesis_path}'))
            raise
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importando diócesis: {str(e)}'))
            raise

    def _import_tipos_documento(self, data_dir):
        tipos_documento_path = os.path.join(data_dir, 'tipos_documento.csv')
        self.stdout.write(self.style.HTTP_INFO(f'Importando tipos de documento desde {tipos_documento_path}...'))
        tipos_documento_creados = 0

        try:
            with open(tipos_documento_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if not row.get('denominacion'):
                        self.stdout.write(self.style.WARNING(f'Fila inválida en tipos de documento: {row}'))
                        continue
                    # Si hay 'id', úsalo; si no, usa 'denominacion' como clave única
                    if row.get('id'):
                        _, created = TipoDocumento.objects.get_or_create(
                            id=row['id'],
                            defaults={'denominacion': row['denominacion'].strip()}
                        )
                    else:
                        _, created = TipoDocumento.objects.get_or_create(
                            denominacion=row['denominacion'].strip()
                        )
                    if created:
                        tipos_documento_creados += 1
            self.stdout.write(self.style.SUCCESS(f'Tipos de documento importados: {tipos_documento_creados} nuevos'))
            return tipos_documento_creados
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'No se encontró el archivo {tipos_documento_path}'))
            raise
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importando tipos de documento: {str(e)}'))
            raise

    def _import_tipos_adquiriente(self, data_dir):
        tipos_adquiriente_path = os.path.join(data_dir, 'tipos_adquiriente.csv')
        self.stdout.write(self.style.HTTP_INFO(f'Importando tipos de adquiriente desde {tipos_adquiriente_path}...'))
        tipos_adquiriente_creados = 0

        try:
            with open(tipos_adquiriente_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if not row.get('nombre'):
                        self.stdout.write(self.style.WARNING(f'Fila inválida en tipos de adquiriente: {row}'))
                        continue
                    # Si hay 'id', úsalo; si no, usa 'nombre' como clave única
                    if row.get('id'):
                        _, created = TipoAdquiriente.objects.get_or_create(
                            id=row['id'],
                            defaults={'nombre': row['nombre'].strip()}
                        )
                    else:
                        _, created = TipoAdquiriente.objects.get_or_create(
                            nombre=row['nombre'].strip()
                        )
                    if created:
                        tipos_adquiriente_creados += 1
            self.stdout.write(self.style.SUCCESS(f'Tipos de adquiriente importados: {tipos_adquiriente_creados} nuevos'))
            return tipos_adquiriente_creados
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'No se encontró el archivo {tipos_adquiriente_path}'))
            raise
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importando tipos de adquiriente: {str(e)}'))
            raise

    def _import_grados_proteccion(self, data_dir):
        grados_proteccion_path = os.path.join(data_dir, 'grados_proteccion.csv')
        self.stdout.write(self.style.HTTP_INFO(f'Importando grados de protección desde {grados_proteccion_path}...'))
        grados_proteccion_creados = 0

        try:
            with open(grados_proteccion_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if not row.get('nombre'):
                        self.stdout.write(self.style.WARNING(f'Fila inválida en grados de protección: {row}'))
                        continue
                    # Si hay 'id', úsalo; si no, usa 'nombre' como clave única
                    if row.get('id'):
                        _, created = GradoProteccion.objects.get_or_create(
                            id=row['id'],
                            defaults={'nombre': row['nombre'].strip()}
                        )
                    else:
                        _, created = GradoProteccion.objects.get_or_create(
                            nombre=row['nombre'].strip()
                        )
                    if created:
                        grados_proteccion_creados += 1
            self.stdout.write(self.style.SUCCESS(f'Grados de protección importados: {grados_proteccion_creados} nuevos'))
            return grados_proteccion_creados
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'No se encontró el archivo {grados_proteccion_path}'))
            raise
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importando grados de protección: {str(e)}'))
            raise