from django.db import IntegrityError
from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.hashers import check_password
from .forms import TransmisionForm
from .models import Transmision, Usuario, Perfil as perfl, Datos, Historia, Room, Message, Publicacion
from .models import Conversation, MessageIndividual, Historia_Destacada, Subcriptores, SobreNosotros, Opiniones
from django.db.models import Q
from django.contrib import messages
from more_itertools import chunked
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
import secrets
from functools import wraps

def get_old_messages_individual(request, crv_id):
    # Obtener los mensajes antiguos de la base de datos
    old_messages = MessageIndividual.objects.filter(conversation_id=crv_id)
    # Convertir los mensajes en un formato JSON
    messages_data = [
        {
            'message': message.content,
            'username': message.sender.usuario,  # Accede al nombre de usuario a través de la relación
            'datetime': message.timestamp.astimezone(timezone.get_current_timezone()).strftime('%Y-%m-%d %H:%M:%S')
        }
        for message in old_messages
    ]
    # Devolver los mensajes como una respuesta JSON
    return JsonResponse(messages_data, safe=False)

def get_old_messages(request):
    # Obtener los mensajes antiguos de la base de datos
    old_messages = Message.objects.all()
    # Convertir los mensajes en un formato JSON
    messages_data = [
        {
            'message': message.message,
            'username': message.user.usuario,  # Accede al nombre de usuario a través de la relación
            'datetime': message.timestamp.astimezone(timezone.get_current_timezone()).strftime('%Y-%m-%d %H:%M:%S')
        }
        for message in old_messages
    ]
    # Devolver los mensajes como una respuesta JSON
    return JsonResponse(messages_data, safe=False)

def generate_session_token():
    return secrets.token_hex(16)

def generate_session_token2():
    return secrets.token_hex(18)

def require_session(view_func):
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        session_token = self.request.COOKIES.get('session_token')
        if session_token:
            try:
                user = Usuario.objects.get(session_token=session_token)
                if user.session_token == session_token:
                    return view_func(self, request, *args, **kwargs)
            except Usuario.DoesNotExist:
                pass
        return redirect('login')
    return wrapper

def cerrar_sesion(request):
    session_token = request.COOKIES.get('session_token')
    if session_token:
        try:
            user = Usuario.objects.get(session_token=session_token)
            user.en_linea = False  # Actualiza el estado de conexión a "desconectado"
            user.save()
        except Usuario.DoesNotExist:
            pass

    response = redirect('login')  # Redirige a la página de inicio de sesión
    response.delete_cookie('session_token')  # Elimina la cookie de sesión
    return response

class Registro(TemplateView):
    template_name = 'core/registro.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        usuario = request.POST.get('user')
        email = request.POST.get('e-mail')
        contrasena = request.POST.get('contraseña')
        sexo = request.POST.get('sexo')
        fecha_nacimiento = request.POST.get('cumpleaños')
        tipo_usuario = request.POST.get('Tipo_Usuario')

        nuevo_usuario = Usuario(
            usuario=usuario,
            email=email,
            contrasena=contrasena,
            sexo=sexo,
            fecha_nacimiento=fecha_nacimiento,
            tipo_usuario=tipo_usuario
        )
        try:
            if tipo_usuario == "creador_contenido":
                nuevo_usuario.estado = "inactivo"
                nuevo_usuario.save()
                nuevo_perfil = perfl(usuario=nuevo_usuario)
                nuevo_perfil.save()
                nuevo_dato = Datos(usuario=nuevo_usuario)
                nuevo_dato.save()
                nuevo_HD = Historia_Destacada(usuario=nuevo_usuario)
                nuevo_HD.save()
                nuevo_SB = Subcriptores(usuario=nuevo_usuario)
                nuevo_SB.save()
                sala_1 = Room.objects.get(id=1)
                sala_1.users.add(nuevo_usuario)
                sala_1.save()
                return redirect('registroc', user=usuario)
            else:
                nuevo_usuario.save()
                nuevo_perfil = perfl(usuario=nuevo_usuario)
                nuevo_perfil.save()
                sala_1 = Room.objects.get(id=1)
                sala_1.users.add(nuevo_usuario)
                sala_1.save()
                messages.success(
                    request, 'Registro exitoso. Por favor, inicia sesión.')
                return redirect('login')
        except IntegrityError as e:
            # Verificar el tipo de error
            if 'usuario' in str(e):
                error_message = 'El usuario "{}" ya está registrado.'.format(
                    usuario)
            elif 'email' in str(e):
                error_message = 'El email "{}" ya está registrado.'.format(
                    email)
            else:
                error_message = 'El usuario o el email ya están registrados.'
            messages.error(request, error_message)
            return redirect('registro')

