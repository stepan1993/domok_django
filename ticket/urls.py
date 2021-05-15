from django.urls import path
from .views import *
app_name = "ticket"
urlpatterns = [
    path('ticket', ticket, name="ticket"),
    path('details/<int:pk>', details, name="details"),
    path('add', add, name="add"),

    path('subscribe/<int:pk>', subscribe, name="subscribe"),
    path('unsubscribe/<int:pk>', unsubscribe, name="unsubscribe"),
    path('finish/<int:pk>', finish, name="finish"),
    path('accept-finish/<int:pk>', accept_finish, name="accept-finish"),
    path('decline-finish/<int:pk>', decline_finish, name="decline-finish"),
]