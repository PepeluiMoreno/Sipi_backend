# heritage_defense/rbac/admin.py
# Configuración del panel de administración para los modelos de rbac.

from django.contrib import admin
from .models import Application, Role, Permission, RolePermission, UserRole, UserProfile

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'application', 'description')
    list_filter = ('application',)

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('code', 'application', 'description')
    list_filter = ('application',)

@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('role', 'permission')
    list_filter = ('role__application',)

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role__application',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'address')
    search_fields = ('user__username', 'phone_number')