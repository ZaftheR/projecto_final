from django import forms 
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RecomendacionesFormulario(forms.ModelForm):
    class Meta:
        model = Recomendaciones
        fields = ["nombre", "fecha", "alojamiento", "descripcion"]
        
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control", "placeholder":"Ingrese el nombre"},),
            "fecha": forms.DateInput(attrs={"type": "date", "class": "form-conntrol", "placeholder":"AAAA/MM/DD"},),
            "alojamiento": forms.TextInput(attrs={"class": "form-control", "placeholder":"Ingrese el alojamiento y ubicación"},),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "placeholder":"Ingrese la descripcion"})
        }



class UserUpdateForms(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ["first_name","last_name", "email"]

class UserProfileForms(forms.ModelForm):
    
    class Meta:
        model = Perfil
        fields = ["imagen"]

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={'rows': 4, 'cols': 50}),
        }


class RegistroUsuarioForm(UserCreationForm):
    
    first_name = forms.CharField(max_length=30, required=True, help_text='Nombre')
    last_name = forms.CharField(max_length=30, required=True, help_text='Apellido')
    email = forms.EmailField(max_length=254, required=True, help_text='Correo electrónico')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
