from django.db import models

class Sala(models.Model):
    numero_sala = models.CharField(max_length=50, unique=True, verbose_name="Número de sala")
    capacidad = models.IntegerField(verbose_name="Capacidad")

    def __str__(self):
        return f"Sala {self.numero_sala} ({self.capacidad} asientos)"

class Sesion(models.Model):
    pelicula = models.ForeignKey('pelicula.Pelicula', on_delete=models.CASCADE, related_name='sesiones', verbose_name="Película")
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='sesiones', verbose_name="Sala") # Borrado en cascada
    fecha_sesion = models.DateField(verbose_name="Fecha de la sesión")
    hora_sesion = models.TimeField(verbose_name="Hora de la sesión")

    class Meta:
        verbose_name = "Sesión"
        verbose_name_plural = "Sesiones"
        ordering = ['fecha_sesion', 'hora_sesion']
        constraints = [
            models.UniqueConstraint(
                fields=['sala', 'fecha_sesion', 'hora_sesion'],
                name='unique_sesion_sala_horario'
            )
        ]

    def __str__(self):
        return f"{self.pelicula.titulo} - Sala {self.sala.numero_sala} ({self.fecha_sesion} {self.hora_sesion.strftime('%H:%M')})"