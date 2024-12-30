from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
# from django.contrib.auth.decorators import login_required

from .models import Recomendaciones, Comentario, Perfil , Vuelo, Estadia, Equipaje
from .forms import Comentario, RecomendacionesFormulario, UserUpdateForms, UserProfileForms, RegistroUsuarioForm



#Funciones para iniciar,registrar,ver , cerrar, editar perfil y cambiar contraseña

def iniciar_sesion(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        contraseña = request.POST.get('contraseña')
        user = authenticate(request, username=usuario, password=contraseña)
        print(user)
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido {usuario}')
            return redirect('inicio')
        else:
            return render(request, 'app_viaje/forms/iniciar_sesion.html', {'error': 'Credenciales inválidas'})
    else:
        return render(request, 'app_viaje/forms/iniciar_sesion.html')


@login_required
def editar_perfil(request):
    
    perfil, _ = Perfil.objects.get_or_create(user=request.user)
    perfil_form = UserProfileForms(request.POST, request.FILES, instance=perfil)
    
    if request.method == 'POST':
        form = UserUpdateForms(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            perfil_form.save()
            return redirect('ver-perfil') 
    else: 
        form = UserUpdateForms(instance=request.user)
        perfil_form = UserProfileForms(instance=perfil)
    return render(request, 'app_viaje/forms/editar-perfil.html', {"form":form ,"perfil_form":perfil_form}) #Es el renderizado para las templates de la seccion Perfil

@login_required
def editar_contraseña(request):
    
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contraseña actualizada correctamente')
            update_session_auth_hash(request, form.user)
            return redirect('ver-perfil')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'app_viaje/forms/editar-contraseña.html', {"form":form})

def cerrar_sesion(request):
        logout(request)
        messages.success(request, 'Sesión cerrada correctamente')
        return redirect('iniciar-sesion')

@login_required
def ver_perfil(request):
    perfil = Perfil.objects.get(user=request.user)
    return render(request, 'app_viaje/ver-perfil.html', {'perfil': perfil})

def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            return redirect('iniciar-sesion')  # Redirige a una página de inicio después del registro
    else:
        form = RegistroUsuarioForm()
    return render(request, 'app_viaje/forms/registrar_usuario.html', {'form': form})


#-----Funciones para mostrar las secciones de la pagina-----

@login_required
def vuelo(request):
    return render(request, 'app_viaje/vuelo.html') #Es el renderizado para las templates de la seccion vuelo

def inicio(request):
    return render(request, 'app_viaje/index.html') #Es el renderizado para las templates de la seccion Inicio

@login_required
def estadia(request):
    return render(request, 'app_viaje/estadia.html',) #Es el renderizado para las templates de la seccion estadia

@login_required
def equipaje(request):
    return render(request, 'app_viaje/equipaje.html') #Es el renderizado para las templates de la seccion equipaje

@login_required
def recomendaciones(request):
    
    query = request.GET.get('q')
    if query:   
        recomendaciones =  Recomendaciones.objects.filter(nombre__icontains=query) | Recomendaciones.objects.filter(alojamiento__icontains=query)
    else:
        recomendaciones = Recomendaciones.objects.all() 
    return render(request, 'app_viaje/recomendaciones.html', {'recomendaciones':recomendaciones}) #Es el renderizado para las templates de la seccion recomendaciones


#-----Funciones para ingresar informacion a la BD -----

@login_required
def formulario_recomendaciones(request):
    
    if request.method == "POST":
        recomendaciones_form = RecomendacionesFormulario(request.POST)
        
        if recomendaciones_form.is_valid():
            info_limpia = recomendaciones_form.cleaned_data
            recomendaciones = Recomendaciones(nombre=info_limpia["nombre"], fecha=info_limpia["fecha"], alojamiento=info_limpia["alojamiento"], descripcion=info_limpia["descripcion"])
            recomendaciones.usuario = request.user
            recomendaciones.save()
            return redirect("recomendaciones")
    else:
        recomendaciones_form = RecomendacionesFormulario()
    
    return render(request, 'app_viaje/forms/recomendaciones-formulario.html', {"form": recomendaciones_form})


#-----Funciones para mostrar, editar y eliminar comentarios-----

@login_required
def lista_comentarios(request):
    comentarios = Comentario.objects.all().order_by('-fecha_publicacion')
    return render(request, 'app_viaje/lista_comentarios.html', {'comentarios': comentarios})

@login_required
def like_comentario(request, pk):
    comentario = get_object_or_404(Comentario, pk=pk)
    if request.method == 'POST':
        if request.user in comentario.liked_by.all():
            comentario.liked_by.remove(request.user)
            comentario.likes -= 1
            user_liked = False
        else:
            comentario.liked_by.add(request.user)
            comentario.likes += 1
            user_liked = True
        comentario.save()
        return redirect('lista_comentarios')
    return redirect('lista_comentarios')

@login_required
def crear_comentario(request):
    if request.method == 'POST':
        contenido = request.POST.get('contenido')
        if contenido:
            comentario = Comentario(usuario=request.user, contenido=contenido)
            comentario.save()
            return redirect('lista_comentarios')
    return redirect('lista_comentarios')

@login_required
def eliminar_comentario(request, pk):
    comentario = get_object_or_404(Comentario, pk=pk)
    if comentario.usuario == request.user:
        comentario.delete()
        return redirect('lista_comentarios')
    else:
        return redirect('lista_comentarios')

@login_required
def editar_comentario(request, pk):
    comentario = get_object_or_404(Comentario, pk=pk)
    
    if comentario.usuario != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para editar este comentario.")
    
    if request.method == 'POST':
        contenido = request.POST.get('contenido')
        if contenido:
            comentario.contenido = contenido
            comentario.save()
            return redirect('lista_comentarios')
    return render(request, 'app_viaje/forms/editar_comentario.html', {'comentario': comentario})


#-----Funciones para eliminar informacion-----

@login_required
def editar_recomendaciones(request, pk):
    recomendacion = get_object_or_404(Recomendaciones, pk=pk) 
    
    if recomendacion.usuario != request.user and not request.user.is_superuser: 
        return HttpResponseForbidden("No tienes permiso para editar esta recomendación.")
    
    if request.method == "POST":
        recomendaciones_form = RecomendacionesFormulario(request.POST, instance=recomendacion)
        if recomendaciones_form.is_valid():
            recomendaciones_form.save()
            return redirect("recomendaciones")
    else:
        recomendaciones_form = RecomendacionesFormulario(instance=recomendacion)
    
    return render(request, "app_viaje/forms/editar-recomendaciones.html", {"form": recomendaciones_form})

@login_required
def eliminar_recomendaciones(request, pk):
    recomendaciones = get_object_or_404(Recomendaciones, pk=pk)
    if recomendaciones.usuario != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("No tienes permiso para eliminar esta recomendación.")
    
    if request.method == "POST":
        recomendaciones.delete()
        return redirect('recomendaciones')
    
    return render(request, 'app_viaje/forms/eliminar_recomendaciones.html', {'recomendaciones': recomendaciones})

@login_required
def ver_recomendaciones(request, pk):
    recomendacion = get_object_or_404(Recomendaciones, pk=pk)
    return render(request, 'app_viaje/detalle_recomendacion.html', {'recomendacion': recomendacion})

#-----Funciones para mostrar acerca de mi-----

def sobre_mi(request):
    return render(request, 'app_viaje/sobre_mi.html')