class RegistroC(TemplateView):
    template_name = 'core/registrocreador.html'

    def get(self, request, user):
        return render(request, self.template_name,{'user':user})

    def post(self, request, user):
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        dni = request.POST.get('dni')
        telefono = request.POST.get('telefono')

        nuevo_dato = Datos.objects.get(usuario__usuario=user)
        nuevo_dato.nombre = nombre
        nuevo_dato.apellido = apellido
        nuevo_dato.dni = dni
        nuevo_dato.telefono = telefono
        try:
            nuevo_dato.save()
            return redirect('emailN',usuario=user)
        except IntegrityError as e:
            return redirect('registro')

class Login(TemplateView):
    template_name = 'core/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        usuario = request.POST.get('user')
        contraseña = request.POST.get('pass')
        try:
            user = Usuario.objects.get(usuario=usuario)
            if user.estado == 'activo' and check_password(contraseña, user.contrasena):
                print(user.tipo_usuario)
                if user.tipo_usuario == 'Usuario':
                    user.session_token = generate_session_token()
                else:
                    user.session_token = generate_session_token2()
                user.en_linea = True
                user.save()
                response = HttpResponseRedirect('Inicio/')
                response.set_cookie('session_token', user.session_token)
                return response
            elif user.estado != 'activo':
                messages.error(
                    request, 'El usuario está inactivo. Contacta al administrador.')
                return redirect('login')
            else:
                messages.error(
                    request, 'Nombre de usuario o contraseña incorrectos.')
                return redirect('login')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuario no encontrado.')
            return redirect('login')

class sobrenosotros(TemplateView):
    template_name = 'core/sobrenostros.html'
    
    @require_session
    def get(self,request):
        nosotros = SobreNosotros.objects.all()
        opiniones = []
        opinion = Opiniones.objects.all()
        perfil = perfl.objects.all()
        for o in opinion:
            for p in perfil:
                if o.Usuario.usuario == p.usuario.usuario:
                    opiniones.append((p.imagen_perfil, o.opinion, p.usuario.usuario, p.usuario.tipo_usuario))
                    
        return render(request,self.template_name, {'n':nosotros, 'op':opiniones})
    def post(self, request):
        nombre = request.POST.get('name')
        correo = request.POST.get('email')
        mensaje = request.POST.get('msj')
        
        # Envía el correo electrónico
        subject = 'Solicitud de Contacto'
        email_message = render_to_string('core/email/emailcont.html', {
            'nombre': nombre,
            'correo': correo,
            'mensaje': mensaje,
        })
        email = EmailMessage(
            subject,
            email_message,
            settings.EMAIL_HOST_USER,
            ['Peaches2024.oficial@gmail.com'], 
        )
        email.content_subtype = 'html'  
        email.send(fail_silently=False)
        
        # Redirecciona o devuelve una respuesta según sea necesario
        messages.success(request, '¡Gracias por tu mensaje! Nos pondremos en contacto contigo pronto.')
        return redirect('sobrenosotros')
        
class Inicio(TemplateView):
    template_name = 'core/index.html'

    @require_session
    def get(self, request):
        session_token = self.request.COOKIES.get('session_token')
        userf = Usuario.objects.get(session_token=session_token)
        perfil = perfl.objects.exclude(usuario__id = userf.id).order_by('-usuario__created')
        perfiles_con_suscriptores = []

        for usuario in Usuario.objects.all():
            subscriptores = Subcriptores.objects.filter(usuario=usuario).first()
            num_suscriptores = subscriptores.sub.all().count() if subscriptores else 0
            perfiles_con_suscriptores.append((usuario.perfil, num_suscriptores))

        perfiles_ordenados = sorted(perfiles_con_suscriptores, key=lambda x: x[1], reverse=True)
        perfiles_filtrados = [perfil for perfil, num_suscriptores in perfiles_ordenados if perfil.usuario != userf]

        
        return render(request, self.template_name, {'perfil': perfil, 'perfild':perfiles_filtrados})

