# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /code

# Instalar dependencias del sistema necesarias para Pillow
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar el archivo de requisitos
COPY requirements.txt /code/

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . /code/

# Exponer el puerto 8000
EXPOSE 8000

# Comando para ejecutar Gunicorn
CMD ["gunicorn", "heritage_defense.wsgi:application", "--bind", "0.0.0.0:8000"]