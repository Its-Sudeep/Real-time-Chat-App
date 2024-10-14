from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('chatpage/<str:username>', views.chatpage, name='chatpage'),
    path('chatpage/<str:username>/<str:room_name>', views.index, name= 'index'),
]



# admin superuser -- admin, pas-- 123