class Contenido(TemplateView):
    template_name = 'core/contenido.html'

    @require_session
    def get(self, request):
        room = Room.objects.get(id=1)
        session_token = self.request.COOKIES.get('session_token')
        userf = Usuario.objects.get(session_token=session_token)
        user = Usuario.objects.all()
                
        # Filtrar perfiles excluyendo el del usuario actual
        perfil = perfl.objects.filter(usuario__historia__isnull=False).distinct()
        miperfil = perfl.objects.exclude(usuario__id=userf.id).filter(usuario__historia__isnull=False).distinct()
        perfila = perfl.objects.get(usuario__usuario=userf.usuario)
        subscriptores = Subcriptores.objects.all()
        siete = []
        ocho = []
        for s in subscriptores:
            if s.sub.filter(usuario=userf.usuario).exists():
                for p in perfil:
                    if p.usuario.usuario == s.usuario.usuario:
                        ocho.append((p.imagen_perfil,p.usuario.usuario))
                
                for p in miperfil:
                    if p.usuario.usuario == s.usuario.usuario:
                        siete.append((p.imagen_perfil,p.usuario.usuario))
        
        view = Historia.objects.all()
        vistas = view.filter(vista=userf.id)
        
        tiene_historias = Historia.objects.filter(usuario__usuario=userf.usuario).exists()
        
        return render(request, self.template_name, {
            'view':vistas,
            'room':room,
            'userf': userf,
            'user': user, 
            'perfila':perfila,
            'perfil7': siete, 
            'perfil8': ocho, 
            'tiene_historias':tiene_historias
        })
    def post(self, request):
        session_token = self.request.COOKIES.get('session_token')
        
        # Obtener el archivo de la solicitud POST
        history = request.FILES.get('history')
        
        if history:  # Verificar si se ha enviado un archivo
            user = Usuario.objects.get(session_token=session_token)
            view = Historia.objects.filter(usuario=user)
            for v in view:
                v.vista.clear()
                v.save()
            
            # Crear una nueva instancia de Historia con el archivo recibido
            historia = Historia(usuario=user, imagen=history)
            historia.save()
            
        return redirect('contenido')
   
class ViewHistoryD(TemplateView):
    template_name = 'core/ViewHistoryd.html'
    
    @require_session
    def get(self, request, usuario, id):
        session_token = self.request.COOKIES.get('session_token')
        userf = Usuario.objects.get(session_token=session_token)
        histor = Historia_Destacada.objects.get(usuario__usuario=usuario)
        imgs = []
        
        if id == '1':
            if histor.Historia1.url.endswith('.mp4'):
                es_video = True
            else:
                es_video = False
            imgs.append((histor.Historia1, es_video))
        if id == '2':
            if histor.Historia2.url.endswith('.mp4'):
                es_video = True
            else:
                es_video = False
            imgs.append((histor.Historia2, es_video))
        if id == '3':
            if histor.Historia3.url.endswith('.mp4'):
                es_video = True
            else:
                es_video = False
            imgs.append((histor.Historia3, es_video))
            
            
        return render(request,self.template_name, {
            'usuario':usuario,
            'history':histor,
            'img':imgs,
            'user':userf,
            'id':id
            })
        
class ViewPub(TemplateView):
    template_name = 'core/ViewPub.html'
    
    @require_session
    def get(self, request, id,tip):
        pub = Publicacion.objects.get(id=id)
        pubs = []
        if pub.pub.url.endswith('.mp4'):
            es_video = True
        else:
            es_video = False
        pubs.append((pub.pub, pub.texto, es_video))
            
        return render(request,self.template_name, {
            'pubs':pubs,
            'tip':tip
            })
        
class ViewPubn(TemplateView):
    template_name = 'core/ViewPubn.html'
    
    @require_session
    def get(self, request, user, id):
        pub = Publicacion.objects.get(id=id)
        pubs = []
        if pub.pub.url.endswith('.mp4'):
            es_video = True
        else:
            es_video = False
        pubs.append((pub.pub, pub.texto, es_video))
            
        return render(request,self.template_name, {
            'pubs':pubs,
            'user':user
            })
    
