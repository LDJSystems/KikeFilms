from django import forms
from .models import Sala, Sesion
from datetime import datetime, timedelta, date

class SalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = ['numero_sala', 'capacidad']
        widgets = {
            'numero_sala': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-white border-secondary',
                'placeholder': 'Ej. Sala 1'
            }),
            'capacidad': forms.NumberInput(attrs={
                'class': 'form-control bg-dark text-white border-secondary',
                'placeholder': 'Ej. 120'
            }),
        }


class SesionForm(forms.ModelForm):
    class Meta:
        model = Sesion

        # Widgets utilizados para aplicar estilos de Bootstrap
        # y definir el tipo de entrada de fecha y hora.
        widgets = {
            'pelicula'     : forms.Select(attrs = {'class' : 'form-select bg-dark text-white border-secondary'}),
            'sala'         : forms.Select(attrs = {'class' : 'form-select bg-dark text-white border-secondary'}),
            'fecha_sesion' : forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control bg-dark text-white border-secondary', 'type': 'date'}),
            'hora_sesion'  : forms.TimeInput(format='%H:%M', attrs={'class': 'form-control bg-dark text-white border-secondary', 'type': 'time'}),
        }

        # Campos del modelo Sesion que podrán ser ingresados
        # y modificados mediante este formulario.
        fields = [
            'pelicula',
            'sala',
            'fecha_sesion',
            'hora_sesion',
        ]

    def clean_fecha_sesion(self):
        """Valida que la fecha de la sesión no sea anterior a la fecha actual."""
        fecha = self.cleaned_data.get('fecha_sesion')
        if fecha and fecha < date.today():
            raise forms.ValidationError('No puedes programar una sesión en una fecha pasada.')
        return fecha

    def clean(self):
        """Valida que una nueva sesión no se cruce con otra sesión
        existente en la misma sala y en la misma fecha.

        Primero obtiene los datos ya validados por Django. Después
        calcula la fecha y hora de inicio y finalización de la nueva
        sesión usando la duración de la película sumando 20 minutos
        de margen de limpieza y desalojo.

        Luego busca las sesiones existentes para la misma sala abarcando
        un rango de +-1 día para evitar solapamientos a medianoche y
        calcula el intervalo de tiempo ocupado por cada una.

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

            # Se calcula cuándo terminará la nueva sesión
            # utilizando la duración de la película en minutos + 20 min de margen.
            fin_nueva_sesion = inicio_nueva_sesion + timedelta(minutes = pelicula.duracion + 20)

            # Busco las sesiones de la misma sala en un rango de +-1 día
            # para prevenir cruces con películas que terminan tras la medianoche.
            sesiones_existentes = Sesion.objects.filter(
                sala = sala,
                fecha_sesion__range = [fecha - timedelta(days=1), fecha + timedelta(days=1)]
            ).select_related('pelicula')

            if self.instance.pk:
                sesiones_existentes = sesiones_existentes.exclude(pk=self.instance.pk)

            # Comparo la nueva sesión contra cada sesión existente.
            for sesion in sesiones_existentes:

                # Calculo el momento exacto de inicio
                # de la sesión que ya está registrada.
                inicio_sesion_existente = datetime.combine(sesion.fecha_sesion, 
                                                        sesion.hora_sesion)

                # Calculo cuándo termina la sesión existente sumando sus 20 min de desalojo.
                fin_sesion_existente = inicio_sesion_existente + timedelta(minutes = sesion.pelicula.duracion + 20)

                # Existe cruce de sesiones cuando la nueva sesión comienza antes
                # de que termine la existente y, al mismo tiempo, termina
                # después de que la sesión existente haya comenzado.
                if inicio_nueva_sesion < fin_sesion_existente and fin_nueva_sesion > inicio_sesion_existente:
                    raise forms.ValidationError(
                        f"No es posible agregar la sesión: La Sala {sala.numero_sala} está ocupada por "
                        f"'{sesion.pelicula.titulo}' hasta las {fin_sesion_existente.strftime('%H:%M')} "
                        f"(incluyendo los 20 min de desalojo y limpieza)."
                    )
        # Django espera que clean() devuelva los datos validados.
        return cleaned_data