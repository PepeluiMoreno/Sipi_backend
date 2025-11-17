"""
Schema principal - ensamblaje final de GraphQL
"""
from pathlib import Path
import importlib
from typing import List, Type
import strawberry

from .schema_generator import SchemaGenerator

# -----------------------------
# Función para cargar modelos automáticamente
# -----------------------------
def load_models_from_folder(folder: str) -> List[Type]:
    models = []
    folder_path = Path(folder)
    if not folder_path.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")

    for py_file in folder_path.glob("*.py"):
        if py_file.name.startswith("__"):
            continue
        module_name = f"{folder.replace('/', '.')}.{py_file.stem}"
        module = importlib.import_module(module_name)

        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if hasattr(attr, "__tablename__"):
                models.append(attr)
    return models

# -----------------------------
# Cargar modelos
# -----------------------------
MODELS = load_models_from_folder("app/db/models")

# -----------------------------
# Generar schema
# -----------------------------
schema: strawberry.Schema = SchemaGenerator.generate_schema(MODELS)
