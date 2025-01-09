from django.db import models
# Create your models here.

from django.contrib.auth.models import User
"""agregar mas detalles a los cursos y a las demas clases como horarios, fechas, mas datos en otras clases"""

class Vuelo(models.Model):
    pass

class Equipaje(models.Model):
    pass

class Estadia(models.Model):
    pass


class Recomendaciones(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    fecha = models.DateField(default='2023-01-01')  # Definir un valor predeterminado aquí
    alojamiento = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return f"Nombre: {self.nombre} | Alojamiento: {self.alojamiento}"


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='media/perfil_img/', blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"

class Comentario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name='liked_comentarios', blank=True)

    def __str__(self):
        return f'{self.usuario.username} - {self.contenido[:20]}'

