# mysite/asgi.py
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import file_sharing.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "file_sharing_project.settings")

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            file_sharing.routing.websocket_urlpatterns
        )
    ),
})