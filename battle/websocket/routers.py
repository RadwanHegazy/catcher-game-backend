from django.urls import path
from .consumers import BattleConsumer, HomeConsumer, CreateBattleConsumer


websocket_urlpatterns = [
    path('battle/<str:battleuuid>/',BattleConsumer.as_asgi()),
    path('',HomeConsumer.as_asgi()),
    path('create/battle/',CreateBattleConsumer.as_asgi()),
]