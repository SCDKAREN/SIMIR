from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.cache import never_cache

from .forms import UsuarioForm
from .models import Casino
# Create your views here.

@never_cache
def crear_usuario_view(request):
    context = {
        'casinos':  Casino.objects.all(),
        'form': UsuarioForm(),
    }
    return render(request,"crear_usuario.html",{'data': context})

def crear_usuario(request):
    if request.method == 'POST':
        try:
            form = UsuarioForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Usuario creado exitosamente')
                return redirect('login')
            else:
                if 'username' in form.errors:
                    messages.error(request, 'El nombre de usuario ya existe. Por favor, elija otro.')
                if 'dni' in form.errors:
                    messages.error(request, 'El documento ya se encuentra registrado. Por favor, verifique el número de documento.')
                return redirect('usuario_app:crear_formulario')
        except Exception as e:
            print("Error al crear el usuario:", e)
            messages.error(request, f'Error al crear el usuario: {e}')
            return redirect('usuario_app:crear_formulario')
    else:
        form = UsuarioForm()
    return redirect('usuario_app:crear_formulario')
