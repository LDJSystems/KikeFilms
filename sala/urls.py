from django.urls import path
from .import views

urlpatterns = [
    #Gestión de sesiones
    path('agregar/',            views.agregar_sesion, name = 'agregar_sesion'),
    path('lista_sesiones/',     views.listar_sesiones, name = 'lista_sesiones'),
    path('<int:pk>/modificar/', views.modificar_sesion, name = 'modificar_sesion'),
    path('eliminar/<int:pk>/', views.eliminar_sesion, name='eliminar_sesion'),
    
    #Gestión de Salas(Solo Superusuario)
    path('salas/', views.listar_salas, name='lista_salas'),
    path('salas/nueva/', views.agregar_sala, name='agregar_sala'),
    path('salas/modificar/<int:pk>/', views.modificar_sala, name='modificar_sala'),
    path('salas/eliminar/<int:pk>/', views.eliminar_sala, name='eliminar_sala'),
]