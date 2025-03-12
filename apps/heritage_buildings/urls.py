# heritage_defense/apps/heritage_buildings/urls.py

from django.urls import path
from . import views
from django.contrib import admin

admin.site.site_header = 'Coordinadora Recuperando '                                       # default: "Django Administration"
admin.site.index_title = 'Registro de Bienes Inmatriculados'                 # default: "Site administration"
admin.site.site_title = 'SI2V' # default: "Django site admin"

urlpatterns = [
    path('', views.building_list, name='building_list'),
    path('<int:pk>/', views.building_detail, name='building_detail'),
    path('new/', views.building_create, name='building_create'),
    path('<int:pk>/edit/', views.building_edit, name='building_edit'),
    path('<int:pk>/delete/', views.building_delete, name='building_delete'),
    path('documents/', views.document_list, name='document_list'),
    path('documents/<int:pk>/', views.document_detail, name='document_detail'),
    path('documents/new/', views.document_create, name='document_create'),
    path('documents/<int:pk>/edit/', views.document_edit, name='document_edit'),
    path('documents/<int:pk>/delete/', views.document_delete, name='document_delete'),
]