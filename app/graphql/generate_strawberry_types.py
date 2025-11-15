# app/graphql/generate_strawberry_types.py
import dataclasses
import strawberry
from typing import Optional, Dict, Any
from sqlalchemy import String, Integer, Boolean, Float, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime

def get_python_type(column_type):
    """Mapea tipos de SQLAlchemy a tipos de Python de forma segura"""
    try:
        if isinstance(column_type, (String, Text)):
            return str
        elif isinstance(column_type, Integer):
            return int
        elif isinstance(column_type, Boolean):
            return bool
        elif isinstance(column_type, Float):
            return float
        elif isinstance(column_type, DateTime):
            return datetime
        elif isinstance(column_type, UUID):
            return str
        elif isinstance(column_type, JSONB):
            return Dict[str, Any]
        else:
            if hasattr(column_type, 'python_type'):
                return column_type.python_type
            return str
    except Exception:
        return str

def generate_strawberry_types(base, include_relationships=False):
    """Genera tipos Strawberry de forma robusta y simple"""
    generated_types = {}
    
    for mapper in base.registry.mappers:
        model_class = mapper.class_
        
        try:
            # Usar campos simples - todos opcionales para evitar problemas
            fields = []
            
            for column in mapper.columns:
                column_name = column.key
                
                if column_name.startswith('_'):
                    continue
                    
                python_type = get_python_type(column.type)
                
                # Todos los campos como opcionales para simplificar
                fields.append((column_name, Optional[python_type]))
            
            if fields:
                # Crear dataclass
                dataclass_type = dataclasses.make_dataclass(
                    model_class.__name__,
                    fields,
                    bases=(object,),
                    namespace={'__annotations__': dict(fields)}
                )
                
                # Convertir a tipo Strawberry
                strawberry_type = strawberry.type(dataclass_type)
                generated_types[model_class.__name__] = strawberry_type
                
        except Exception as e:
            print(f"⚠️  No se pudo generar tipo para {model_class.__name__}: {e}")
            continue
    
    return generated_types