from django.urls import path
from app_mensajeria import views

urlpatterns = [
    path("enviar-mensaje/", views.enviar_mensaje, name="enviar-mensaje"),
    path("mostrar-mensaje/", views.mostrar_mensaje, name="mostrar-mensaje"),
]