from django.shortcuts import render
from pelicula.models import Pelicula

# Create your views here.
def inicio(request):
    query = request.GET.get('q', '').strip()
    if query:
        peliculas = Pelicula.objects.filter(titulo__icontains=query)
    else:
        peliculas = Pelicula.objects.all()

    return render(request, 'core/inicio.html', {'peliculas' : peliculas, 'q': query})