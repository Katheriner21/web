from django.contrib import admin
from .models import *

admin.site.register([Usuario, Perfil, Datos, Historia, Message, Room, Conversation, MessageIndividual, 
                    Transmision, Historia_Destacada, Subcriptores, SobreNosotros, Opiniones, Publicacion])
 