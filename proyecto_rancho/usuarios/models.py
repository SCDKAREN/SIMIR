from django.db import models
from django.contrib.auth.models import AbstractUser
from registro.models import Casino

# Create your models here.

class Usuario(AbstractUser):
    casino = models.ForeingKey(Casino, on_delete = models.CASCADE, related_name = 'usuarios')
    es_usuarioBasico = models.BooleanField(default=False)
    es_administrador = models.BooleanField(default=False)

    def _str_(self):
        return self.username