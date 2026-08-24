from django.contrib import admin
from django import forms
from django.db import models
from .models import Pelicula, Director, Genero
from .models import obtener_fecha_limite

# Register your models here.

@admin.register(Pelicula)

class PeliculasAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.DateField: {
            "widget" : forms.DateInput(attrs = {"type" : "date",
                                                "max"  : obtener_fecha_limite().isoformat()})
        },
    }

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

@admin.register(Director)

class DirectorAdmin(admin.ModelAdmin):
    pass

@admin.register(Genero)

class GeneroAdmin(admin.ModelAdmin):
    pass