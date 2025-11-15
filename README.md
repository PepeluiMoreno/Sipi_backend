# SIPI ·  Servicio de Información sobre el Patrimonio Inmatriculado por la Iglesia Católica en España
Generado: 2025-11-11 22:39:17 UTC

## Contenido y alcance de la aplicación
- Servidor **Strawberry GraphQL** para servir en formato json la información disponible  de uso religioso y completar sus expendientes en cuanto a transmisiones de propiedad y rehabilitaciones a través del frontend de la aplicación SIPI, ara consulta cruda desde un sandbox de graphql.
- ETL con extract/transform/load y workflows n8n stub, con datos obtendidos de fuentes cartograficas y documentales como OSM y Wikidata.
- Cruce del censo de edificios religiosos con el listado publicado de las inmatriculaciones para marcar los inmatriculados
- TODO: contectarla a la aplicación BDNS-backend de subvenciones para busqueda de concesiones monetarias percibidad por la persona jurídica que ostenta la posesión del inmueble.

  

## Arranque
```bash
pip install -e .
cp .env.example .env
python -m app.graphql.asgi
# http://localhost:8040/graphql
```
