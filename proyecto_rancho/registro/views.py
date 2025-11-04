import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import RegistroForm
from .models import Comida
from .utils import *
from django.db.models import Q, F
from django.http import JsonResponse
from .models import Registro, Casino
# Create your views here.

@never_cache
def login_view(request):
    # Si el usuario ya está autenticado, redirigirlo directamente
    print("Usuario en sesión:", request.user)
    if request.user.is_authenticated:
        if request.user.es_administrador:
            return redirect("registro_app:reporte_mensual")
        else:
            return redirect("registro_app:registro")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.es_administrador:
                return redirect("registro_app:reporte_mensual")
            else:
                return redirect("registro_app:registro")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")

    return render(request, "login.html")

def logout_view(request):
    logout(request)  # elimina la sesión del usuario
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect("login")  # cambia "login" por el nombre de tu url de login

@login_required(login_url='login') 
def registrar(request):
    usuario = request.user
    comidas = Comida.objects.all()  
    if not usuario.is_authenticated:
        return redirect('login')
    # Si son entre las 6 y 10 de la mañana redirigir a pagina de formulario no habilitado
    hora_actual = datetime.datetime.now().time()
    hora_inicio = datetime.time(6, 0)
    hora_fin = datetime.time(10, 0)
    context = {}
    form_activado_hasta = cache.get('formulario_activado_hasta')
    activo_globalmente = False
    if form_activado_hasta and datetime.datetime.now() < form_activado_hasta:
        activo_globalmente = True
    print("Formulario activado hasta:", form_activado_hasta)
    # Verificar si la hora actual está dentro del rango
    if not (hora_inicio <= hora_actual <= hora_fin or activo_globalmente):
        context = {
            'no_habilitado': True,
        }
    form = RegistroForm(request.POST)
    return render(request,"registrar.html",{'form': form, 'usuario': usuario, 'comidas': comidas, 'data': context if context else {}})


@login_required(login_url='login')  # redirige al login si no está autenticado
def registro_exitoso(request):
    logout(request)  
    return render(request, 'registro_exitoso.html')

@login_required(login_url='login')  # redirige al login si no está autenticado    
def reporte_mensual_view(request):
    usuario=request.user
    hora_actual = datetime.datetime.now().time()
    hora_inicio = datetime.time(7, 0)
    hora_fin = datetime.time(10, 0)
    form_activado_hasta = cache.get('formulario_activado_hasta')
    print("Formulario activado hasta:", form_activado_hasta)

    if form_activado_hasta:
        form_activado = True
        hora = form_activado_hasta.strftime('%H:%M')
    else:
        if (hora_inicio <= hora_actual <= hora_fin):
            form_activado = None
        else:
            form_activado = False
    print('form_activado:', form_activado)
    if usuario.es_administrador == False:
        return redirect('registro_app:registro')
    context = {
        'comidas': Comida.objects.all(),
        'casinos': Casino.objects.all(),
        'fecha_hoy': datetime.date.today().strftime('%d/%m/%Y'),
        'hero': True,
        'form_activado': form_activado,
        'hora': hora if form_activado else None
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
    filtro_fecha  = request.GET.get('fecha')

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
            'documento', 
        ]
        search_terms = search_value.split()
        for term in search_terms:
            term_conditions = Q()
            for field in fields:
                term_conditions |= Q(**{f"{field}__icontains": term})

            conditions &= term_conditions

    filtered_data = Registro.objects.filter(conditions)
    
    # Aplicamos filtros dinámicos
    if filtro_comida:
        filtered_data = filtered_data.filter(comida=filtro_comida)
    if filtro_casino:
        filtered_data = filtered_data.filter(casino=filtro_casino)
    if filtro_fecha:
        try:
            fecha_obj = datetime.datetime.strptime(filtro_fecha, '%Y-%m-%d').date()
            filtered_data = filtered_data.filter(fecha_hora__date=fecha_obj)
        except ValueError:
            print("Formato de fecha inválido:", filtro_fecha)
    else:
        hoy = datetime.date.today()
        filtered_data = filtered_data.filter(fecha_hora__date=hoy)
        
    filtered_data = filtered_data.order_by(order_column)
    total_records = filtered_data.count()

    # Paginación
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

