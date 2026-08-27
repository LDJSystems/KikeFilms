from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from core.decorators import gestor_required
from .models import Pelicula
from .forms import PeliculaForm

# Create your views here.

#Crear nueva pelicula
@login_required
@gestor_required
def agregar_pelicula(request):
    if request.method == 'POST':
        formulario = PeliculaForm(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect('listar_peliculas')
    else:
        formulario = PeliculaForm()
    return render(request, 'pelicula/nueva_pelicula.html', {'formulario' : formulario})

#Listado de Peliculas
def listar_peliculas(request):
    peliculas = Pelicula.objects.all()
    print(peliculas)
    return render(request, 'pelicula/lista.html', {'peliculas' : peliculas})

#Modificar Peliculas
@login_required
@gestor_required
def modificar_pelicula(request, pk):
    pelicula = get_object_or_404(Pelicula, pk = pk)

    if request.method == 'POST':
        formulario = PeliculaForm(
            request.POST, 
            request.FILES,
            instance = pelicula
        )

        if formulario.is_valid():
            formulario.save()
            return redirect('listar_peliculas')
    else:
        formulario = PeliculaForm(instance = pelicula)

    return render(request, "pelicula/nueva_pelicula.html", {"formulario" : formulario})