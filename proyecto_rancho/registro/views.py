import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import RegistroForm
from .models import Comida
from django.db.models import Q, F
from django.http import JsonResponse
from .models import Registro, Casino
# Create your views here.

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        print("Intentando login con:", username, password)
        print("Resultado authenticate:", user)

        if user is not None:
            login(request, user)
            return redirect("registro_app:registro")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    return render(request, "login.html")

    return render(request, "login.html")  # tu template de login

def logout_view(request):
    logout(request)  # elimina la sesión del usuario
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect("login")  # cambia "login" por el nombre de tu url de login

def registrar(request):
    usuario = request.user
    comidas = Comida.objects.all()  
    # if not usuario.is_authenticated:
    #     return redirect('login')
    form = RegistroForm(request.POST)
    return render(request,"registrar.html",{'form': form, 'usuario': usuario, 'comidas': comidas})

def crear_registro(request):
    fecha_hoy = datetime.date.today()
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            documento = form.cleaned_data['documento']
            comidas_ids = request.POST.getlist('comida')
            print("Comidas seleccionadas:", comidas_ids)
            # Creamos un objeto base sin guardar
            registro_base = form.save(commit=False)
            
            # Validación: ya existe registro para este documento en estas comidas hoy?
            registros_existentes = Registro.objects.filter(
                documento=documento,
                fecha_hora__date=fecha_hoy,
                comida_id__in=comidas_ids,
            )

            if registros_existentes.exists():
                # Ya está registrado para al menos una de esas comidas hoy
                messages.error(request, "Ya te has anotado hoy en una de las comidas seleccionadas.")
                return redirect('registro_app:registro')
            else:
                for comida_id in comidas_ids:
                    comida = Comida.objects.get(id=comida_id)
                    registro = Registro(
                        **{
                            campo.name: getattr(registro_base, campo.name)
                            for campo in Registro._meta.fields
                            if campo.name not in ('id', 'comida', 'fecha_hora')
                        }
                    )
                    registro.comida = comida
                    registro.save()
                return redirect('registro_app:registro_exitoso')
        else:
            print("Formulario no válido:", form.errors)
    else:
        form = RegistroForm()
    
    return render(request, 'registro/crear_registro.html', {'form': form})

def registro_exitoso(request):
    logout(request)  # elimina la sesión del usuario
    return render(request, 'registro_exitoso.html')

    
def reporte_mensual_view(request):
    context = {
        'comidas': Comida.objects.all(),
        'casinos': Casino.objects.all(),
    }
    
    return render(request,"reporte_mensual.html",{'data': context})

def registro_datatable(request):
    draw = request.GET.get('draw')
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    order_column_index = int(request.GET.get('order[0][column]', 0))
    order_direction = request.GET.get('order[0][dir]', 'asc')
    search_value = request.GET.get('search[value]', None)

    filtro_comida = request.GET.get('comida')
    filtro_casino = request.GET.get('casino')

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

    hoy = datetime.date.today()

    filtered_data = Registro.objects.filter(
        fecha_hora__date=hoy
    ).filter(conditions)
    
      # Aplicamos filtros dinámicos
    if filtro_comida:
        filtered_data = filtered_data.filter(comida=filtro_comida)
    if filtro_casino:
        filtered_data = filtered_data.filter(casino=filtro_casino)
    
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
