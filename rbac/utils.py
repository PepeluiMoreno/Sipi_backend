# heritage_defense/rbac/utils.py
# Utilidades para la aplicación rbac.

from django.core.exceptions import PermissionDenied
from .models import UserRole, Permission, Application

def has_permission(user, permission_code, application_name):
    try:
        application = Application.objects.get(name=application_name)
        permission = Permission.objects.get(code=permission_code, application=application)
        roles = UserRole.objects.filter(user=user, role__application=application, role__rolepermission__permission=permission)
        return roles.exists()
    except (Application.DoesNotExist, Permission.DoesNotExist):
        return False

def check_permission(user, permission_code, application_name):
    if not has_permission(user, permission_code, application_name):
        raise PermissionDenied("You do not have permission to perform this action.")