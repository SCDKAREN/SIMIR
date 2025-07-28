from django.shortcuts import render, redirect
from .forms import RegistroForm
from .models import Comida
# Create your views here.

def login_view(request):
    return render(request, "login.html")

def registrar(request):
    usuario = request.user
    comida = Comida.objects.get(id=1)  # Asumiendo que tienes un objeto Comida con id=1
    # if not usuario.is_authenticated:
    #     return redirect('login')
    form = RegistroForm(request.POST)
    return render(request,"registrar.html",{'form': form, 'usuario': usuario, 'comida': comida})

def crear_registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registro:registro_exitoso')  # Asegúrate de tener esta vista o URL
    else:
        form = RegistroForm()
    
    return render(request, 'registro/crear_registro.html', {'form': form})

    
def reporte_mensual_view(request):
    context = {
        
    }
    return render(request,"reporte_mensual.html",{'data': context})
