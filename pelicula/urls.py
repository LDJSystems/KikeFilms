from django.urls import path
from .views import PeliculaCreateView

urlpatterns = [
    path('agregar/', PeliculaCreateView.as_view(), name='pelicula_create'),
    path('', PeliculaCreateView.as_view(), name='pelicula_list'),
]