class ViewHistory(TemplateView):
    template_name = 'core/ViewHistory.html'
    
    @require_session
    def get(self, request, usuario):
        session_token = self.request.COOKIES.get('session_token')
        userf = Usuario.objects.get(session_token=session_token)
        user = Usuario.objects.all()
        perfil = perfl.objects.filter(usuario__historia__isnull=False).distinct()
        miperfil = perfl.objects.exclude(usuario__id=userf.id).filter(usuario__historia__isnull=False).distinct()
        perfila = perfl.objects.get(usuario__usuario=userf.usuario)
        subscriptores = Subcriptores.objects.all()
        siete = []
        ocho = []
        for s in subscriptores:
            if s.sub.filter(usuario=userf.usuario).exists():
                for p in perfil:
                    if p.usuario.usuario == s.usuario.usuario:
                        ocho.append((p.imagen_perfil,p.usuario.usuario))
                
                for p in miperfil:
                    if p.usuario.usuario == s.usuario.usuario:
                        siete.append((p.imagen_perfil,p.usuario.usuario))
        
        histor = Historia.objects.filter(usuario__usuario=usuario)
        history = []
        for h in histor:
            if h.imagen.url.endswith('.mp4'):
                es_video = True
            else:
                es_video = False
            history.append((h.imagen, es_video))
            
        return render(request,self.template_name, {
            'usuario':usuario,
            'userf':userf,
            'user': user, 
            'perfila':perfila,
            'perfil7':siete, 
            'perfil8':ocho, 
            'userH':history
            })

class Soporte(TemplateView):
    template_name = 'core/soporte.html'
    
    @require_session
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        asunto = request.POST.get('asunto')
        mensaje = request.POST.get('mensaje')
        
        # Envía el correo electrónico
        subject = 'Solicitud de Soporte'
        email_message = render_to_string('core/email/emailsop.html', {
            'nombre': nombre,
            'correo': correo,
            'asunto': asunto,
            'mensaje': mensaje,
        })
        email = EmailMessage(
            subject,
            email_message,
            settings.EMAIL_HOST_USER,
            ['Peaches2024.oficial@gmail.com'], 
        )
        email.content_subtype = 'html'  
        email.send(fail_silently=False)
        
        # Redirecciona o devuelve una respuesta según sea necesario
        messages.success(request, '¡Gracias por tu mensaje! Nos pondremos en contacto contigo pronto.')
        return redirect('soporte')
        
class view_perfild(TemplateView):
    template_name = 'core/view-perfild.html'
    
    @require_session
    def get(self, request):
        session_token = self.request.COOKIES.get('session_token')
        usera = Usuario.objects.get(session_token=session_token)
        perfil = perfl.objects.get(usuario=usera)
        perfiles = perfl.objects.all()
        conversaciones = Conversation.objects.filter(user1__usuario = perfil.usuario.usuario) | Conversation.objects.filter(user2__usuario = perfil.usuario.usuario)

        conversaciones_con_otro_usuario = []

        # Iterar sobre las conversaciones y encontrar el otro usuario en cada una
        for conversacion in conversaciones:
            otro_usuario = conversacion.user2 if conversacion.user1.usuario == perfil.usuario.usuario else conversacion.user1
            conversaciones_con_otro_usuario.append((conversacion.id,otro_usuario))
                
        return render(request, self.template_name, {'perfl': perfil, 'user':usera, 'userchat':usera.usuario, 'chats':conversaciones_con_otro_usuario, 'perfiles':perfiles}) 

class MIPerfil(TemplateView):
    template_name = 'core/MIperfil.html'

    @require_session
    def get(self, request):
        session_token = request.COOKIES.get('session_token')
        user = Usuario.objects.get(session_token=session_token)
        perfil = perfl.objects.get(usuario__session_token=session_token)
        perfiles = perfl.objects.all()
        conversaciones = Conversation.objects.filter(user1__usuario = perfil.usuario.usuario) | Conversation.objects.filter(user2__usuario = perfil.usuario.usuario)

        conversaciones_con_otro_usuario = []

        # Iterar sobre las conversaciones y encontrar el otro usuario en cada una
        for conversacion in conversaciones:
            otro_usuario = conversacion.user2 if conversacion.user1.usuario == perfil.usuario.usuario else conversacion.user1
            conversaciones_con_otro_usuario.append((conversacion.id,otro_usuario))
        return render(request, self.template_name, {'user':user, 'perfl': perfil, 'chats':conversaciones_con_otro_usuario, 'perfiles':perfiles})

    def post(self, request):
        session_token = request.COOKIES.get('session_token')
        user = request.session.get('usuario')
        perfil = perfl.objects.get(usuario__session_token=session_token)

        # Obtener los datos del formulario
        texto1 = request.POST.get('texto1')
        texto2 = request.POST.get('texto2')
        texto3 = request.POST.get('texto3')
        imagen_portada = request.FILES.get('imagen_portada')
        imagen_perfil = request.FILES.get('imagen_perfil')
        imagen1 = request.FILES.get('imagen1')
        imagen2 = request.FILES.get('imagen2')
        imagen3 = request.FILES.get('imagen3')

        # Verificar y actualizar los campos que han sido modificados en el formulario
        if texto1:
            perfil.texto1 = texto1
        if texto2:
            perfil.texto2 = texto2
        if texto3:
            perfil.texto3 = texto3
        if imagen_portada:
            perfil.imagen_portada = imagen_portada
        if imagen_perfil:
            perfil.imagen_perfil = imagen_perfil
        if imagen1:
            perfil.imagen1 = imagen1
        if imagen2:
            perfil.imagen2 = imagen2
        if imagen3:
            perfil.imagen3 = imagen3
        try:
            perfil.save()  # Guardar los cambios en el perfil
            return redirect('perfil')
        except Exception as e:
            return JsonResponse({'error': f'Ocurrió un error al guardar el perfil: {str(e)}'}, status=500)

