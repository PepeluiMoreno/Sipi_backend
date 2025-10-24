import os
ENV = os.getenv('ENV', 'production').lower()
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
DATABASE_URL_DIRECT = os.getenv('DATABASE_URL')
DATABASE_URL_POOLER = os.getenv('DATABASE_URL_POOLER')
DATABASE_URL_RUNTIME = DATABASE_URL_POOLER or DATABASE_URL_DIRECT
ALLOWED_ORIGINS = [o.strip() for o in os.getenv('ALLOWED_ORIGINS', '').split(',') if o.strip()]
GRAPHIQL_ENABLED = ENV != 'production'
