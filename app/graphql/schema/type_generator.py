# query_builder.py
"""
Constructor dinámico de queries SQLAlchemy
"""
from typing import Type, Optional, List
from sqlalchemy import select, func, and_, asc, desc

from .base_types import FilterCondition, OrderBy, PaginationInput, clamp_limit

class DynamicQueryBuilder:
    """Construye queries SQLAlchemy dinámicamente"""
    
    @staticmethod
    def apply_filters(query, model: Type, filters: Optional[List[FilterCondition]]):
        """Aplica filtros dinámicos a la query"""
        if not filters:
            return query
        
        conditions = []
        for filter_cond in filters:
            column = getattr(model, filter_cond.field, None)
            if column is None:
                continue
            
            op = filter_cond.operator
            value = filter_cond.value
            values = filter_cond.values
            
            if op.value == "eq":
                conditions.append(column == value)
            elif op.value == "ne":
                conditions.append(column != value)
            elif op.value == "gt":
                conditions.append(column > value)
            elif op.value == "gte":
                conditions.append(column >= value)
            elif op.value == "lt":
                conditions.append(column < value)
            elif op.value == "lte":
                conditions.append(column <= value)
            elif op.value == "like":
                conditions.append(column.like(f"%{value}%"))
            elif op.value == "ilike":
                conditions.append(column.ilike(f"%{value}%"))
            elif op.value == "in":
                if values:
                    conditions.append(column.in_(values))
            elif op.value == "not_in":
                if values:
                    conditions.append(~column.in_(values))
            elif op.value == "is_null":
                if value:
                    conditions.append(column.is_(None))
                else:
                    conditions.append(column.isnot(None))
            elif op.value == "between":
                if values and len(values) == 2:
                    conditions.append(column.between(values[0], values[1]))
        
        if conditions:
            query = query.where(and_(*conditions))
        
        return query
    
    @staticmethod
    def apply_ordering(query, model: Type, order_by: Optional[List[OrderBy]]):
        """Aplica ordenamiento a la query"""
        if not order_by:
            return query
        
        for order in order_by:
            column = getattr(model, order.field, None)
            if column is None:
                continue
            
            if order.direction.value == "asc":
                query = query.order_by(asc(column))
            else:
                query = query.order_by(desc(column))
        
        return query
    
    @staticmethod
    def apply_pagination(query, pagination: Optional[PaginationInput]):
        """Aplica paginación a la query"""
        if not pagination:
            return query, 1, 20
        
        page = max(1, pagination.page)
        page_size = clamp_limit(pagination.page_size, 20, 100)
        
        offset = (page - 1) * page_size
        query = query.limit(page_size).offset(offset)
        
        return query, page, page_size