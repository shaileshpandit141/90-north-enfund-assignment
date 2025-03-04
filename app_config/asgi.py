"""ASGI config for app_config project.
It exposes the ASGI callable as a module-level variable named ``application``.
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app_config.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        # "websocket": URLRouter(),
    }
)
