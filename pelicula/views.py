from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.decorators import gestor_required
from .models import Pelicula
from .forms import PeliculaForm

# Crear nueva pelicula
@login_required
@gestor_required
def agregar_pelicula(request):
    if request.method == 'POST':
        formulario = PeliculaForm(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "¡Pelicula añadida con éxito!")
            return redirect('listar_peliculas')
    else:
        formulario = PeliculaForm()
    return render(request, 'pelicula/nueva_pelicula.html', {'formulario' : formulario})

# Listado de Peliculas (con búsqueda opcional)
def listar_peliculas(request):
    query = request.GET.get('q', '').strip()
    buscando = len(query) > 0
    
    peliculas_base = Pelicula.objects.prefetch_related('sesion_set__sala')

    resultados = None
    if buscando:
        resultados = peliculas_base.filter(titulo__icontains=query)

    peliculas = peliculas_base.all()

    return render(request, 'pelicula/lista.html', {
        'peliculas': peliculas,
        'resultados': resultados,
        'q': query,
        'buscando': buscando,
    })

# Modificar Pelicula
@login_required
@gestor_required
def modificar_pelicula(request, pk):
    pelicula = get_object_or_404(Pelicula, pk=pk)

    if request.method == 'POST':
        formulario = PeliculaForm(
            request.POST, 
            request.FILES,
            instance=pelicula 
        )

        if formulario.is_valid():
            formulario.save()
            messages.success(request, '¡Pelicula modificada con éxito!')
            return redirect('listar_peliculas')
    else:
        formulario = PeliculaForm(instance=pelicula)

    return render(request, "pelicula/nueva_pelicula.html", {"formulario" : formulario})

# Eliminar Pelicula
@login_required
@gestor_required
def eliminar_pelicula(request, pk):
    pelicula = get_object_or_404(Pelicula, pk=pk)

    if request.method == 'POST':
        pelicula.delete()
        messages.success(request, '¡Pelicula eliminada con éxito!')
        return redirect('listar_peliculas')

    return render(request, 'pelicula/eliminar_pelicula.html', {'pelicula' : pelicula})