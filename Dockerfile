FROM python:3.11-slim
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# código
COPY . .

# entrypoint al final para no perder permisos si se re-copia
COPY entrypoint.sh /app/entrypoint.sh
RUN sed -i 's/\r$//' /app/entrypoint.sh && chmod 755 /app/entrypoint.sh

# Copia el script de espera
COPY wait-for-db.sh /app/wait-for-db.sh
RUN chmod +x /app/wait-for-db.sh

# Usa el script de espera en el comando
CMD ["./wait-for-db.sh", "db", "python", "main.py"]

EXPOSE 8000
ENTRYPOINT ["/app/entrypoint.sh"]

