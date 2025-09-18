from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['last_name', 'first_name', 'casino', 'dni', 'username', 'password', 'is_superuser']
        
    def save(self, commit=True):
        user = super().save(commit=False)
        # Hashear la contraseña
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user