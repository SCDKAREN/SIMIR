import datetime
from django.shortcuts import render, redirect
from .forms import RegistroForm
from .models import Comida
from django.db.models import Q, F
from django.http import JsonResponse
from .models import Registro
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
        try:
            form = RegistroForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('registro:registro_exitoso')  # Asegúrate de tener esta vista o URL
            else:
                print("Formulario no válido:", form.errors)
        except Exception as e:
            print(f"Error al guardar el registro: {e}")
            return redirect('registro:crear_registro')
    else:
        form = RegistroForm()
    
    return render(request, 'registro/crear_registro.html', {'form': form})

    
def reporte_mensual_view(request):
    context = {
        
    }
    return render(request,"reporte_mensual.html",{'data': context})

def registro_datatable(request):
    draw = request.GET.get('draw')
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    order_column_index = int(request.GET.get('order[0][column]', 0))
    order_direction = request.GET.get('order[0][dir]', 'asc')
    search_value = request.GET.get('search[value]', None)

    # Mapeo de índices a columnas del datatable
    column_mapping = {
        0: 'fecha_hora', 
        1: 'apellido', 
        2: 'nombre', 
        3: 'documento', 
        4: 'casino', 
        5: 'comida',
    }

    order_column = column_mapping.get(order_column_index, 'apellido')
    if order_direction == 'desc':
        order_column = F(order_column).asc(nulls_last=True)
    else:
        order_column = F(order_column).desc(nulls_last=True)

    # Construimos dinámicamente las condiciones de búsqueda utilizando Q objects
    conditions = Q()
    if search_value:
        fields = [
            'documento', 'apellido', 'casino', 'comida'  # Cambio aquí para buscar por user_made
        ]
        search_terms = search_value.split()
        for term in search_terms:
            term_conditions = Q()
            for field in fields:
                term_conditions |= Q(**{f"{field}__icontains": term})

            conditions &= term_conditions



    filtered_data = Registro.objects.all()
    filtered_data = filtered_data.order_by(order_column)
    total_records = filtered_data.count()

    data = [
        item.to_json()
        for item in filtered_data[start: start + length]
    ]   

    return JsonResponse({
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data
    })
