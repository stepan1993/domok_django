from django.urls import path
from .views import *
app_name = "vote"
urlpatterns = [
    path('vote', vote, name="vote"),
    path('details', details, name="details"),
] 