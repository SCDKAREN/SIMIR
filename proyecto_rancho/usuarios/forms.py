from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['last_name', 'first_name', 'casino', 'dni', 'username', 'password', 'is_superuser']