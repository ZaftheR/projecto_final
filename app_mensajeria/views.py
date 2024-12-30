from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Mensaje
# Create your views here.

def enviar_mensaje(request):
    
    if request.method == 'POST':
        destinatario_username = request.POST.get('destinatario')
        contenido = request.POST.get('contenido')
        destinatario = User.objects.get(username=destinatario_username)
        Mensaje.objects.create(remitente=request.user, destinatario=destinatario, contenido=contenido)
        return redirect('mostrar-mensaje')
    
    usuarios = User.objects.exclude(username=request.user.username)
        
    return render(request, 'app_mensajeria/enviar-mensaje.html',  {'usuarios':usuarios})


def mostrar_mensaje(request):
    
    mensajes = Mensaje.objects.filter(destinatario=request.user).order_by('-fecha_envio')
    
    return render(request, 'app_mensajeria/mostrar-mensaje.html', {'mensajes':mensajes})