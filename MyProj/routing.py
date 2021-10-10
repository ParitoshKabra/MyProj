from channels.auth import AuthMiddleWareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import trelloAPIs.routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddleWareStack(
        URLRouter(
            trelloAPIs.routing.websocket_urlpatterns
        )
    )
})