class Perfil(TemplateView):
    template_name = 'core/perfil.html'

    @require_session
    def get(self, request, user):
        perfil = perfl.objects.get(usuario__usuario=user)
        session_token = self.request.COOKIES.get('session_token')
        usera = Usuario.objects.get(session_token=session_token)
        conversacion = Conversation.objects.filter(
                Q(user1__usuario=usera.usuario) & Q(user2__usuario=perfil.usuario.usuario) |
                Q(user1__usuario=perfil.usuario.usuario) & Q(user2__usuario=usera.usuario)
            ).first()
        if not conversacion:
            usuario_obj = Usuario.objects.get(usuario=perfil.usuario.usuario)
            Conversation.objects.create(user1=usuario_obj, user2=usera)
            conversacion = Conversation.objects.filter(
                Q(user1__usuario=usera.usuario) & Q(user2__usuario=perfil.usuario.usuario) |
                Q(user1__usuario=perfil.usuario.usuario) & Q(user2__usuario=usera.usuario)
            ).first()
                
        return render(request, self.template_name, {'perfl': perfil, 'user':usera, 'crv':conversacion, 'userchat':user}) 
    
class view_perfil(TemplateView):
    template_name = 'core/view-perfil.html'
    
    @require_session
    def get(self, request):
        session_token = self.request.COOKIES.get('session_token')
        usera = Usuario.objects.get(session_token=session_token)
        history = Historia_Destacada.objects.get(usuario=usera)
        perfil = perfl.objects.get(usuario=usera)
        if history.vista1.filter(id=usera.id).exists():
            view1 = True
        else:
            view1 = False

        if history.vista2.filter(id=usera.id).exists():
            view2 = True
        else:
            view2 = False

        if history.vista3.filter(id=usera.id).exists():
            view3 = True
        else:
            view3 = False
        sb = Subcriptores.objects.get(usuario=usera)
        bsb = Subcriptores.objects.filter(sub=usera.id)
        perfiles = perfl.objects.all()
        cant_sb = sb.sub.count()
        publ = Publicacion.objects.filter(user__usuario=usera)
        pubs = []
        for p in publ:
            if p.pub.url.endswith('.mp4'):
                es_video = True
            else:
                es_video = False
            pubs.append((p.pub, p.texto, es_video, p.id))
        pub = list(chunked(pubs,5))
        conversaciones = Conversation.objects.filter(user1__usuario = perfil.usuario.usuario) | Conversation.objects.filter(user2__usuario = perfil.usuario.usuario)

        conversaciones_con_otro_usuario = []

        # Iterar sobre las conversaciones y encontrar el otro usuario en cada una
        for conversacion in conversaciones:
            otro_usuario = conversacion.user2 if conversacion.user1.usuario == perfil.usuario.usuario else conversacion.user1
            conversaciones_con_otro_usuario.append((conversacion.id,otro_usuario))
            
        return render(request, self.template_name, {'pub':pub, 'perfl': perfil, 'user':usera, 'chats':conversaciones_con_otro_usuario, 'perfiles':perfiles, 'userchat':usera.usuario, 'sb':cant_sb, 'bsb':bsb, 'history':history, 'view1':view1, 'view2':view2, 'view3':view3}) 

