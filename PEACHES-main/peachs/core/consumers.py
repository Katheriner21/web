import subprocess
import cv2
import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from django.utils import timezone
from ffmpeg import _ffmpeg
import numpy as np
from .models import Message, Usuario, Conversation, MessageIndividual

def convert_bytes_to_opencv_video(bytes_data):
    # Comando ffmpeg para convertir bytes de entrada a un formato de video compatible con OpenCV
    command = [
        'ffmpeg',
        '-y',  # Sobrescribe el archivo de salida si existe
        '-f', 'webm',  # Formato de entrada
        '-c:v', 'vp9',  # Códec de video de entrada
        '-i', 'pipe:',  # Lee desde la entrada estándar (stdin)
        '-pix_fmt', 'bgr24',  # Formato de píxeles de salida
        '-vcodec', 'rawvideo',  # Códec de video de salida
        '-',
    ]

    # Ejecutar el comando ffmpeg y capturar la salida
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, _ = process.communicate(input=bytes_data)

    # Convertir la salida a un array numpy y darle la forma adecuada
    return np.frombuffer(out, np.uint8).reshape([-1, 720, 1280, 3])



class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'sala_chat_%s' % self.id
        self.user = self.scope['url_route']['kwargs']['user']

        print('Conexión establecida al room_group_name ' + self.room_group_name)
        print('Conexión establecida channel_name ' + self.channel_name)
        print(f'Usuario conectado: {self.user}')

        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        print('Se ha desconectado')
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)


    def receive(self, text_data):
        print('Mensaje recibido')
        
        sender_id = None 

        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']

            # Obtenemos el ID del usuario que envia el mensaje
            
            usuario = Usuario.objects.get(usuario=self.user)
            sender_id = usuario.id
            print(sender_id)
            if sender_id:
                # Grabamos el mensaje en la base de datos
                message_save = Message.objects.create(user_id=sender_id, room_id=self.id, message=message)
                message_save.save()
                                                      
                # Sincronizamos y enviamos el mensaje a la sala de chat
                async_to_sync(self.channel_layer.group_send)(self.room_group_name, {
                    'type': 'chat_message',
                    'message': message,
                    'username': usuario.usuario,
                    'datetime': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'sender_id': sender_id
                })
            else:
                print('Usuario no autenticado. Ignorando el mensaje')

        except json.JSONDecodeError as e:
            print('Hubo un error al decodificar el JSON: ', e)
        except KeyError as e:
            print('Clave faltante en el JSON: ', e)
        except Exception as e:
            print('Error desconocido: ', e)

    def chat_message(self, event):
        message = event['message']
        username = event['username']
        datetime = event['datetime']
        sender_id = event['sender_id']

        usuario = Usuario.objects.get(usuario=self.user)
        current_user_id = usuario.id
        if sender_id != current_user_id:
            self.send(text_data=json.dumps({
                'message':message,
                'username': username,
                'datetime': datetime
            }))

class ChatConsumerIndividual(WebsocketConsumer):

    def connect(self):
        self.id = self.scope['url_route']['kwargs']['crv_id']
        self.room_group_name = 'sala_chat_%s' % self.id
        self.user = self.scope['url_route']['kwargs']['user']

        print('Conexión establecida al room_group_name ' + self.room_group_name)
        print('Conexión establecida channel_name ' + self.channel_name)
        print(f'Usuario conectado: {self.user}')

        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        print('Se ha desconectado')
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)


    def receive(self, text_data):
        print('Mensaje recibido')
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']

            # Buscar la conversación
            conversation = Conversation.objects.get(id=self.id)

            # Buscar el remitente del mensaje
            sender = Usuario.objects.get(usuario=self.user)
            sender_id = sender.id

            # Grabar el mensaje en la base de datos
            message_save = MessageIndividual.objects.create(sender=sender, conversation=conversation, content=message)
            message_save.save()

            # Enviar el mensaje a todos los usuarios en la conversación
            async_to_sync(self.channel_layer.group_send)(self.room_group_name, {
                    'type': 'chat_message',
                    'message': message,
                    'username': sender.usuario,
                    'datetime': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'sender_id': sender_id
                })

        except json.JSONDecodeError as e:
            print('Error al decodificar JSON:', e)
        except KeyError as e:
            print('Clave faltante en el JSON:', e)
        except Conversation.DoesNotExist:
            print('Conversación no encontrada')
        except Usuario.DoesNotExist:
            print('Usuario no encontrado')

    def chat_message(self, event):
        message = event['message']
        username = event['username']
        datetime = event['datetime']
        sender_id = event['sender_id']

        usuario = Usuario.objects.get(usuario=self.user)
        current_user_id = usuario.id
        if sender_id != current_user_id:
            self.send(text_data=json.dumps({
                'message':message,
                'username': username,
                'datetime': datetime
            }))

class LiveStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'live_stream'
        self.room_group_name = 'stream_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # En el lado del servidor (Python, Django, u otro framework)
    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            # Convertir los datos del video a un formato compatible con OpenCV
            video_data = convert_bytes_to_opencv_video(bytes_data)
            
            print(video_data)
            
            # Ahora puedes usar video_data con OpenCV para procesar el video según sea necesario
            # Por ejemplo, puedes guardar el video en disco
            for frame in video_data:
                cv2.imwrite('frame.jpg', frame)
                # Procesar el frame o hacer cualquier otra operación necesaria
            
            # Envía los datos procesados al grupo
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'stream_message',
                    'message': bytes_data,  # Puedes enviar los datos sin modificar si es necesario
                    'mime_type': 'video/webm'  # También puedes enviar el tipo MIME original si lo prefieres
                }
            ) # Libera el recurso de video

        
    async def stream_message(self, event):
        message = event['message']
        if isinstance(message, str):
            await self.send(text_data=json.dumps({
                'message': message
            }))
        else:
            await self.send(bytes_data=message)