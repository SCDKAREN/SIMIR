from django import forms
from .models import *

class RegistroForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = ['apellido', 'nombre', 'documento', 'casino', 'comida']