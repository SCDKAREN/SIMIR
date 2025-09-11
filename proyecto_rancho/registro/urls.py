from django.urls import path
from .views import *

app_name = 'registro_app'
urlpatterns = [
    path("/", login_view, name="login"),
    path('registrar/', registrar, name='registro'),
    path('crear/', crear_registro, name='crear'),
    path('reporte-mensual/', reporte_mensual_view, name='reporte_mensual'),
    path('datatable/',registro_datatable,name='datatable')
]