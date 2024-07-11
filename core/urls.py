from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import form_persona,form_borrar_persona,eliminar_cuenta_usuario,form_mod_persona,form_post, form_mod_post, form_borrar_post, registrar_usuario, index, nos, coming_son, log, login_view, logout_view, lista_usuarios, forgetpassword,changepassword, frontpage, post_detail, editar_comentario, changepassword_login
from . import reserva
from .reserva import adm
from .views import form_mod_persona
from . import views
from .views import detectar_sentimiento
from .views import marcar_notificacion_superusuario

urlpatterns=[   
    path('log',log, name='log'),
    path('registrar_usuario',registrar_usuario,name="registrar_usuario"),
    path('login/',LoginView.as_view(template_name='core/log.html'),name="login"),
    path('sesion',login_view,name="sesion"),
    path('logout',logout_view,name="logout"),
    path('lista_usuarios', lista_usuarios, name='lista_usuarios'), 
    path('form_borrar_persona/<str:id>/', form_borrar_persona, name='form_borrar_persona'),
    path('eliminar_cuenta_usuario/', eliminar_cuenta_usuario, name='eliminar_cuenta_usuario'),
    path('',index, name='index'),
    path('nos',nos, name='nos'),
    path('coming_son',coming_son, name='coming_son'),
    path('form_persona',form_persona,name='form_persona'),
    path('form_mod_persona/', form_mod_persona, name='form_mod_persona'),
    path('forgetpassword', forgetpassword ,name="forgetpassword"),
    path('changepassword/<token>/', changepassword, name='changepassword'),
    path('changepassword/', changepassword_login, name="changepassword_login"),
    path('frontpage', views.frontpage, name='frontpage'),
    path('form_post', views.form_post, name='form_post'),
    path('form_mod_post/<int:post_id>/', views.form_mod_post, name='form_mod_post'),
    path('form_borrar_post/<int:id>/', views.form_borrar_post, name='form_borrar_post'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('editar_comentario/<int:comment_id>/', views.editar_comentario, name='editar_comentario'),
    path('marcar-notificacion-superusuario-leida/<int:notificacion_id>/', marcar_notificacion_superusuario, name='marcar_notificacion_superusuario_leida'),
    path('marcar-notificacion-leida/<int:notificacion_id>/', views.marcar_notificacion_leida, name='marcar_notificacion_leida'),
    path('eliminar-notificacion/<int:notificacion_id>/', views.eliminar_notificacion, name='eliminar_notificacion'),
    path('psicologo/new/', reserva.registrar_psicologo, name='registrar_psicologo'), 
    path('especialidad/new/', reserva.registrar_especialidad, name='registrar_especialidad'),
    path('horarios/new/', reserva.insertar_horarios, name='insertar_horarios'),
    path('agenda/new/', reserva.crear_nueva_agenda, name='crear_nueva_agenda'),
    path('listar_agendas', reserva.listar_agendas, name='listar_agendas'),
    path('detallar_agenda/<int:id>/', reserva.detallar_agenda, name='detallar_agenda'),
    path('adm',adm, name='adm'),
    path('autenticar_persona', reserva.autenticar_persona, name='autenticar_persona'),
    path('area_de_persona/<int:id>/',reserva.area_de_persona, name= 'area_de_persona'),
    path('marcar_consulta/<int:id>/<int:pk>/',reserva.marcar_consulta, name='marcar_consulta'),
    path('detectar_sentimiento/', detectar_sentimiento, name='detectar_sentimiento'),  # Agregado: Nueva ruta para detectar_sentimiento
]


