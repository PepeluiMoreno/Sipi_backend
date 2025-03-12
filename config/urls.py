# heritage_defense/config/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('heritage_buildings/', include('apps.heritage_buildings.urls')),  # URLs de la app heritage_buildings
    path('', admin.site.urls)  # provisional
]