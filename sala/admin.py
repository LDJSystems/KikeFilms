from django.contrib import admin
from .models import Sala, Sesion

# Register your models here.

@admin.register(Sesion)

class SesionAdmin(admin.ModelAdmin):
    #Voy a mostrar en pantalla
    list_display = (
        "numero_sala",
        "titulo_pelicula",
        "fecha_sesion",
        "hora_sesion",
    )

    #Opciones de busqueda
    search_fields = (
        "pelicula__titulo",
    )

    #Lista de posibles filtros
    list_filter =(
        "sala",
        "fecha_sesion",
        "hora_sesion",

    )

    def titulo_pelicula(self, obj):
        return obj.pelicula.titulo

    def numero_sala(self, obj):
        return obj.sala.numero_sala

@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    pass