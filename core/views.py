from django.views.generic import ListView
from pelicula.models import Pelicula

class HomeView(ListView):
    model = Pelicula
    template_name = "core/inicio.html"
    context_object_name = 'peliculas'
    ordering = ['-fecha_lanzamiento']