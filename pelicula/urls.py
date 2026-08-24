from django.urls import path
from .views import PeliculaCreateView, InicioView

urlpatterns = [
    path('agregar/', PeliculaCreateView.as_view(), name='pelicula_create'),
    path('', InicioView.as_view(), name='inicio'),
]