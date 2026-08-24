from django.contrib import admin
from .models import Pelicula, Director, Genero

# Register your models here.

@admin.register(Pelicula)

class PeliculasAdmin(admin.ModelAdmin):
    filter_horizontal = ("genero",) # Organiza dos bloques de filtros para la seleccion del genero de la pelicula

    list_display = (
        "titulo",
        "director",
        "duracion",
        "fecha_lanzamiento",
    )

    search_fields = (
        "titulo",
        "director",
    )

    list_filter = (
        "genero",
        "director",
        "fecha_lanzamiento",
    )