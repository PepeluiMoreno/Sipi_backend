# heritage_defense/rbac/urls.py
# URLs para la aplicación rbac.

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]