class Perfilcontenido(TemplateView):
    template_name = 'core/perfilContenido.html'
    
    @require_session
    def get(self, request, user):
        perfil = perfl.objects.get(usuario__usuario=user)
        session_token = self.request.COOKIES.get('session_token')
        history = Historia_Destacada.objects.get(usuario__usuario=user)
        usera = Usuario.objects.get(session_token=session_token)
        publ = Publicacion.objects.filter(user__usuario=user)
        pubs = []
        for p in publ:
            if p.pub.url.endswith('.mp4'):
                es_video = True
            else:
                es_video = False
            pubs.append((p.pub, p.texto, es_video, p.id))
        pub = list(chunked(pubs,5))
        
        if history.vista1.filter(id=usera.id).exists():
            view1 = True
        else:
            view1 = False

        if history.vista2.filter(id=usera.id).exists():
            view2 = True
        else:
            view2 = False

        if history.vista3.filter(id=usera.id).exists():
            view3 = True
        else:
            view3 = False
        sb = Subcriptores.objects.get(usuario__usuario=user)
        bsb = False
        for s in sb.sub.all():
            if s == usera:
                bsb = True
        
        print(bsb)
        cant_sb = sb.sub.count()
        conversacion = Conversation.objects.filter(
                Q(user1__usuario=usera.usuario) & Q(user2__usuario=perfil.usuario.usuario) |
                Q(user1__usuario=perfil.usuario.usuario) & Q(user2__usuario=usera.usuario)
            ).first()
        if not conversacion:
            usuario_obj = Usuario.objects.get(usuario=perfil.usuario.usuario)
            Conversation.objects.create(user1=usuario_obj, user2=usera)
            conversacion = Conversation.objects.filter(
                Q(user1__usuario=usera.usuario) & Q(user2__usuario=perfil.usuario.usuario) |
                Q(user1__usuario=perfil.usuario.usuario) & Q(user2__usuario=usera.usuario)
            ).first()
                
        return render(request, self.template_name, {'pub':pub, 'perfl': perfil, 'user':usera, 'crv':conversacion, 'userchat':user, 'sb':cant_sb, 'bsb':bsb, 'history':history, 'view1':view1, 'view2':view2, 'view3':view3}) 

class Miperfilcontenido(TemplateView):
    template_name = 'core/MIperfilContenido.html'

    @require_session
    def get(self, request):
        session_token = request.COOKIES.get('session_token')
        user = Usuario.objects.get(session_token=session_token)
        publ = Publicacion.objects.filter(user=user).order_by("-created")
        pubs = []
        for p in publ:
            if p.pub.url.endswith('.mp4'):
                es_video = True
            else:
                es_video = False
            pubs.append((p.pub, p.texto, es_video, p.id))
            
        first_chunk_size = 4
        first_chunk = pubs[:first_chunk_size]
        remaining_data = pubs[first_chunk_size:]

        # Dividir los datos restantes en chunks de tamaño 5
        other_chunks = list(chunked(remaining_data, 5))

        # Combinar el primer chunk y los otros chunks
        pub = [first_chunk] + other_chunks
          
        perfil = perfl.objects.get(usuario__session_token=session_token)
        perfiles = perfl.objects.all()
        history = Historia_Destacada.objects.get(usuario__session_token=session_token)
        sb = Subcriptores.objects.get(usuario__session_token=session_token)
        cant_sb = sb.sub.count()
        
        conversaciones = Conversation.objects.filter(user1__usuario = perfil.usuario.usuario) | Conversation.objects.filter(user2__usuario = perfil.usuario.usuario)

        conversaciones_con_otro_usuario = []

        # Iterar sobre las conversaciones y encontrar el otro usuario en cada una
        for conversacion in conversaciones:
            otro_usuario = conversacion.user2 if conversacion.user1.usuario == perfil.usuario.usuario else conversacion.user1
            conversaciones_con_otro_usuario.append((conversacion.id,otro_usuario))
           
        return render(request, self.template_name, {'perfl': perfil, 'history':history, 'sb':cant_sb, 'chats':conversaciones_con_otro_usuario, 'perfiles':perfiles, 'user':user, 'pub':pub})

    def post(self, request):
        session_token = request.COOKIES.get('session_token')
        perfil = perfl.objects.get(usuario__session_token=session_token)
        history = Historia_Destacada.objects.get(usuario__session_token=session_token)

        # Obtener los datos del formulario
        imagen_portada = request.FILES.get('imagen_portada')
        imagen_perfil = request.FILES.get('imagen_perfil')
        historia1 = request.FILES.get('historia1')
        historia2 = request.FILES.get('historia2')
        historia3 = request.FILES.get('historia3')

        # Verificar y actualizar los campos que han sido modificados en el formulario
        if imagen_portada:
            perfil.imagen_portada = imagen_portada
        if imagen_perfil:
            perfil.imagen_perfil = imagen_perfil
        if historia1:
            history.Historia1 = historia1
            history.vista1.clear()
        if historia2:
            history.Historia2 = historia2
            history.vista2.clear()
        if historia3:
            history.Historia3 = historia3
            history.vista3.clear()
        try:
            perfil.save()  # Guardar los cambios en el perfil
            history.save()
            return redirect('perfilcontenido')
        except Exception as e:
            return JsonResponse({'error': f'Ocurrió un error al guardar el perfil: {str(e)}'}, status=500)

