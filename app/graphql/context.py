from .dataloaders import ByIdLoader
from app.db.models import Provincia, Localidad, Diocesis

class GQLContext:
    def __init__(self):
        self.provincia_by_id = ByIdLoader(Provincia)
        self.localidad_by_id = ByIdLoader(Localidad)
        self.diocesis_by_id = ByIdLoader(Diocesis)
