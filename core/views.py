from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, Http404
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .models import Post, Comment, Notificacion, NotificacionSuperusuario, Persona, Tipousuario
from .forms import CommentForm, PostForm, PersonaForm  # Agrega tus formularios aquí
from .helpers import send_forget_password_mail, send_welcome_email, send_account_deletion_notification, send_account_mydeletion_notification #Para los correos
from .AI import predecir_sentimiento  # Importa la función predecir_sentimiento desde AI.py
from .comment_processing import procesar_comentario  # Nueva importación
import uuid



@csrf_exempt
def detectar_sentimiento(request):
    if request.method == 'POST':
        comentario_id = request.POST.get('comentario_id')
        comentario = Comment.objects.get(id=comentario_id)

        # Obtén el texto del comentario
        texto_comentario = comentario.body

        # Procesa el comentario
        sentimiento_predicho = procesar_comentario(comentario)

        # Acciones basadas en el sentimiento predicho
        if sentimiento_predicho == 'negativo':
            # Notificar al superusuario de Django
            superusuario_django = User.objects.filter(is_superuser=True).first()
            if superusuario_django:
                notificacion_superusuario = Notificacion.objects.create(
                    contenido=f"Comentario negativo detectado en la publicación de {comentario.author.user.username}",
                    comentario=comentario
                )

        return JsonResponse({'sentimiento': sentimiento_predicho})
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)




# Añade esta función a tu archivo views.py
# Importa HttpResponse


# Añade esta función a tu archivo views.py
def index(request):
    notificaciones_no_leidas = []
    notificaciones_superusuario_no_leidas = []

    if hasattr(request.user, 'persona'):
        persona = request.user.persona
        notificaciones_no_leidas = persona.notificacion_set.filter(leida=False)

    if request.user.is_superuser:
        notificaciones_superusuario_no_leidas = NotificacionSuperusuario.objects.filter(leida=False)

    # Define si el anuncio debe mostrarse o no (puedes ajustar esta lógica según tus necesidades)
    mostrar_anuncio = True
    video_anuncio = True  # Ajusta según tu lógica

    # Agrega el banner de anuncio al contexto
    context = {
        'notificaciones_no_leidas': notificaciones_no_leidas,
        'notificaciones_superusuario_no_leidas': notificaciones_superusuario_no_leidas,
        'mostrar_anuncio': mostrar_anuncio,
        'video_anuncio': video_anuncio,
    }
    # Devuelve la respuesta con el banner de anuncio
    return render(request, 'core/index.html', context)




def mostrar_notificaciones(request):
    if request.user.is_authenticated:
        notificaciones = Notificacion.objects.filter(persona=request.user.persona, leida=False)
    else:
        notificaciones = []

    return render(request, 'mostrar_notificaciones.html', {'notificaciones': notificaciones})

def marcar_notificacion_leida(request, notificacion_id):
    notificacion = get_object_or_404(Notificacion, id=notificacion_id)
    notificacion.leida = True
    notificacion.save()
    return JsonResponse({'mensaje': 'Notificación marcada como leída con éxito'})

def marcar_notificacion_superusuario(request, notificacion_id):
    notificacion = get_object_or_404(NotificacionSuperusuario, id=notificacion_id)
    notificacion.leida = True
    notificacion.save()
    # Realiza otras acciones según sea necesario
    return JsonResponse({'mensaje': 'Notificación del superusuario marcada como leída con éxito'})

def eliminar_notificacion(request, notificacion_id):
    notificacion = get_object_or_404(Notificacion, id=notificacion_id)
    notificacion.delete()
    return JsonResponse({'mensaje': 'Notificación eliminada con éxito'})

def not_found_view(request, exception=None):
    return render(request, 'NOTFOUND.html', status=404)

def nos(request):
    return render(request,'core/nos.html')

def coming_son(request):
    return render(request,'core/coming_son.html')

def form_persona(request):
    return render(request,'core/form_persona.html')


def log(request):
    return render(request,'core/log.html')







def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        c = request.POST.get('password')

        user = authenticate(username=u, password=c)

        if user is not None:
            if user.is_active:
                login(request, user)
                #messages.success(request, '¡Inicio de sesión exitoso!')
                return redirect('index')
            else:
                messages.error(request, 'Usuario Inactivo')
        else:
            messages.error(request, 'Usuario y/o contraseña incorrecta ❌')

    return render(request, 'core/log.html')















def logout_view(request):
    logout(request)
    return redirect('index')

