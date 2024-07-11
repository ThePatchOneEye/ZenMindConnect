# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from .AI import predecir_sentimiento
# Procesamiento de comentario usando señales


# En models.py
class Especialidad(models.Model):
    nombre = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.nombre

class Psicologo(models.Model):
    nombre = models.CharField(max_length=200, blank=False, null=False)
    rut = models.CharField(max_length=30, blank=False, null=False, unique=True)
    email = models.EmailField()
    telefono = models.CharField(max_length=17)
    especialidad = models.ForeignKey(Especialidad, on_delete= models.CASCADE, verbose_name='Especialidad',blank=False)

    def __str__(self):
        return self.nombre

class Horarios(models.Model):
    HORA_CHOISES = (
        ('08:00AM⛅','08:00AM⛅'),
        ('09:00AM⛅','09:00AM⛅'),
        ('10:00AM⛅','10:00AM⛅'),
        ('11:00AM⛅','11:00AM⛅'),
        ('12:00PM☀️','12:00PM☀️'),
        ('13:00PM☀️','13:00PM☀️'),
        ('14:00PM☀️','14:00PM☀️'),
        ('15:00PM☀️','15:00PM☀️'),
        ('16:00PM☀️','16:00PM☀️'),
        ('17:00PM🌄','17:00PM🌄'),
        ('18:00PM🌄','18:00PM🌄'),
        ('19:00PM🌄','19:00PM🌄')
        
    )
    horas = models.CharField(max_length=9,choices=HORA_CHOISES, blank=False, null=False)

    def __str__(self):
        return self.horas

class Agenda(models.Model):
    psicologo = models.ForeignKey(Psicologo, on_delete=models.CASCADE, verbose_name='Psicologo Especialista',blank=False)
    data = models.DateField()
    horarios = models.ManyToManyField(Horarios, blank= False)

    def __str__(self):
        return str(self.psicologo.nombre)


class Hilo(models.Model):
    idTiphilo = models.AutoField(primary_key=True, verbose_name='Id Hilo', unique=True)
    nombreHilo = models.CharField(max_length=50, verbose_name='Nombre hilo')

    def __str__(self):
        return self.nombreHilo




class Tipousuario(models.Model):
    idTipoUsuario = models.AutoField(primary_key=True, verbose_name='Id_tipo_usuario', unique=True)
    tipoUsuario = models.CharField(max_length=50, verbose_name='Tipo_usuario')

    def __str__(self):
        return self.tipoUsuario







class Persona(models.Model):
    rut = models.CharField(max_length=12, primary_key=True, verbose_name='Rut_usuario', unique=True)
    nombre = models.CharField(max_length=20, verbose_name='Nombre_usuario')
    apellido = models.CharField(max_length=20, verbose_name='Apellido_usuario')
    fechaNac = models.DateField(max_length=10, verbose_name='Nacimiento_usuario')
    correo = models.EmailField(max_length=50, verbose_name='Correo_usuario')
    telefono = models.CharField(max_length=12, verbose_name='telefono_psicologo')
    contrasena = models.CharField(max_length=36, verbose_name='Contrasena_usuario')
    tipousuario = models.ForeignKey(Tipousuario, on_delete=models.CASCADE)
    consulta = models.ManyToManyField(Agenda, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.rut





class Post(models.Model):
    idPost = models.AutoField(primary_key=True, verbose_name='Id Post', unique=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=50)  # Define la longitud máxima
    intro = models.TextField()
    body = models.TextField()
    hilo = models.ForeignKey(Hilo, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Persona, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date_added']

    def save(self, *args, **kwargs):
        # Generar un slug único basado en el título
        if not self.slug:
            self.slug = slugify(self.title)

        # Verificar si el slug ya existe y agregar un sufijo numérico si es necesario
        original_slug = self.slug
        count = 1
        while Post.objects.filter(slug=self.slug).exists():
            self.slug = f"{original_slug}-{count}"
            count += 1

        # Asegurarse de que el slug no supere la longitud máxima
        if len(self.slug) > self._meta.get_field('slug').max_length:
            self.slug = self.slug[:self._meta.get_field('slug').max_length]

        super().save(*args, **kwargs)




class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Persona, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['date_added']



class Notificacion(models.Model):
    contenido = models.TextField()
    comentario = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True, related_name='notificaciones')
    leida = models.BooleanField(default=False)
    persona = models.ForeignKey('Persona', on_delete=models.CASCADE)

    def __str__(self):
        return self.contenido



class NotificacionSuperusuario(models.Model):
    contenido = models.TextField()
    comentario = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True, related_name='notificaciones_superusuario')
    leida = models.BooleanField(default=False)

    def __str__(self):
        return self.contenido



@receiver(post_save, sender=Comment)
def procesar_comentario(sender, instance, **kwargs):
    comentario = instance
    sentimiento_predicho = predecir_sentimiento(comentario.body)

    # Acciones basadas en el sentimiento predicho
    if sentimiento_predicho == 'negativo':
        # Notificar al superusuario de Django
        superusuario_django = User.objects.filter(is_superuser=True).first()
        if superusuario_django:
            notificacion_superusuario = NotificacionSuperusuario.objects.create(
            contenido=f"Comentario <span style='color: red; font-weight: bold;'>negativo</span> detectado en la publicación de:",
            comentario=comentario
            )       


