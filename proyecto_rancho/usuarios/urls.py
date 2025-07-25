from django.urls import path
from .views import *

app_name = 'usuario_app'
urlpatterns = [
    path('/crear', crear_usuario, name='crear'),
    
]