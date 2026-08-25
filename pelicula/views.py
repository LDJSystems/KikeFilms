from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import Pelicula
from .forms import PeliculaForm

# Create your views here.

#Crear nueva pelicula
def agregar_pelicula(request):
    if request.method == 'POST':
        formulario = PeliculaForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('pelicula')
    else:
        formulario = PeliculaForm()
    return render(request, 'pelicula/nuevo.html', {'formulario' : formulario})

#Listado de Peliculas
def listar_peliculas(request):
    peliculas = Pelicula.objects.all()
    return render(request, 'pelicula/lista.html', {'peliculas' : peliculas})
