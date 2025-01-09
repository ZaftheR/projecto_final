from app_viaje import views
from django.urls import path

urlpatterns = [
    
    #----funciones para mostrar perfiles, editar perdiles y cambiar contraseñas----
    path('ver-perfil/', views.ver_perfil, name="ver-perfil"),
    path('editar-perfil/', views.editar_perfil, name="editar-perfil"),
    path('editar-contraseña/', views.editar_contraseña, name="editar-contraseña"),
    
    #----funciones para registro, iniciar y cerrar sesion----
    path('iniciar_sesion/', views.iniciar_sesion, name="iniciar-sesion"),
    path('cerrar_sesion/', views.cerrar_sesion, name="cerrar-sesion"),
    path('registrar_usuario/', views.registrar_usuario, name="registrar-usuario"),
    
    #----funciones para ver informacion----
    path('Vuelo/', views.vuelo, name='vuelo'),
    path('', views.inicio, name= 'inicio'),
    path('equipaje/', views.equipaje, name= 'equipaje'),
    path('estadia/', views.estadia, name= 'estadia'),
    path('recomendaciones/', views.recomendaciones, name= 'recomendaciones'),
    
    #----formularios para agregar información----
    path('recomendaciones-formulario/', views.formulario_recomendaciones, name= 'recomendaciones-formulario'),
    
    #----funciones para mostrar comentarios----
    path('comentarios/', views.lista_comentarios, name='lista_comentarios'),
    path('crear_comentario/', views.crear_comentario, name='crear_comentario'),
    path('like/<int:pk>/', views.like_comentario, name='like_comentario'),
    path('eliminar/<int:pk>/', views.eliminar_comentario, name='eliminar_comentario'),
    path('editar/<int:pk>/', views.editar_comentario, name='editar_comentario'),
    
    #----funciones de Recomendaciones----
    path('recomencadiones-eliminar/<int:pk>/', views.eliminar_recomendaciones, name= 'recomendaciones-eliminar'),
    path('recomendaciones-editar/<int:pk>/', views.editar_recomendaciones, name= 'recomendaciones-editar'),
    path('ver-recomendaciones/<int:pk>/', views.ver_recomendaciones, name='recomendaciones-ver'),
    
    #----funciones sobre mi----
    path('sobre-mi/', views.sobre_mi, name='sobre-mi'),
]