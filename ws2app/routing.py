from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/sc/<str:username>/<str:group_name>/', consumers.MySyncConsumer.as_asgi()),
    path('ws/ac/<str:username>/<str:group_name>/', consumers.MyAsyncConsumer.as_asgi()),
]