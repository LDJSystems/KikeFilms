from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Pelicula
from .forms import PeliculaForm
from django.views.generic import ListView
from .models import Pelicula

class PeliculaCreateView(CreateView):
    model = Pelicula
    form_class = PeliculaForm
    template_name = 'pelicula/pelicula_form.html'
    success_url = reverse_lazy('pelicula_list')
    
class PeliculaListView(ListView):
    model = Pelicula
    template_name = 'pelicula/pelicula_list.html'
    context_object_name = 'peliculas'
    ordering = ['- fecha_lanzamiento']