class pago(TemplateView):
    template_name = "core/pago.html"
    
    @require_session
    def get(self, request,user):
        return render(request, self.template_name,{'user':user})

def vistas(request, usuario):
    view = Historia.objects.filter(usuario__usuario=usuario)
    session_token = request.COOKIES.get('session_token')
    user = Usuario.objects.get(session_token=session_token)
    for v in view:
        v.vista.add(user)
        v.save()
    return redirect('contenido')

def vistasd(request, usuario, id):
    view = Historia_Destacada.objects.get(usuario__usuario=usuario)
    session_token = request.COOKIES.get('session_token')
    user = Usuario.objects.get(session_token=session_token)
    if id == '1':
        view.vista1.add(user)
        view.save()
    if id == '2':
        view.vista2.add(user)
        view.save()
    if id == '3':
        view.vista3.add(user)
        view.save()        
    return redirect('viewperfil')
    
def agregar_subscriptor(request, user):
    session_token = request.COOKIES.get('session_token')
    usuario = Usuario.objects.get(session_token=session_token)
    sb = Subcriptores.objects.get(usuario__usuario=user)
    sb.sub.add(usuario)
    sb.save()
    return JsonResponse({'message': 'Suscripción exitosa'})

def cargar_pub(request):
    session_token = request.COOKIES.get('session_token')
    user = Usuario.objects.get(session_token=session_token)
    info = request.POST.get('info')
    pub = request.FILES.get('pub')
    if pub:
        nueva_pub = Publicacion(
            user = user,
            pub = pub,
            texto = info
        )
        nueva_pub.save()
        return JsonResponse({'success': 'Publicación guardada correctamente', 'redirect_url': '/perfilcontenido/'})
    else:
        return JsonResponse({'error': 'No puede agregar publicación sin foto o video'})
    
def edit_pub(request):
    session_token = request.COOKIES.get('session_token')
    user = Usuario.objects.get(session_token=session_token)
    id = request.POST.get('id')
    info = request.POST.get('info')
    pub = request.FILES.get('pub')
    edit_pub = Publicacion.objects.get(id=id)
    if pub:
        edit_pub.user = user
        edit_pub.pub = pub
        edit_pub.texto = info
        edit_pub.save()
        return JsonResponse({'success': 'Publicación editada correctamente', 'redirect_url': '/perfilcontenido/'})
    else:
        return JsonResponse({'error': 'No puede editar publicación sin foto o video'})
    
def cargar_opinion(request):
    session_token = request.COOKIES.get('session_token')
    user = Usuario.objects.get(session_token=session_token)
    op = request.POST.get('opinion')
    if op:  # Verificar si se proporcionó un valor para 'opinion'
        nueva_opinion = Opiniones(
            Usuario=user,
            opinion=op
        )
        nueva_opinion.save()
        return JsonResponse({'message': 'Opinion guardada correctamente'})
    else:
        return JsonResponse({'error': 'El campo opinion no puede estar vacío'})

def upload_images(request):
    if request.method == 'POST' and 'image' in request.FILES:
        image_file = request.FILES['image']
        user = request.POST.get('dato')
        num = request.POST.get('num')
        dato = Datos.objects.get(usuario__usuario=user)

        if num == '1':  # Si num es '1' y imagen1 está vacío, lo guardamos ahí
            dato.imagen1 = image_file
        elif num == '2':  # Si num es '2' y imagen2 está vacío, lo guardamos ahí
            dato.imagen2 = image_file
        dato.save()
        return JsonResponse({'message': 'Imagen recibida y guardada correctamente'})

    return JsonResponse({'error': 'No se envió una imagen o se utilizó un método HTTP incorrecto'}, status=400)

def upload_video(request):
    if request.method == 'POST' and 'video' in request.FILES:
        video_file = request.FILES['video']
        user = request.POST.get('dato')
        dato = Datos.objects.get(usuario__usuario=user)
        dato.video = video_file
        dato.save()
        return JsonResponse({'message': 'Video enviado correctamente'})
    return JsonResponse({'error': 'No se envió un video o se utilizó un método HTTP incorrecto'}, status=400)

