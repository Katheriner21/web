from django.urls import path
from .consumers import ChatConsumer, ChatConsumerIndividual, LiveStreamConsumer

websocket_urlpatterns = [
    path('ws/room/<room_id>/<user>/', ChatConsumer.as_asgi()),
    path('ws/crv/<crv_id>/<user>/', ChatConsumerIndividual.as_asgi()),
    path('ws/streaming_app/live_stream/<id>/', LiveStreamConsumer.as_asgi()),
]
