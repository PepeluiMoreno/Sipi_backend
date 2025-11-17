
"""
Generadores de tipos Strawberry y resolvers de propiedades para modelos SQLAlchemy
"""
from typing import Type, Any, Dict, Callable, List, Optional, get_origin, get_args
from datetime import date, datetime
from decimal import Decimal
import strawberry
from strawberry.types import Info
from sqlalchemy.inspection import inspect
import enum
import uuid

# ==============================
# Property Detector
# ==============================

class PropertyDetector:
    """Detecta propiedades y métodos útiles en un modelo SQLAlchemy"""

    @staticmethod
    def is_property_method(obj) -> bool:
        """Determina si un objeto es una propiedad (@property)"""
        return isinstance(obj, property) or (hasattr(obj, 'fget') and obj.fget is not None)

    @staticmethod
    def is_callable_method(obj) -> bool:
        """Determina si un objeto es un método callable público"""
        return callable(obj) and not isinstance(obj, type) and not obj.__name__.startswith("_")

    @staticmethod
    def get_model_properties(model: Type) -> Dict[str, Dict[str, Any]]:
        """Devuelve propiedades y métodos útiles con tipos inferidos"""
        props = {}

        for attr_name in dir(model):
            if attr_name.startswith("_"):
                continue

            attr = getattr(model, attr_name)

            if PropertyDetector.is_property_method(attr):
                props[attr_name] = {
                    "type": "property",
                    "obj": attr,
                    "return_type": PropertyDetector.infer_return_type(attr)
                }
            elif PropertyDetector.is_callable_method(attr):
                excluded_prefixes = ["query", "metadata", "register", "sa_"]
                if not any(attr_name.startswith(p) for p in excluded_prefixes):
                    props[attr_name] = {
                        "type": "method",
                        "obj": attr,
                        "return_type": PropertyDetector.infer_return_type(attr)
                    }
        return props

    @staticmethod
    def infer_return_type(attr_obj) -> Type:
        """Intenta inferir tipo de retorno de propiedades o métodos"""
        try:
            func = attr_obj.fget if hasattr(attr_obj, "fget") and attr_obj.fget else attr_obj
            if hasattr(func, "__annotations__") and "return" in func.__annotations__:
                return func.__annotations__["return"]

            # heurísticas por nombre
            name = getattr(func, "__name__", "").lower()
            if name.startswith("is_") or name.startswith("has_") or name.startswith("tiene_"):
                return bool
            if name.startswith("get_") or name.endswith("_list"):
                return List[Any]
            if "count" in name or "total" in name:
                return int
            if "date" in name or "fecha" in name:
                return date
            if "datetime" in name:
                return datetime

            return str
        except Exception:
            return str

# ==============================
# Property Resolver
# ==============================

class PropertyResolver:
    """Crea resolvers para propiedades y métodos de un modelo"""

    @staticmethod
    def create_property_resolver(prop_name: str, prop_info: Dict) -> Callable:
        async def resolver(self, info: Info) -> Any:
            try:
                instance = self._model_instance
                value = getattr(instance, prop_name)
                if prop_info["type"] == "method" and callable(value):
                    result = value()
                    if hasattr(result, "__await__"):
                        result = await result
                    return result
                return value
            except Exception as e:
                print(f"Error resolviendo propiedad '{prop_name}': {e}")
                return None
        return resolver

# ==============================
# Strawberry Type Generator
# ==============================

class StrawberryTypeGenerator:
    """Genera tipos Strawberry a partir de modelos SQLAlchemy"""

    _type_mapping = {
        int: int,
        str: str,
        float: float,
        bool: bool,
        datetime: datetime,
        date: date,
        Decimal: float,
        dict: str,
        list: list,
    }

    @classmethod
    def python_type_to_strawberry(cls, py_type: Type, column=None) -> Type:
        """Convierte tipos Python a tipos Strawberry"""
        origin = get_origin(py_type)
        if origin is Optional:
            args = get_args(py_type)
            if args:
                return Optional[cls.python_type_to_strawberry(args[0], column)]
        if origin is list:
            args = get_args(py_type)
            if args:
                return List[cls.python_type_to_strawberry(args[0], column)]
            return List[Any]

        if isinstance(py_type, type) and issubclass(py_type, enum.Enum):
            return py_type

        if py_type == uuid.UUID:
            return strawberry.ID

        if column and (column.primary_key or column.name == "id"):
            return strawberry.ID

        return cls._type_mapping.get(py_type, str)

    @classmethod
    def generate_strawberry_type(cls, model: Type, type_name: str = None) -> Type:
        """Genera un tipo Strawberry completo incluyendo propiedades"""
        if type_name is None:
            type_name = f"{model.__name__}Type"

        mapper = inspect(model)
        fields: Dict[str, Type] = {}

        # Columnas
        for col in mapper.columns:
            st_type = cls.python_type_to_strawberry(col.type.python_type, col)
            fields[col.name] = Optional[st_type] if col.nullable else st_type

        # Propiedades y métodos
        props = PropertyDetector.get_model_properties(model)
        for name, info in props.items():
            st_type = cls.python_type_to_strawberry(info["return_type"])
            fields[name] = st_type

        # Crear tipo Strawberry dinámico
        return strawberry.type(type(type_name, (), {"__annotations__": fields}))

    @classmethod
    def generate_input_type(cls, model: Type, operation: str = "create") -> Type:
        """Genera Input type para create/update"""
        type_name = f"{model.__name__}{operation.capitalize()}Input"
        mapper = inspect(model)
        fields: Dict[str, Type] = {}

        for col in mapper.columns:
            if col.primary_key and operation == "create":
                continue
            py_type = col.type.python_type
            st_type = cls.python_type_to_strawberry(py_type, col)

            if operation == "update":
                st_type = Optional[st_type]
            else:  # create
                if col.nullable or col.default or col.server_default:
                    st_type = Optional[st_type]

            fields[col.name] = st_type

        return strawberry.input(type(type_name, (), {"__annotations__": fields}))
