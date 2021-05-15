from django.urls import path
from .views import *
app_name = "chat"
urlpatterns = [
    path('chat', chat, name="chat"),
    path('get-new-messages', get_new_messages, name="get-new-messages"),
] 