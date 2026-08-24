from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from .models import Pelicula
from .forms import PeliculaForm
from django.views.generic import TemplateView
from django.views.generic import ListView

class PeliculaCreateView(CreateView):
    model = Pelicula
    form_class = PeliculaForm
    template_name = 'pelicula/pelicula_form.html'
    success_url = reverse_lazy('pelicula_list')

class PeliculaListView(ListView):
    model = Pelicula
    template_name = 'pelicula/inicio.html'
    context_object_name = 'peliculas'
    ordering = ['-fecha_lanzamiento']

class InicioView(ListView):
    model = Pelicula
    template_name = 'core/inicio.html'
    context_object_name = 'peliculas'
    ordering = ['-fecha_lanzamiento']