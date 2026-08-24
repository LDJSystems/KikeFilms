from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

def obtener_fecha_limite():
    """Esta funcion trae la fecha limite luego de calcular la actual
        y sumarle los dos años de limite """
    fecha_actual = timezone.localdate()
    fecha_limite = fecha_actual.replace(year = fecha_actual.year + 2)
    return fecha_limite

def validar_fecha_lanzamiento(fecha):
    """Esta funcion va a recibir una fecha desde el admin,
       sera la encargada de revisar que la fecha que ingresa 
       el usuario no supere los dos años partiendo de la fecha actual"""

    fecha_actual = timezone.localdate()
    #Esta linea asigna una fecha limite. la cual no puede superar los dos años a partir del año actual
    fecha_limite = obtener_fecha_limite()

    if fecha > fecha_limite:
        raise ValidationError("Fecha fuera de rango")

class Director(models.Model):
    nombre   = models.CharField("Nombre", max_length = 150)
    apellido = models.CharField("Apellido", max_length = 150)

    class Meta:
        """Uso esta clase meta para corregir el error de
            singular y plural"""
        verbose_name        = "Director"
        verbose_name_plural = "Directores"

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Genero(models.Model):
    nombre_genero = models.CharField("Nombre Genero", max_length = 50)

    def __str__(self):
        return self.nombre_genero

class Pelicula(models.Model):
    portada_imagen    = models.ImageField(blank = True, null = True, upload_to = "./pelicula")
    titulo            = models.CharField("Titulo", max_length = 255)
    genero            = models.ManyToManyField(Genero)
    duracion          = models.IntegerField("Duracion")
    sinopsis          = models.TextField("Sinopsis")
    director          = models.ForeignKey(Director, on_delete = models.CASCADE)
    fecha_lanzamiento = models.DateField("Fecha de lanzamiento", validators=[validar_fecha_lanzamiento])

    def __str__(self):
       return f"{self.titulo} - {self.director}"
