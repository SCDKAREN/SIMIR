from django.contrib import admin
from .models import *


@admin.register(Usuario)
class RegistroUsuarios(admin.ModelAdmin):
    list_display = ('username', 'last_name', 'first_name', 'dni', 'casino', 'is_superuser')
    search_fields = ('last_name', 'first_name', 'dni', 'casino')
    list_filter = ('casino', 'dni')
    ordering = ('last_name',)
    
