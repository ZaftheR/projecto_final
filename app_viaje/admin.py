from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Perfil)
admin.site.register(Vuelo)
admin.site.register(Estadia)
admin.site.register(Equipaje)
admin.site.register(Recomendaciones)

class ComentarioAdmin(admin.ModelAdmin): 
    list_display = ('usuario', 'fecha_publicacion', 'likes')
    search_fields = ('usuario__username', 'contenido')

class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'imagen')