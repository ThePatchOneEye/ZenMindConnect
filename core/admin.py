from django.contrib import admin
from .models import Tipousuario, Especialidad, Persona, Psicologo, Horarios, Agenda, Post, Hilo, Comment, Notificacion, NotificacionSuperusuario
#Todas las tablas para manejarlas en el admin Django
admin.site.register(Tipousuario)
admin.site.register(Especialidad)
admin.site.register(Psicologo)
admin.site.register(Horarios)
admin.site.register(Agenda)
admin.site.register(Post)
admin.site.register(Hilo)
admin.site.register(Persona)
admin.site.register(Comment)
admin.site.register(Notificacion)
admin.site.register(NotificacionSuperusuario)
