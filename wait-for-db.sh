#!/bin/bash
set -e

host="db"
port="5432"

echo "Esperando a que PostgreSQL esté disponible en $host:$port..."

while ! nc -z $host $port; do
  sleep 1
done

echo "PostgreSQL está listo - ejecutando comando"
exec "$@"