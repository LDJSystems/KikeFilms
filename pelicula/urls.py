from django.urls import path
from .import views

urlpatterns = [
    path('listar_peliculas/',   views.listar_peliculas, name = 'listar_peliculas'),
    path('agregar/',            views.agregar_pelicula, name = 'agregar_pelicula'),
    path('<int:pk>/modificar/', views.modificar_pelicula, name = 'modificar_pelicula'),
    path('<int:pk>/eliminar/',  views.eliminar_pelicula, name = 'eliminar_pelicula'),
]