# app/graphql/error_handling.py

import sys
from functools import wraps

def suppress_traceback_continue(func):
    """Decorador para suprimir tracebacks pero continuar la ejecución"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_type = type(e).__name__
            print(f"⚠️  {error_type} en {func.__name__}: {str(e)}", file=sys.stderr)
            return None
    return wrapper