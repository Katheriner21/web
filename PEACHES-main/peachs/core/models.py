from django.db import models
from django.contrib.auth.hashers import make_password
from django.dispatch import receiver
from django.utils import timezone
import os
from django.db.models.signals import pre_delete

class Usuario(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    TIPO_USUARIO_CHOICES = [
        ('usuario', 'Usuario'),
        ('creador_contenido', 'Usuario creador de contenido'),
    ]

    usuario = models.CharField(max_length=150, unique=True, verbose_name="Usuario")
    email = models.EmailField(unique=True, verbose_name="Email")
    contrasena = models.CharField(max_length=128, verbose_name="Contraseña")
    sexo = models.CharField(max_length=20, verbose_name="Sexo")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo', verbose_name="Estado")
    en_linea = models.BooleanField(default=False)
    tipo_usuario = models.CharField(max_length=30, choices=TIPO_USUARIO_CHOICES, default='usuario', verbose_name="Tipo de usuario") 
    session_token = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creacion")
 
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ["-created"]

    def save(self, *args, **kwargs):
        if not self.pk:
            self.contrasena = make_password(self.contrasena)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.usuario

class Datos(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20)
    imagen1 = models.ImageField(upload_to='imagenes', null=True, blank=True)
    imagen2 = models.ImageField(upload_to='imagenes', null=True, blank=True)
    video = models.FileField(upload_to='videos', null=True, blank=True)

    class Meta:
        verbose_name = 'Dato'
        verbose_name_plural = 'Datos'

    def __str__(self):
        return self.usuario.usuario
    
    def save(self, *args, **kwargs):
        # Eliminar imágenes antiguas si se actualizan
        if self.pk:
            old_instance = Datos.objects.get(pk=self.pk)
            if self.imagen1 != old_instance.imagen1:
                old_instance.imagen1.delete(save=False)
            if self.imagen2 != old_instance.imagen2:
                old_instance.imagen2.delete(save=False)
            if self.video != old_instance.video:
                old_instance.video.delete(save=False)
        super().save(*args, **kwargs)
    
class Perfil(models.Model): 
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    texto1 = models.CharField(max_length=160)
    texto2 = models.CharField(max_length=160)
    texto3 = models.CharField(max_length=160)
    imagen_portada = models.ImageField(upload_to='perfil', null=True, blank=True)
    imagen_perfil = models.ImageField(upload_to='perfil', null=True, blank=True)
    imagen1 = models.ImageField(upload_to='perfil', null=True, blank=True)
    imagen2 = models.ImageField(upload_to='perfil', null=True, blank=True)
    imagen3 = models.ImageField(upload_to='perfil', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'
        
    def __str__(self):
        return self.usuario.usuario 
    
    def save(self, *args, **kwargs):
        # Eliminar imágenes antiguas si se actualizan
        if self.pk:
            old_instance = Perfil.objects.get(pk=self.pk)
            if self.imagen_portada != old_instance.imagen_portada:
                old_instance.imagen_portada.delete(save=False)
            if self.imagen_perfil != old_instance.imagen_perfil:
                old_instance.imagen_perfil.delete(save=False)
            if self.imagen1 != old_instance.imagen1:
                old_instance.imagen1.delete(save=False)
            if self.imagen2 != old_instance.imagen2:
                old_instance.imagen2.delete(save=False)
            if self.imagen3 != old_instance.imagen3:
                old_instance.imagen3.delete(save=False)
        super().save(*args, **kwargs)
        
class Historia(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    imagen = models.FileField(upload_to='Historias', null=True, blank=True, verbose_name="Imagen o Video") 
    vista = models.ManyToManyField(Usuario, related_name='vista_joined', blank=True, verbose_name='Vistas')
    fecha_creacion = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Historia'
        verbose_name_plural = 'Historias'

    def __str__(self):
        return f"Historia de {self.usuario.usuario}"

class Historia_Destacada(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    Historia1 = models.FileField(upload_to='historia_destacada', null=True, blank=True, verbose_name="Imagen o Video")
    Historia2 = models.FileField(upload_to='historia_destacada', null=True, blank=True, verbose_name="Imagen o Video")
    Historia3 = models.FileField(upload_to='historia_destacada', null=True, blank=True, verbose_name="Imagen o Video")
    vista1 = models.ManyToManyField(Usuario, related_name='vista1_d_joined', blank=True, verbose_name='Vistas1')
    vista2 = models.ManyToManyField(Usuario, related_name='vista2_d_joined', blank=True, verbose_name='Vistas2')
    vista3 = models.ManyToManyField(Usuario, related_name='vista3_d_joined', blank=True, verbose_name='Vistas3')
    
    class Meta:
        verbose_name = 'Historia_Destacada'
        verbose_name_plural = 'Historias_Destacadas'
        
    def __str__(self):
        return f'Historias destacadas de {self.usuario.usuario}'
    
    def save(self, *args, **kwargs):
        # Eliminar imágenes antiguas si se actualizan
        if self.pk:
            old_instance = Historia_Destacada.objects.get(pk=self.pk)
            if self.Historia1 != old_instance.Historia1:
                old_instance.Historia1.delete(save=False)
            if self.Historia2 != old_instance.Historia2:
                old_instance.Historia2.delete(save=False)
            if self.Historia3 != old_instance.Historia3:
                old_instance.Historia3.delete(save=False)
        super().save(*args, **kwargs)
    
# Define una función para eliminar físicamente el archivo de imagen asociado
@receiver(pre_delete, sender=Historia)
def eliminar_archivo_de_imagen(sender, instance, **kwargs):
    # Verifica si hay un archivo de imagen asociado y elimínalo
    if instance.imagen:
        # Obtiene la ruta del archivo de imagen
        ruta_imagen = instance.imagen.path
        # Verifica si el archivo de imagen existe en el sistema de archivos
        if os.path.exists(ruta_imagen):
            # Elimina físicamente el archivo de imagen
            os.remove(ruta_imagen)

class Subcriptores(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    sub = models.ManyToManyField(Usuario, related_name='subcriptores_joined', blank=True, verbose_name='Subcriptores')
    
    class Meta:
        verbose_name = 'Subcripcion'
        verbose_name_plural = 'Subcripciones'

    def __str__(self):
        return f'Subcriptores de {self.usuario.usuario}'

class Room(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    users = models.ManyToManyField(Usuario, related_name='rooms_joined', blank=True)
    
    class Meta:
        verbose_name = 'Sala'
        verbose_name_plural = 'Salas'

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name='Usuario')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='Sala')
    message = models.TextField(verbose_name='Mensaje', default="")
    timestamp = models.DateTimeField(default=timezone.now, verbose_name='Enviado')
    
    class Meta:
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'

    def __str__(self):
        return f"Mensaje de {self.user.usuario}"

class Conversation(models.Model):
    user1 = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='Usuario_1')
    user2 = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='Usuario_2')
    
    class Meta:
        verbose_name = 'Conversacion'
        verbose_name_plural = 'Conversaciones'
    
    def save(self, *args, **kwargs):
        # Ordena los IDs de los usuarios
        user_ids = [self.user1_id, self.user2_id]
        user_ids.sort()

        # Verifica si ya existe una conversación entre los usuarios
        existing_conversation = Conversation.objects.filter(
            user1_id=user_ids[0], user2_id=user_ids[1]
        ).first()

        if existing_conversation:
            # Si la conversación ya existe, actualiza los campos de la instancia actual
            self.id = existing_conversation.id
        else:
            # Si no existe, guarda la nueva conversación
            super().save(*args, **kwargs)

    def __str__(self):
        return f'Conversacion entre {self.user1} y {self.user2}'
    
class MessageIndividual(models.Model):
    sender = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='sent_messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Mensaje Individual'
        verbose_name_plural = 'Mensajes Individuales'

    def __str__(self):
        return f'Mesaje de {self.sender} en {self.conversation} en la fecha: {self.timestamp}'
   
class Publicacion(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Usuario")
    pub = models.FileField(upload_to='publicacion', null=True, blank=True, verbose_name="Imagen o Video")   
    texto = models.TextField(max_length=200, verbose_name="Informacion")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creacion")
    
    class Meta:
        verbose_name = 'Publicacion'
        verbose_name_plural = 'Publicaciones'
    
    def __str__(self):
        return f'Publicacion de {self.user}'   
    
    def save(self, *args, **kwargs):
        # Eliminar imágenes antiguas si se actualizan
        if self.pk:
            old_instance = Publicacion.objects.get(pk=self.pk)
            if self.pub != old_instance.pub:
                old_instance.pub.delete(save=False)
        super().save(*args, **kwargs)
        
@receiver(pre_delete, sender=Publicacion)
def eliminar_archivo_de_imagen(sender, instance, **kwargs):
    # Verifica si hay un archivo de imagen asociado y elimínalo
    if instance.pub:
        # Obtiene la ruta del archivo de imagen
        ruta_imagen = instance.pub.path
        # Verifica si el archivo de imagen existe en el sistema de archivos
        if os.path.exists(ruta_imagen):
            # Elimina físicamente el archivo de imagen
            os.remove(ruta_imagen)

class Opiniones(models.Model):
    Usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Usuario")
    opinion = models.TextField(verbose_name="Opinion")   
    
    class Meta:
        verbose_name = 'Opinion'
        verbose_name_plural = 'Opiniones'
    
    def __str__(self):
        return f'Opnion de {self.Usuario}'

class SobreNosotros(models.Model):
    oportunidad = models.TextField()
    politicas = models.TextField()
    mision = models.TextField()
    def __str__(self):
        return f'Informacion sobre nosotros'
    
class Transmision(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField(auto_now_add=True)