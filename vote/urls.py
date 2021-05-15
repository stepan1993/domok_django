from django.urls import path
from .views import *
app_name = "vote"
urlpatterns = [
    path('vote', vote, name="vote"),
    path('add/<int:id>', add, name="add"),
    path('result/<int:id>', result, name="result"),
    path('members/<int:id>', members, name="members"),
    path('set-vote/<int:id>', set_vote, name="set-vote"),
]