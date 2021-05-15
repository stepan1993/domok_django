from django.urls import path, include
from .views import *
from django.urls import  re_path

app_name = "main"
urlpatterns = [
    path('', index,name='index'),
    path('registration', registration),
    path('validate-username/',validate_username),
    
    re_path(r'^change-current-home/$', change_current_home, name='change-current-home'),
]
