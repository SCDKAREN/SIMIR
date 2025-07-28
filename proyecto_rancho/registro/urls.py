from django.urls import path
from .views import *

app_name = 'registro_app'
urlpatterns = [
    path('registrar/', registrar, name='registro'),
    path('crear/', crear_registro, name='crear'),
    path('reporte-mensual/', reporte_mensual_view, name='reporte_mensual'),
]