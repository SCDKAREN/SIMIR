from django.db import models
from django.contrib.auth.models import AbstractUser
from registro.models import Casino

# Create your models here.

class Usuario(AbstractUser):
    casino = models.ForeignKey(Casino, on_delete = models.CASCADE, related_name = 'usuarios', null=True)
    dni = models.CharField(max_length=10, unique=True, null=True)
    
    es_administrador = models.BooleanField(default=False)
        
    def _str_(self):
        return self.username