from django.contrib import admin
from .models import *

admin.site.register(Casino)

admin.site.register(Comida)

@admin.register(Registro)
class RegistroAdmin(admin.ModelAdmin):
    list_display = ('apellido', 'nombre', 'documento', 'casino', 'confirmado', 'fecha_hora')
    search_fields = ('apellido', 'nombre', 'documento', 'casino')
    list_filter = ('confirmado', 'casino', 'comida')
    ordering = ('-fecha_hora',)
    
    