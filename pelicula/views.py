from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
            messages.success(request, "Pelicula añadida con exito!")
            return redirect('listar_peliculas')
    else:
        formulario = PeliculaForm()
    return render(request, 'pelicula/nueva_pelicula.html', {'formulario' : formulario})

#Listado de Peliculas (con búsqueda opcional)
def listar_peliculas(request):
    query = request.GET.get('q', '').strip()
    buscando = len(query) > 0
    resultados = None

    if buscando:
        resultados = Pelicula.objects.filter(titulo__icontains=query)

    peliculas = Pelicula.objects.all()

    return render(request, 'pelicula/lista.html', {
        'peliculas': peliculas,
        'resultados': resultados,
        'q': query,
        'buscando': buscando,
    })

#Modificar Pelicula
@login_required
@gestor_required
def modificar_pelicula(request, pk):
    pelicula = get_object_or_404(Pelicula, pk = pk) #Recoge la pk de la pelicula que recibio y la busca en la base de datos
                                                    #Si no la encuentra, se detiene la ejecucion 

    if request.method == 'POST': #Valido que el formulario no se haya enviado vacio
        formulario = PeliculaForm(
            request.POST, 
            request.FILES,
            instance = pelicula 
        )

        if formulario.is_valid(): #Valido que se esten cumpliendo todas las reglas del modelo
            formulario.save()
            messages.success(request, 'Pelicula Modificada con exito!')
            return redirect('listar_peliculas')
    else:
        formulario = PeliculaForm(instance = pelicula)

    return render(request, "pelicula/nueva_pelicula.html", {"formulario" : formulario})

#Eliminar Pelicula
@login_required
@gestor_required
def eliminar_pelicula(request, pk):
    pelicula = get_object_or_404(Pelicula, pk = pk)

    if request.method == 'POST':
        pelicula.delete()
        messages.success(request, 'Pelicula Eliminada con exito!')
        return redirect('listar_peliculas')

    return render(request, 'pelicula/', {'pelicula' : pelicula})