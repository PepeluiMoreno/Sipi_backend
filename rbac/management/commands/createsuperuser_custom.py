import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Crea un superusuario usando variables de entorno'

    def handle(self, *args, **options):
        User = get_user_model()

        # Obtener las credenciales del superusuario desde variables de entorno
        username = os.getenv('DJANGO_SUPERUSER_USERNAME')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

        # Verificar que las variables de entorno estén configuradas
        if not username or not email or not password:
            self.stdout.write(self.style.ERROR('Faltan variables de entorno para crear el superusuario.'))
            return

        # Crear el superusuario si no existe
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS(f'Superusuario "{username}" creado exitosamente.'))
        else:
            self.stdout.write(self.style.WARNING(f'El superusuario "{username}" ya existe.'))