def lista_usuarios(request):
    personas= Persona.objects.all()
    return render(request,'core/lista_usuarios.html',context={'datos':personas})





@login_required
def eliminar_cuenta_usuario(request):
    try:
        # Obtén la persona asociada al usuario actual
        persona = request.user.persona
        # Obtén el usuario asociado a la persona
        user = persona.user
        # Envía el correo de notificación antes de eliminar la cuenta
        send_account_mydeletion_notification(persona.correo)
        # Elimina la persona y el usuario
        persona.delete()
        user.delete()
        # Cierra la sesión
        logout(request)
        messages.success(request, "Tu cuenta ha sido eliminada exitosamente 🗑️")
        messages.info(request, "Cuenta eliminada. Por favor, inicia sesión con otra cuenta.")
    except Persona.DoesNotExist:
        messages.error(request, "La persona no existe ❌")
    except User.DoesNotExist:
        messages.error(request, "El usuario no existe ❌")

    return redirect('log')  # Ajusta el nombre de la ruta según tu configuración de URLs





def form_borrar_persona(request, id):
    try:
        persona = Persona.objects.get(rut=id)
        # Obtén el usuario asociado a la persona
        user = persona.user
        # Envía el correo de notificación antes de eliminar la cuenta
        send_account_deletion_notification(persona.correo)
        # Elimina la persona y el usuario
        persona.delete()
        user.delete()
        messages.success(request, "Usuario eliminado exitosamente 🗑️")
    except Persona.DoesNotExist:
        messages.error(request, "La persona no existe ❌")
    except User.DoesNotExist:
        messages.error(request, "El usuario no existe ❌")

    return redirect('lista_usuarios')



def frontpage(request):
    # Recupera las publicaciones y asegúrate de que tengan un idPost válido
    posts = Post.objects.all()
    for post in posts:
        if not post.idPost:
            post.idPost = 0
        post.save()

    # Verifica si hay mensajes y si hay al menos uno de éxito relacionado con la publicación
    success_messages = [m for m in messages.get_messages(request) if 'success' in m.tags and 'Publicado!' in m.message]

    return render(request, 'core/frontpage.html', {'posts': posts, 'success_messages': success_messages})



def form_post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            if request.user.persona.tipousuario_id == 2:
                post = post_form.save(commit=False)
                original_slug = slugify(post.title)
                max_length = 50
                if len(original_slug) > max_length:
                    original_slug = original_slug[:max_length]

                slug = original_slug
                counter = 1
                while Post.objects.filter(slug=slug).exists():
                    counter += 1
                    slug = f"{original_slug}-{counter}"

                slug = slugify(request.user.username)
                post.slug = slug

                post.author = request.user.persona
                post.save()

                # Configura el mensaje solo después de publicar con éxito
                messages.success(request, "Publicado!")

                return redirect('frontpage')
            else:
                raise Http404("No tienes permiso para publicar.")
    else:
        post_form = PostForm(initial={'slug': slugify(request.user.username)}, use_required_attribute=False)

    return render(request, 'core/form_post.html', {'post_form': post_form})




def form_mod_post(request, post_id):
    try:
        # Obtén el post por su ID
        post = Post.objects.get(idPost=post_id)

        # Almacena el slug original
        original_slug = post.slug

        # Verifica si el usuario es el autor del post
        if request.user.is_authenticated and request.user.persona == post.author:
            if request.method == 'POST':
                # Si el formulario se envía, procesa los datos
                formulario = PostForm(data=request.POST, instance=post)

                # Elimina el campo 'slug' del formulario para evitar validaciones
                del formulario.fields['slug']

                if formulario.is_valid():
                    # Restaura el slug original antes de guardar el formulario
                    post.slug = original_slug
                    formulario.save()
                    messages.success(request, "El post ha sido modificado exitosamente ✔️ Publicado!")
                    return redirect('frontpage')  # Redirige al usuario a donde desees después de guardar los cambios

            else:
                # Si el formulario no se ha enviado, muestra el formulario con los datos actuales del post
                formulario = PostForm(instance=post)

                # Elimina el campo 'slug' del formulario para evitar validaciones
                del formulario.fields['slug']

            datos = {
                'form': formulario,
                'post': post,
            }
            return render(request, 'core/form_mod_post.html', datos)
        else:
            raise Http404("No tienes permiso para editar esta publicación.")
    except Post.DoesNotExist:
        raise Http404("La publicación que intentas editar no existe.")

