import os

from django.core.asgi import get_asgi_application

# Imported 
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
from chat import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'learning.settings')

application = ProtocolTypeRouter(
    {
        'http' : get_asgi_application(),
        'websocket' : AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(routing.websockets_urlspattern))
        ) 
    }
)