def cod_mail(request):
    if request.method == "POST":
        cod = request.POST['cod']
        user = request.POST['user']
        email = Usuario.objects.get(usuario=user)
        subject = 'Codigo de verificacion'
        template = render_to_string('core/email/emailcod.html', {
            'user':user,
            'cod':cod
        })
        email = EmailMessage(
            subject,
            template,
            settings.EMAIL_HOST_USER,
            [email.email]
        )
        email.content_subtype = 'html' 
        email.fail_silently = False
        email.send()
        return JsonResponse({'error': 'Correo enviado'})

def not_mail(request,usuario):
    subject = 'Usuario Nuevo'
    template = render_to_string('core/email/emailnot.html', {
        'usuario':usuario
    })
    email = EmailMessage(
        subject,
        template,
        settings.EMAIL_HOST_USER,
        ['Peaches2024.oficial@gmail.com']
    )
    email.content_subtype = 'html'
    email.fail_silently = False
    email.send()
    messages.success(
            request, 'Sus datos serán validados y su cuenta será activada en un lapso de 12 horas.')
    return redirect('login')

########################
from .agora import get_rtc_token, APP_ID

def streaming_view(request, name):
    channel_name = name
    rtc_token = get_rtc_token(channel_name, role='host')
    
    context = {
        "appId": APP_ID,
        "channel": channel_name,
        "token": rtc_token,
    }
    
    return render(request, "core/live/grabar.html", context)

def watch_streaming_view(request, name):
    channel_name = name
    rtc_token = get_rtc_token(channel_name, role="audience")

    context = {
        "appId": APP_ID,
        "channel": channel_name,
        "token": rtc_token,
    }

    return render(request, "core/live/ver_transmision.html", context)


###########pagos##########
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import requests
import json
import base64

PAYPAL_CLIENT_ID = "ASTCe-PZ7FoSIOhAC75G1tBJAvQp3Dz7LplGUhrsYpTvj-pMa1aKCGA7JqEbVOpB1h5SnTpSbdxnuXrl"
PAYPAL_CLIENT_SECRET = "EI897tT1pojQuwfOLf-d6-6uErMNXFA9IWmzfS7GhUw-bOGxWp_4wNCbv7TgU1xdP9A6ueYuKnUkchgK"
BASE_URL = "https://api-m.sandbox.paypal.com"
PORT = 8888


# Función para generar el token de acceso OAuth 2.0
def generate_access_token():
    try:
        if not PAYPAL_CLIENT_ID or not PAYPAL_CLIENT_SECRET:
            raise Exception("MISSING_API_CREDENTIALS")

        auth_str = f"{PAYPAL_CLIENT_ID}:{PAYPAL_CLIENT_SECRET}"
        auth_b64 = base64.b64encode(auth_str.encode("ascii")).decode("ascii")
        headers = {
            "Authorization": f"Basic {auth_b64}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        payload = {"grant_type": "client_credentials"}

        response = requests.post(
            f"{BASE_URL}/v1/oauth2/token",
            data=payload,
            headers=headers,
        )

        if response.status_code == 200:
            data = response.json()
            return data.get("access_token")
        else:
            raise Exception(f"Failed to generate Access Token: {response.text}")

    except Exception as e:
        print(f"Failed to generate Access Token: {e}")
        return None

# Vista para crear una orden de PayPal
@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        try:
            cart_data = json.loads(request.body)
            access_token = generate_access_token()
            url = f"{BASE_URL}/v2/checkout/orders"
            payload = {
                "intent": "CAPTURE",
                "purchase_units": [
                    {
                        "amount": {
                            "currency_code": "USD",
                            "value": "10.00",
                        },
                    },
                ],
            }
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            }
            response = requests.post(url, json=payload, headers=headers)
            return JsonResponse(handle_response(response))
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

# Vista para capturar una orden de PayPal
@csrf_exempt
def capture_order(request, order_id):
    if request.method == 'POST':
        try:
            access_token = generate_access_token()
            url = f"{BASE_URL}/v2/checkout/orders/{order_id}/capture"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            }
            response = requests.post(url, headers=headers)
            return JsonResponse(handle_response(response))
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

# Función para manejar la respuesta de la API de PayPal
def handle_response(response):
    try:
        json_response = response.json()
        return {
            'json_response': json_response,
            'http_status_code': response.status_code
        }
    except:
        return {'error': 'Failed to parse response'}