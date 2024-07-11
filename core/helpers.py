from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ValidationError


#Mail para la bienvenioda 
def send_welcome_email(email):
    try:
        subject = 'Bienvenido a ZenMindConnect'
        
        # Cuerpo del mensaje con formato HTML
        message = f"""
            <html>
                <head>
                    <style>
                        /* Puedes agregar estilos CSS aquí */
                        body {{
                            font-family: 'Arial', sans-serif;
                            background: linear-gradient(to bottom, #4b908e, #ffffff, #4b908e);
                            color: #fff;
                            padding: 20px;
                        }}
                        .container {{
                            max-width: 600px;
                            margin: 0 auto;
                            background: linear-gradient(to bottom, #4b908e, #ffffff, #4b908e);
                            padding: 20px;
                            border-radius: 10px;
                            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                            text-align: center;
                        }}
                        h1 {{
                            color: #808080;  /* Gris intenso */
                        }}
                        p {{
                            color: #000;  /* Negro */
                            font-size: 16px;
                            line-height: 1.5;
                            margin-bottom: 20px;
                        }}
                        img {{
                            max-width: 100%;
                            height: auto;
                            margin-bottom: 20px;
                        }}
                        .zenmindconnect-text {{
                            color: #001F3F;  /* Azul marino */
                            font-size: 36px;
                            font-weight: bold;
                            margin-top: 10px;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <!-- Reemplaza 'URL_DEL_LOGO' con el enlace directo a tu logotipo -->
                        <img src="https://i.postimg.cc/RCWybCKM/logo-final.png" alt="Logo de ZenMindConnect">
                        <div class="zenmindconnect-text">ZenMindConnect</div>
                        <h1>¡Bienvenido/a a ZenMindConnect!</h1>
                        <p>Gracias por registrarte en nuestra plataforma.</p>
                    </div>
                </body>
            </html>
        """
        
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        
        # Especifica el tipo de contenido como HTML
        send_mail(subject, '', email_from, recipient_list, html_message=message)
        return True
    except ValidationError as e:
        print(f'Error al enviar el correo electrónico de bienvenida: {e}')
        return False





#Mail para recuperar la contraseña 
def send_forget_password_mail(email, token):
    try:
        subject = 'Aquí tienes tu enlace para recuperar tu contraseña | ZenMindConnect'
        
        # Cuerpo del mensaje con formato HTML
        message = f"""
            <html>
                <head>
                    <style>
                        /* Puedes agregar estilos CSS aquí */
                        body {{
                            font-family: 'Arial', sans-serif;
                            background: linear-gradient(to bottom, #4b908e, #ffffff, #4b908e);
                            color: #fff;
                            padding: 20px;
                        }}
                        .container {{
                            max-width: 600px;
                            margin: 0 auto;
                            background: linear-gradient(to bottom, #4b908e, #ffffff, #4b908e);
                            padding: 20px;
                            border-radius: 10px;
                            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                            text-align: center;
                        }}
                        h1 {{
                            color: #808080;  /* Gris intenso */
                        }}
                        p {{
                            color: #000;  /* Negro */
                            font-size: 16px;
                            line-height: 1.5;
                            margin-bottom: 20px;
                        }}
                        img {{
                            max-width: 100%;
                            height: auto;
                            margin-bottom: 20px;
                        }}
                        .zenmindconnect-text {{
                            color: #001F3F;  /* Azul marino */
                            font-size: 36px;
                            font-weight: bold;
                            margin-top: 10px;
                        }}
                        .reset-link {{
                            display: inline-block;
                            padding: 10px 20px;
                            background-color: #FFA500;  /* Naranja */
                            color: #fff;
                            text-decoration: none;
                            border-radius: 5px;
                            font-size: 16px;
                            margin-top: 20px;
                        }}
                        .key-icon {{
                            font-size: 24px;
                            color: #fff;
                            margin-left: 5px;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <!-- Reemplaza 'URL_DEL_LOGO' con el enlace directo a tu logotipo -->
                        <img src="https://i.postimg.cc/RCWybCKM/logo-final.png" alt="Logo de ZenMindConnect">
                        <div class="zenmindconnect-text">ZenMindConnect</div>
                        <h1>Hola,</h1>
                        <p>Somos el equipo de ZenMindConnect. Hemos visto que deseas recuperar tu contraseña o se te ha olvidado. Para recuperar tu contraseña, haz clic en el siguiente enlace:</p>
                        <a class="reset-link" href="http://127.0.0.1:8000/changepassword/{token}/">Recuperar Contraseña<span class="key-icon">&#128273;</span></a>
                    </div>
                </body>
            </html>
        """
        
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        
        # Especifica el tipo de contenido como HTML
        send_mail(subject, '', email_from, recipient_list, html_message=message)
        return True
    except ValidationError as e:
        print(f'Error al enviar el correo electrónico: {e}')
        return False


