from django.shortcuts import render, redirect
from .forms import RegistroForm

# Create your views here.

def registrar(request):
    form = RegistroForm(request.POST)
    return render(request,"registrar.html",{'form': form})

def crear_registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        print("todo bien")
        if form.is_valid():
            
            form.save()
            return redirect('registro:registro_exitoso')  # Asegúrate de tener esta vista o URL
    else:
        form = RegistroForm()
    
    return render(request, 'registro/crear_registro.html', {'form': form})