def form_borrar_post(request, id):
    post = get_object_or_404(Post, idPost=id)  # Obtén el post o muestra un error 404 si no existe

    post.delete()
    messages.success(request, "El post ha sido eliminado exitosamente ✔️")
    return redirect('frontpage')



def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post

            if not request.user.is_superuser:
                comment.author = request.user.persona  # Establece el autor del comentario
                comment.save()

                # Crea una notificación para el autor del post
                notificacion = Notificacion.objects.create(
                    persona=post.author,
                    contenido=f"Nuevo comentario en tu publicación: '{post.title}'",
                    comentario=comment
                )

            messages.success(request, "Comentario publicado!")
            return redirect('post_detail', slug=post.slug)
    else:
        form = CommentForm()

        if request.user.is_authenticated and not request.user.is_superuser:
            form.fields['nombre_del_autor'].initial = request.user.persona.nombre

    return render(request, 'core/post_detail.html', {'post': post, 'form': form})
    
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    messages.success(request, "El comentario ha sido eliminado.")
    return redirect('post_detail', slug=comment.post.slug)

def editar_comentario(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == "POST":
        if request.user == comment.author.user:
            nuevo_comentario = request.POST.get("edited_comment")
            nuevo_comentario_name = request.POST.get("edited_comment_name")
            comment.name = nuevo_comentario_name
            comment.body = nuevo_comentario
            comment.save()
            messages.success(request, "Comentario ha sido editado!")
        else:
            messages.error(request, "No tienes permiso para editar este comentario.")

    return redirect('post_detail', slug=comment.post.slug)





@login_required
def changepassword_login(request):
    context = {}

    try:
        usuario_actual = request.user
        context = {'user_rut': usuario_actual.persona.rut}

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_rut = request.POST.get('user_rut')

            if user_rut is None:
                messages.success(request, 'Usuario no encontrado.❌')
                return redirect('changepassword')

            if new_password != confirm_password:
                messages.success(request, 'Ambas contraseñas deben ser iguales.⚠️')
                return redirect('changepassword')

            user_obj = User.objects.get(id=user_rut)
            user_obj.set_password(new_password)
            user_obj.save()
            messages.success(request, 'Contraseña cambiada exitosamente.✔️')
            return redirect('log')

    except Exception as e:
        print(e)
        messages.error(request, 'Error al cambiar la contraseña.❌')
        return redirect('log')

    return render(request, 'core/changepassword_login.html', context)






def changepassword(request , token):
    context = {}
    try:
        usuario_obj = Persona.objects.filter(contrasena = token).first()
        context = {'user_rut' : usuario_obj.rut}
        
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_rut = request.POST.get('user_rut')
            
            if user_rut is  None:
                messages.success(request, 'Usuario con encontrado.❌')
                return redirect(f'changepassword/{token}/')
                
            
            if  new_password != confirm_password:
                messages.success(request, 'Ambas contraseñas deben ser iguales.⚠️')
                return redirect(f'changepassword/{token}/')
                         
            
            user_obj = User.objects.get(id = user_rut)
            user_obj.set_password(new_password)
            user_obj.save()
            messages.success(request, 'Has recuperado tu contraseña.✔️')
            return redirect('log')
    except Exception as e:
        print(e)
    return render(request , 'core/changepassword.html' , context)




def forgetpassword(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            
            # Verificar si existe un usuario con el nombre proporcionado
            persona_obj = Persona.objects.filter(nombre=username).first()
            
            if not persona_obj:
                messages.error(request, 'Usuario no encontrado con este nickname. ❌')
                return redirect('forgetpassword')
            
            # Generar un token único
            token = str(uuid.uuid4())
            
            # Actualizar la contraseña de la Persona con el token generado
            persona_obj.contrasena = token
            persona_obj.save()
            
            # Enviar correo electrónico con el token
            send_forget_password_mail(persona_obj.correo, token)
            
            messages.success(request, 'El email ha sido enviado, revisa tu bandeja de entrada o SPAM.✔️')
            return redirect('forgetpassword')
                
    except Exception as e:
        print(e)
    
    return render(request, 'core/forgetpassword.html')



#registrar usuario
def registrar_usuario(request):
    if request.method == 'POST':
        rut_p = request.POST['Rut']
        nombre_p = request.POST['nombre']
        apellido_p = request.POST['apellido']
        fechnac_p = request.POST['fechnac']
        email_p = request.POST['email']
        telefono_p = request.POST['Telefono']
        ccontra_p = request.POST['password']
        ccontra_confirm = request.POST['password_confirm']
        tipousuario_p = Tipousuario.objects.get(idTipoUsuario=2)

        # Verificar si ya existe un usuario con el mismo "username" (nickname)
        if User.objects.filter(username=nombre_p).exists():
            messages.error(request, 'El nickname ya está en uso. Por favor, elige otro ❗⚠️📢.')
            return redirect('form_persona')

        # Verificar si ya existe un usuario con el mismo "Rut"
        if Persona.objects.filter(rut=rut_p).exists():
            messages.error(request, 'El Rut ya está registrado. Por favor, elige otro ❗⚠️📢.')
            return redirect('form_persona')

        if Persona.objects.filter(telefono=telefono_p).exists():
            messages.error(request, 'El Telefono ya está registrado. Por favor, elige otro ❗⚠️📢.')
            return redirect('form_persona')

        if Persona.objects.filter(correo=email_p).exists():
            messages.error(request, 'El correo ya está registrado. Por favor, elige otro ❗⚠️📢.')
            return redirect('form_persona')

        if ccontra_p != ccontra_confirm:
            messages.error(request, 'Las contraseñas no coinciden. Por favor, inténtalo de nuevo ❗⚠️📢.')
            return redirect('form_persona')
            
        # Si no existe, crea el nuevo usuario
        user = User.objects.create_user(id=rut_p, username=nombre_p, password=ccontra_p, first_name=nombre_p, email=email_p, is_staff=1, is_superuser=0)
        
        # Luego, crea la Persona y asocia el usuario
        persona = Persona(rut=rut_p, nombre=nombre_p, apellido=apellido_p, fechaNac=fechnac_p, correo=email_p, telefono=telefono_p, contrasena=ccontra_p, tipousuario=tipousuario_p, user=user)
        persona.save()

        # Envía el correo de bienvenida
        send_welcome_email(email_p)
        messages.success(request, 'Usuario creado con éxito ✔️')
        return redirect('log')
    else:
        # Maneja el caso en que el método de la solicitud no sea POST
        return redirect('form_persona')

    #------------------------------------------

def form_mod_persona(request):
    # Obtener el usuario actualmente autenticado
    usuario = request.user

    try:
        # Obtener el objeto Persona correspondiente al usuario
        persona = Persona.objects.get(user=usuario)
    except Persona.DoesNotExist:
        # Manejar el caso en el que el perfil no existe
        persona = None

    try:
        # Obtener el objeto User correspondiente al usuario
        user = User.objects.get(username=usuario.username)
    except User.DoesNotExist:
        # Manejar el caso en el que el usuario no existe
        user = None

    if request.method == 'POST':
        # Si el formulario se envía, procesar los datos
        formulario = PersonaForm(data=request.POST, instance=persona)
        if formulario.is_valid():
            # Validar si el Rut ya está en uso
            new_rut = formulario.cleaned_data.get('rut')
            if Persona.objects.exclude(user=user).filter(rut=new_rut).exists():
                messages.error(request, 'El Rut ya está registrado. Por favor, elige otro ❗⚠️📢.')
                return redirect('form_mod_persona')

            # Validar si el correo electrónico ya está en uso
            new_email = formulario.cleaned_data.get('correo')
            if Persona.objects.exclude(user=user).filter(correo=new_email).exists():
                messages.error(request, 'El correo ya está registrado. Por favor, elige otro ❗⚠️📢.')
                return redirect('form_mod_persona')

            # Validar si el número de teléfono ya está en uso
            new_telefono = formulario.cleaned_data.get('telefono')
            if Persona.objects.exclude(user=user).filter(telefono=new_telefono).exists():
                messages.error(request, 'El número de teléfono ya está registrado. Por favor, elige otro ❗⚠️📢.')
                return redirect('form_mod_persona')



    
            perfil = formulario.save(commit=False)
            perfil.user = usuario
            perfil.save()

            # Actualizar campos del modelo User
            if user:
                user.email = new_email
                user.username = formulario.cleaned_data['nombre']
                user.save()

            messages.success(request, "Perfil modificado exitosamente ✔️")
            return redirect('log')  # Redirige al usuario a donde desees después de guardar los cambios

    else:
        # Si el perfil no existe, mostrar el formulario de creación de perfil
        if not persona:
            formulario = PersonaForm()
        else:
            # Si el perfil existe, mostrar el formulario con los datos actuales del perfil
            formulario = PersonaForm(instance=persona)

    datos = {'form': formulario}
    return render(request, 'core/form_mod_persona.html', datos)





