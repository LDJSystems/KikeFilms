from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from core.decorators import gestor_required
from django.contrib import messages
from .models import Sala, Sesion
from .forms import SesionForm, SalaForm
from pelicula.models import Pelicula  # Importación añadida

# ==================== VISTAS DE SESIONES ====================

@login_required
@gestor_required
def agregar_sesion(request):
    if not Sala.objects.exists():
        messages.warning(request, "No hay salas registradas. Es necesario crear al menos una sala antes de agregar funciones.")
        return redirect('lista_sesiones')

    if request.method == 'POST':
        formulario = SesionForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "¡Sesión agregada con éxito!")
            return redirect('lista_sesiones')
    else:
        formulario = SesionForm()
    return render(request, 'sala/nueva_sesion.html', {'formulario': formulario})


def listar_sesiones(request):
    sesiones = Sesion.objects.select_related('pelicula', 'sala').all()
    peliculas = Pelicula.objects.all()
    salas = Sala.objects.all()
    return render(request, "sala/lista_sesiones.html", {
        "sesiones": sesiones,
        "peliculas": peliculas,
        "salas": salas,
    })


@login_required
@gestor_required
def modificar_sesion(request, pk):
    sesion = get_object_or_404(Sesion, pk=pk)

    if request.method == 'POST':
        formulario = SesionForm(request.POST, instance=sesion)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "¡Sesión modificada con éxito!")
        else:
            for field, errors in formulario.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    return redirect('lista_sesiones')


@login_required
@gestor_required
def eliminar_sesion(request, pk):
    sesion = get_object_or_404(Sesion, pk=pk)
    if request.method == 'POST':
        sesion.delete()
        messages.success(request, "¡Sesión eliminada con éxito!")
    return redirect('lista_sesiones')


# ==================== VISTAS DE SALAS (SUPERUSUARIO) ====================

@login_required
@user_passes_test(lambda u: u.is_superuser)
def listar_salas(request):
    salas = Sala.objects.all()
    formulario = SalaForm()
    return render(request, 'sala/lista_salas.html', {'salas': salas, 'formulario': formulario})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def agregar_sala(request):
    if request.method == 'POST':
        formulario = SalaForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "¡Sala creada con éxito!")
        else:
            for field, errors in formulario.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    return redirect('lista_salas')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def modificar_sala(request, pk):
    sala = get_object_or_404(Sala, pk=pk)
    if request.method == 'POST':
        formulario = SalaForm(request.POST, instance=sala)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "¡Sala modificada con éxito!")
        else:
            for field, errors in formulario.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    return redirect('lista_salas')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def eliminar_sala(request, pk):
    sala = get_object_or_404(Sala, pk=pk)
    if request.method == 'POST':
        sala.delete()
        messages.success(request, "¡Sala eliminada con éxito!")
    return redirect('lista_salas')