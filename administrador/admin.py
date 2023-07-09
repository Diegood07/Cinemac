from django.contrib import admin
from .models import Peliculas,Imagen,Administradores
# Register your models here.

admin.site.register(Peliculas)
admin.site.register(Imagen)
admin.site.register(Administradores)