# Nueva función para enviar el correo de notificación de eliminación de cuenta
def send_account_deletion_notification(email):
    try:
        subject = 'Notificación: Tu cuenta ha sido eliminada | ZenMindConnect'
        
        # Cuerpo del mensaje con formato HTML
        message = f"""
            <html>
                <head>
                <style>
                        /* Puedes agregar estilos CSS aquí */
                        body {{
                            font-family: 'Arial', sans-serif;
                            background: linear-gradient(to bottom, #4b908e, #ffffff, #4b908e);
                            color: #fff;
                            padding: 20px;
                        }}
                        .container {{
                            max-width: 600px;
                            margin: 0 auto;
                            background: linear-gradient(to bottom, #4b908e, #ffffff, #4b908e);
                            padding: 20px;
                            border-radius: 10px;
                            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                            text-align: center;
                        }}
                        h1 {{
                            color: #808080;  /* Gris intenso */
                        }}
                        p {{
                            color: #000;  /* Negro */
                            font-size: 16px;
                            line-height: 1.5;
                            margin-bottom: 20px;
                        }}
                        img {{
                            max-width: 100%;
                            height: auto;
                            margin-bottom: 20px;
                        }}
                        .zenmindconnect-text {{
                            color: #001F3F;  /* Azul marino */
                            font-size: 36px;
                            font-weight: bold;
                            margin-top: 10px;
                        }}
                        .reset-link {{
                            display: inline-block;
                            padding: 10px 20px;
                            background-color: #FFA500;  /* Naranja */
                            color: #fff;
                            text-decoration: none;
                            border-radius: 5px;
                            font-size: 16px;
                            margin-top: 20px;
                        }}
                        .key-icon {{
                            font-size: 24px;
                            color: #fff;
                            margin-left: 5px;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <img src="https://i.postimg.cc/RCWybCKM/logo-final.png" alt="Logo de ZenMindConnect">
                        <div class="zenmindconnect-text">ZenMindConnect</div>
                        <h1>Hola,</h1>
                        <p>Tu cuenta en ZenMindConnect ha sido eliminada debido a comportamiento inadecuado.</p>
                        <p>Si tienes alguna pregunta o crees que ha habido un error, contáctanos al correo
                        ZenMindConnect.scrum@gmail.com.</p>
                        <p class="delete-icon">&#10060;</p>
                    </div>
                </body>
            </html>
        """
        
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        
        # Especifica el tipo de contenido como HTML
        send_mail(subject, '', email_from, recipient_list, html_message=message)
        return True
    except ValidationError as e:
        print(f'Error al enviar el correo electrónico de notificación: {e}')
        return False




# Nueva función para enviar el correo de notificación de eliminación de cuenta
def send_account_mydeletion_notification(email):
    try:
        subject = 'Notificación: Tu cuenta ha sido eliminada | ZenMindConnect'
        
        # Cuerpo del mensaje con formato HTML
        message = f"""
            <html>
                <head>
                <style>
                        /* Puedes agregar estilos CSS aquí */
                        body {{
                            font-family: 'Arial', sans-serif;
                            background: linear-gradient(to bottom, #4b908e, #ffffff, #4b908e);
                            color: #fff;
                            padding: 20px;
                        }}
                        .container {{
                            max-width: 600px;
                            margin: 0 auto;
                            background: linear-gradient(to bottom, #4b908e, #ffffff, #4b908e);
                            padding: 20px;
                            border-radius: 10px;
                            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                            text-align: center;
                        }}
                        h1 {{
                            color: #808080;  /* Gris intenso */
                        }}
                        p {{
                            color: #000;  /* Negro */
                            font-size: 16px;
                            line-height: 1.5;
                            margin-bottom: 20px;
                        }}
                        img {{
                            max-width: 100%;
                            height: auto;
                            margin-bottom: 20px;
                        }}
                        .zenmindconnect-text {{
                            color: #001F3F;  /* Azul marino */
                            font-size: 36px;
                            font-weight: bold;
                            margin-top: 10px;
                        }}
                        .reset-link {{
                            display: inline-block;
                            padding: 10px 20px;
                            background-color: #FFA500;  /* Naranja */
                            color: #fff;
                            text-decoration: none;
                            border-radius: 5px;
                            font-size: 16px;
                            margin-top: 20px;
                        }}
                        .key-icon {{
                            font-size: 24px;
                            color: #fff;
                            margin-left: 5px;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <img src="https://i.postimg.cc/RCWybCKM/logo-final.png" alt="Logo de ZenMindConnect">
                        <div class="zenmindconnect-text">ZenMindConnect</div>
                        <h1>Hola,</h1>
                        <p>Tu cuenta en ZenMindConnect ha sido eliminada.</p>
                        <p>Lamentamos que te hayas ido de ZenMindConnect.
                        Esperamos que puedas volver pronto, ante dudas o consultas comunicarse al email:
                        ZenMindConnect.scrum@gmail.com.</p>
                        <p class="delete-icon">&#10060;</p>
                    </div>
                </body>
            </html>
        """
        
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        
        # Especifica el tipo de contenido como HTML
        send_mail(subject, '', email_from, recipient_list, html_message=message)
        return True
    except ValidationError as e:
        print(f'Error al enviar el correo electrónico de notificación: {e}')
        return False
