from django.shortcuts import render
from pelicula.models import Pelicula

# Create your views here.
def inicio(request):
    peliculas = Pelicula.objects.all()
    return render(request, 'core/inicio.html', {'peliculas' : peliculas})