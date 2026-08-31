from django.urls import path
from .import views

urlpatterns = [
    path('agregar/',            views.agregar_sesion, name = 'agregar_sesion'),
    path('lista_sesiones/',     views.listar_sesiones, name = 'lista_sesiones'),
    path('<int:pk>/modificar/', views.modificar_sesion, name = 'modificar_sesion'),
    path('eliminar/<int:pk>/', views.eliminar_sesion, name='eliminar_sesion'),
]