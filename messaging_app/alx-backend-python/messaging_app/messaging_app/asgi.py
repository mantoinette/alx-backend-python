import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path
from chats.consumers import ChatConsumer  # You'll need to create this

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messaging_app.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                path('ws/chat/<str:room_name>/', ChatConsumer.as_asgi()),
            ])
        )
    ),
})
