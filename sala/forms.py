from django import forms
from .models import Sesion
from datetime import datetime, timedelta

class SesionForm(forms.ModelForm):
    class Meta:
        model = Sesion

        # Widgets utilizados para aplicar estilos de Bootstrap
        # y definir el tipo de entrada de fecha y hora.
        widgets = {
            'pelicula'     : forms.Select(attrs = {'class' : 'form-select'}),
            'sala'         : forms.Select(attrs = {'class' : 'form-select'}),
            'fecha_sesion' : forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
            'hora_sesion'  : forms.TimeInput(format='%H:%M', attrs={'class': 'form-control', 'type': 'time'}),
        }

        # Campos del modelo Sesion que podrán ser ingresados
        # y modificados mediante este formulario.
        fields = [
            'pelicula',
            'sala',
            'fecha_sesion',
            'hora_sesion',
        ]

    def clean(self):
        """Valida que una nueva sesión no se cruce con otra sesión
        existente en la misma sala y en la misma fecha.

        Primero obtiene los datos ya validados por Django. Después
        calcula la fecha y hora de inicio y finalización de la nueva
        sesión usando la duración de la película.

        Luego busca las sesiones existentes para la misma sala y fecha
        y calcula el intervalo de tiempo ocupado por cada una.

        Si el intervalo de la nueva sesión coincide o se cruza con el
        intervalo de una sesión existente, se genera un ValidationError
        y el formulario no podrá guardarse.

        Returns:
            dict: Datos validados del formulario."""

        
        # Se ejecutan primero las validaciones de ModelForm luego
        # recupera los datos que pasaron esas validaciones.
        cleaned_data = super().clean()
        pelicula = cleaned_data.get('pelicula')
        sala     = cleaned_data.get('sala')
        fecha    = cleaned_data.get('fecha_sesion')
        hora     = cleaned_data.get('hora_sesion')

        # Solo se comprueba el cruce de sesiones si todos los datos necesarios
        # están disponibles y han sido validados correctamente.
        if pelicula and sala and fecha and hora:

            # Uno la fecha y la hora para obtener un único momento de inicio de la nueva sesión.
            inicio_nueva_sesion = datetime.combine(fecha, hora)

            # Se Calcula cuándo terminará la nueva sesión
            # utilizando la duración de la película en minutos.
            fin_nueva_sesion = inicio_nueva_sesion + timedelta(minutes = pelicula.duracion)

            # Busco únicamente las sesiones de la misma sala
            # y del mismo día.
            sesiones_existentes = Sesion.objects.filter(
                sala = sala,
                fecha_sesion = fecha
            )

            if self.instance.pk:
                sesiones_existentes = sesiones_existentes.exclude(pk=self.instance.pk)

            # Comparo la nueva sesión contra cada sesión existente.
            for sesion in sesiones_existentes:

                # Calculo el momento exacto de inicio
                # de la sesión que ya está registrada.
                inicio_sesion_existente = datetime.combine(sesion.fecha_sesion, 
                                                        sesion.hora_sesion)

                # Calculo cuándo termina la sesión existente.
                fin_sesion_existente = inicio_sesion_existente + timedelta(minutes = sesion.pelicula.duracion)

                # Existe cruce de sesiones cuando la nueva sesión comienza antes
                # de que termine la existente y, al mismo tiempo, termina
                # después de que la sesión existente haya comenzado.
                if inicio_nueva_sesion < fin_sesion_existente and fin_nueva_sesion > inicio_sesion_existente:
                    raise forms.ValidationError(
                        'No es posible agregar la sesion: Sala ocupada en esta franja horaria!'
                    )
        # Django espera que clean() devuelva los datos validados.
        return cleaned_data