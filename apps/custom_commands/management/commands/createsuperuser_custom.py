import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Crea un superusuario con un nombre de usuario y contraseña específicos desde variables de entorno'

    def handle(self, *args, **kwargs):
        username = os.getenv('DJANGO_SUPERUSER_USERNAME')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')

        # Depuración: Imprime las variables de entorno
        print(f"Username: {username}")
        print(f"Password: {password}")
        print(f"Email: {email}")

        if not username or not password:
            self.stdout.write(self.style.ERROR('Debes proporcionar un nombre de usuario y una contraseña en las variables de entorno'))
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'El usuario "{username}" ya existe'))
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f'Superusuario "{username}" creado con éxito'))