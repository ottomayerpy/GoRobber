from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path

from service.consumers import GameConsumer

application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                path('case/<int:number>/', GameConsumer),
                path('', GameConsumer),
                path('profile/', GameConsumer),
                path('profile/login/', GameConsumer),
                path('profile/levels/', GameConsumer),
                path('profile/finance/', GameConsumer),
                path('profile/id<int:id>/', GameConsumer),
                path('support/terms/', GameConsumer),
                path('support/privacy/', GameConsumer),
                path('support/send_message/', GameConsumer),
                path('support/', GameConsumer),
                path('rating/', GameConsumer),
                path('payouts/', GameConsumer),
            ])
        )
    )
})
