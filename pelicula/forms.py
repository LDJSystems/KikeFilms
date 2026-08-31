from django import forms
from .models import Pelicula

class PeliculaForm(forms.ModelForm):
    class Meta:
        model = Pelicula

        widgets = {
            'portada_imagen'    : forms.ClearableFileInput(attrs= {'class': 'form-control'}),
            'titulo'            : forms.TextInput(attrs={'class' : 'form-control'}),
            'sinopsis'          : forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'director'          : forms.Select(attrs={'class': 'form-select'}),
            'genero'            : forms.SelectMultiple(attrs={'class': 'form-select'}),
            'duracion'          : forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha_lanzamiento' : forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
        }

        fields = [
            'portada_imagen',
            'titulo',
            'sinopsis', 
            'director', 
            'genero', 
            'duracion',
            'fecha_lanzamiento', 
            ]