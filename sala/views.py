from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from core.decorators import gestor_required
from django.contrib import messages
from .models import Sala,Sesion
from pelicula.models import Pelicula
from .forms import SesionForm

# Create your views here.

#Agregar Sesion
def agregar_sesion(request):
    if request.method == 'POST':
        formulario = SesionForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Sesion agregada con exito!")
            return redirect('agregar_sesion')
    else:
        formulario = SesionForm()
    return render(request, 'sala/nueva_sesion.html', {'formulario' : formulario})

#Listar todas las sesiones
def listar_sesiones(request):
    sesiones = Sesion.objects.all()
    peliculas = Pelicula.objects.all()
    salas = Sala.objects.all()

    contexto = {
        "sesiones": sesiones,
        "peliculas": peliculas,
        "salas": salas,
    }

    return render(
        request,
        "sala/lista_sesiones.html",
        contexto
    )

#Modificar sesion
@login_required
@gestor_required
def modificar_sesion(request, pk):
    sesion = get_object_or_404(Sesion, pk = pk)

    if request.method == 'POST':
        formulario = SesionForm(
            request.POST,
            instance = sesion #Le digo a django que quiero modificar una instancia de sesion y no crear una nueva
        )

        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Sesion modificada con exito!")
            return redirect('lista_sesiones')
        else:
            messages.error(request, "No es posible modificar la sesión: la sala está ocupada en esa franja horaria.")
            return redirect('lista_sesiones')

    else:
        formulario = SesionForm(instance = sesion)

    return render(request, 'sala/lista_sesiones.html', {'formulario' : formulario})