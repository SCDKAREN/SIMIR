#Archivo signal para generar instancias de Comida al hacer el primer migrate
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import Comida
from django.conf import settings

@receiver(post_migrate)
def create_initial_comidas(sender, **kwargs):
    if sender.name == 'registro':
        if not Comida.objects.exists():
            for comida_nombre in settings.COMIDAS:
                Comida.objects.create(nombre=comida_nombre)
            print("Comidas iniciales creadas.")
        else:
            print("Las comidas ya existen, no se crearon nuevas.")