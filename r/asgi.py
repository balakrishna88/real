# r/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# Set the default settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'r.settings')

# Initialize Django
django_asgi_app = get_asgi_application()

# Import routing AFTER Django is initialized
from chat import routing  # noqa: E402 (disable import order warning)

# Define the ASGI application
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})
