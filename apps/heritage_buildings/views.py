# heritage_defense/apps/heritage_buildings/views.py
# Vistas para la gestión de inmuebles y documents.

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import building, document
from .forms import BuildingForm, DocumentForm

@login_required
def building_list(request):
    buildings = building.objects.all()
    return render(request, 'heritage_buildings/building_list.html', {'buildings': buildings})

@login_required
def building_detail(request, pk):
    building = get_object_or_404(building, pk=pk)
    return render(request, 'heritage_buildings/building_detail.html', {'building': building})

@login_required
def building_create(request):
    if request.method == 'POST':
        form = BuildingForm(request.POST)
        if form.is_valid():
            building = form.save(commit=False)
            building.save()
            return redirect('building_detail', pk=building.pk)
    else:
        form = BuildingForm()
    return render(request, 'heritage_buildings/building_form.html', {'form': form})

@login_required
def building_edit(request, pk):
    building = get_object_or_404(building, pk=pk)
    if request.method == 'POST':
        form = BuildingForm(request.POST, instance=building)
        if form.is_valid():
            building = form.save()
            return redirect('building_detail', pk=building.pk)
    else:
        form = BuildingForm(instance=building)
    return render(request, 'heritage_buildings/building_form.html', {'form': form})

@login_required
def building_delete(request, pk):
    building = get_object_or_404(building, pk=pk)
    if request.method == 'POST':
        building.delete()
        return redirect('building_list')
    return render(request, 'heritage_buildings/building_confirm_delete.html', {'building': building})

@login_required
def document_list(request):
    documents = document.objects.all()
    return render(request, 'heritage_buildings/document_list.html', {'documents': documents})

@login_required
def document_detail(request, pk):
    document = get_object_or_404(document, pk=pk)
    return render(request, 'heritage_buildings/document_detail.html', {'document': document})

@login_required
def document_create(request):
    if request.method == 'POST':
        form = documentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save()
            return redirect('document_detail', pk=document.pk)
    else:
        form = documentForm()
    return render(request, 'heritage_buildings/document_form.html', {'form': form})

@login_required
def document_edit(request, pk):
    document = get_object_or_404(document, pk=pk)
    if request.method == 'POST':
        form = documentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            document = form.save()
            return redirect('document_detail', pk=document.pk)
    else:
        form = documentForm(instance=document)
    return render(request, 'heritage_buildings/document_form.html', {'form': form})

@login_required
def document_delete(request, pk):
    document = get_object_or_404(document, pk=pk)
    if request.method == 'POST':
        document.delete()
        return redirect('document_list')
    return render(request, 'heritage_buildings/document_confirm_delete.html', {'document': document})