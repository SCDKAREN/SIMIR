from django.urls import path
from .views import *

app_name = 'usuario_app'
urlpatterns = [
    path('crear/', crear_usuario_view, name='crear_formulario'),
    path('crear-usuario/', crear_usuario, name='crear'),

]