"""
ASGI config for Missing Persons Finder project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

# Initialize Django ASGI application
django_asgi_app = get_asgi_application()

# Import websocket URLs after Django setup
#from search_manager.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    # Uncomment this when websocket_urlpatterns is defined
    #"websocket": AuthMiddlewareStack(
    #    URLRouter(
    #        websocket_urlpatterns
    #    )
    #),
})
