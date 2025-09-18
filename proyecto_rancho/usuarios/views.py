from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import UsuarioForm
from .models import Casino
# Create your views here.

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
                return redirect('registro_app:login')
        except Exception as e:
            messages.error(request, f'Error al crear el usuario: {e}')
            return redirect('usuario_app:crear_formulario')
    else:
        form = UsuarioForm()
    return redirect('usuario_app:crear_formulario')
