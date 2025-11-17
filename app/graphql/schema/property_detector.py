"""
Detección y resolución de propiedades y métodos de modelos SQLAlchemy
"""
from typing import Type, Dict, Any, Callable, List
from datetime import datetime, date
from decimal import Decimal
from strawberry.types import Info
import enum
import uuid

# ==================== DETECTOR DE PROPIEDADES ====================

class PropertyDetector:
    """Detecta propiedades y métodos en modelos SQLAlchemy"""
    
    @staticmethod
    def is_property_method(obj) -> bool:
        """Determina si un objeto es una propiedad (@property)"""
        return isinstance(obj, property) or (
            hasattr(obj, 'fget') and obj.fget is not None
        )
    
    @staticmethod
    def is_callable_method(obj) -> bool:
        """Determina si un objeto es un método callable que puede ser útil"""
        return callable(obj) and not isinstance(obj, type) and not obj.__name__.startswith('_')
    
    @staticmethod
    def get_model_properties(model: Type) -> Dict[str, Any]:
        """Obtiene todas las propiedades y métodos útiles de un modelo"""
        properties = {}
        
        # Obtener todas las propiedades (@property)
        for attr_name in dir(model):
            if attr_name.startswith('_'):
                continue
                
            attr = getattr(model, attr_name)
            
            # Detectar propiedades (@property)
            if PropertyDetector.is_property_method(attr):
                properties[attr_name] = {
                    'type': 'property',
                    'obj': attr,
                    'return_type': PropertyDetector.infer_return_type(attr)
                }
            
            # Detectar métodos útiles (excluyendo métodos internos)
            elif (PropertyDetector.is_callable_method(attr) and 
                  hasattr(attr, '__name__') and 
                  not attr_name.startswith('_')):
                excluded_prefixes = ['query', 'metadata', 'register', 'test_', 'sa_']
                if not any(attr_name.startswith(prefix) for prefix in excluded_prefixes):
                    properties[attr_name] = {
                        'type': 'method',
                        'obj': attr,
                        'return_type': PropertyDetector.infer_return_type(attr)
                    }
        
        return properties
    
    @staticmethod
    def infer_return_type(prop_obj) -> Type:
        """Infiere el tipo de retorno de una propiedad o método"""
        try:
            if hasattr(prop_obj, 'fget') and prop_obj.fget is not None:
                func = prop_obj.fget
            else:
                func = prop_obj
            
            if hasattr(func, '__annotations__') and 'return' in func.__annotations__:
                return func.__annotations__['return']
            
            if hasattr(func, '__name__'):
                name = func.__name__.lower()
                if name.startswith('is_') or name.startswith('has_') or name.startswith('tiene_'):
                    return bool
                elif name.startswith('get_') or name.endswith('_list'):
                    return List[Any]
                elif 'count' in name or 'total' in name:
                    return int
                elif 'date' in name or 'fecha' in name:
                    return date
                elif 'datetime' in name:
                    return datetime
            
            return str
            
        except Exception:
            return str

# ==================== RESOLVER DE PROPIEDADES ====================

class PropertyResolver:
    """Resuelve propiedades y métodos en resolvers GraphQL"""
    
    @staticmethod
    def create_property_resolver(prop_name: str, prop_info: Dict) -> Callable:
        """Crea un resolver para una propiedad o método"""
        
        async def resolver(self, info: Info) -> Any:
            try:
                model_instance = self._model_instance
                prop_value = getattr(model_instance, prop_name)
                
                if prop_info['type'] == 'method' and callable(prop_value):
                    result = prop_value()
                    if hasattr(result, '__await__'):
                        result = await result
                    return result
                else:
                    return prop_value
                    
            except Exception as e:
                print(f"Error resolviendo propiedad {prop_name}: {e}")
                return None
        
        return resolver
