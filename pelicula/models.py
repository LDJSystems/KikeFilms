from django.db import models

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
    portada_imagen    = models.ImageField(blank = True, null = True, upload_to = "pelicula/")
    titulo            = models.CharField("Titulo", max_length = 255)
    genero            = models.ManyToManyField(Genero)
    duracion          = models.IntegerField("Duracion")
    sinopsis          = models.TextField("Sinopsis")
    director          = models.ForeignKey(Director, on_delete = models.CASCADE)
    fecha_lanzamiento = models.DateField("Fecha de lanzamiento")

    def __str__(self):
       return f"{self.titulo} - {self.director}"
