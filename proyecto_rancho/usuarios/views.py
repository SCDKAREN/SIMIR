from django.shortcuts import render
from .forms import UsuarioForm
# Create your views here.
def crear_usuario(request):
    form = UsuarioForm(request.POST)
    return render(request,"crear_usuario.html",{'form': form})
