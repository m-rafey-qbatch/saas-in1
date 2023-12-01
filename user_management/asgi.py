import os
from django.core.asgi import get_asgi_application

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'user_management.settings')

# Setup Django FIRST
django_asgi_app = get_asgi_application()


from channels.routing import ProtocolTypeRouter, URLRouter
from users.middleware import ChatAuthMiddleware
from .routing import websocket_urlpatterns
from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({
    "http": django_asgi_app,  # For handling the normal http requests
    "websocket": AuthMiddlewareStack(
        ChatAuthMiddleware(
            URLRouter(
                websocket_urlpatterns
            )
        )
    ),
})
