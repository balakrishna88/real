# routing.py (or wherever your WebSocket URL patterns are defined)
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    # Route for individual chat rooms
    path('ws/chat/<int:room_id>/', consumers.ChatConsumer.as_asgi()),
    
    # Route for group chats
    path('ws/group_chat/<int:group_id>/', consumers.GroupChatConsumer.as_asgi()),
]