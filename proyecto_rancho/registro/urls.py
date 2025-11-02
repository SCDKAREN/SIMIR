from django.urls import path
from .views import *

app_name = 'registro_app'
urlpatterns = [
    path("", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path('registrar/', registrar, name='registro'),
    path('registro-exitoso/', registro_exitoso, name='registro_exitoso'),
    path('crear/', crear_registro, name='crear'),
    path('reporte-mensual/', reporte_mensual_view, name='reporte_mensual'),
    path('configurar-comidas/', config_comidas, name='config_comidas'),
    path('registro-no-habilitado/', registro_no_habilitado_view, name='registro_no_habilitado'),
    path('datatable/',registro_datatable,name='datatable')
]