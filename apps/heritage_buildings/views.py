# heritage_defense/apps/heritage_buildings/views.py
# Vistas para la gestión de inmuebles y documents.

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Edificio, Documento
from .forms import BuildingForm, DocumentForm

@login_required
def building_list(request):
    buildings = Edificio.objects.all()
    return render(request, 'heritage_buildings/building_list.html', {'buildings': buildings})

@login_required
def building_detail(request, pk):
    Edificio = get_object_or_404(Edificio, pk=pk)
    return render(request, 'heritage_buildings/building_detail.html', {'Edificio': Edificio})

@login_required
def building_create(request):
    if request.method == 'POST':
        form = BuildingForm(request.POST)
        if form.is_valid():
            Edificio = form.save(commit=False)
            Edificio.save()
            return redirect('building_detail', pk=Edificio.pk)
    else:
        form = BuildingForm()
    return render(request, 'heritage_buildings/building_form.html', {'form': form})

@login_required
def building_edit(request, pk):
    Edificio = get_object_or_404(Edificio, pk=pk)
    if request.method == 'POST':
        form = BuildingForm(request.POST, instance=Edificio)
        if form.is_valid():
            Edificio = form.save()
            return redirect('building_detail', pk=Edificio.pk)
    else:
        form = BuildingForm(instance=Edificio)
    return render(request, 'heritage_buildings/building_form.html', {'form': form})

@login_required
def building_delete(request, pk):
    Edificio = get_object_or_404(Edificio, pk=pk)
    if request.method == 'POST':
        Edificio.delete()
        return redirect('building_list')
    return render(request, 'heritage_buildings/building_confirm_delete.html', {'Edificio': Edificio})

@login_required
def document_list(request):
    documents = Documento.objects.all()
    return render(request, 'heritage_buildings/document_list.html', {'documents': documents})

@login_required
def document_detail(request, pk):
    Documento = get_object_or_404(Documento, pk=pk)
    return render(request, 'heritage_buildings/document_detail.html', {'Documento': Documento})

@login_required
def document_create(request):
    if request.method == 'POST':
        form = documentForm(request.POST, request.FILES)
        if form.is_valid():
            Documento = form.save()
            return redirect('document_detail', pk=Documento.pk)
    else:
        form = documentForm()
    return render(request, 'heritage_buildings/document_form.html', {'form': form})

@login_required
def document_edit(request, pk):
    Documento = get_object_or_404(Documento, pk=pk)
    if request.method == 'POST':
        form = documentForm(request.POST, request.FILES, instance=Documento)
        if form.is_valid():
            Documento = form.save()
            return redirect('document_detail', pk=Documento.pk)
    else:
        form = documentForm(instance=Documento)
    return render(request, 'heritage_buildings/document_form.html', {'form': form})

@login_required
def document_delete(request, pk):
    Documento = get_object_or_404(Documento, pk=pk)
    if request.method == 'POST':
        Documento.delete()
        return redirect('document_list')
    return render(request, 'heritage_buildings/document_confirm_delete.html', {'Documento': Documento})