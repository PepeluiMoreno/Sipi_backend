# heritage_defense/config/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rbac/', include('rbac.urls')),  # URLs de la  utilidad de control de acceso
    path('heritage_buildings/', include('apps.heritage_buildings.urls')),  # URLs de la app heritage_buildings
    
]