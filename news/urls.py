from django.urls import path, re_path
from .views import *
app_name = "news"
urlpatterns = [
    path('news/<int:pk>', news, name="news"),
    path('edit/<int:pk>', edit, name="edit"),
    re_path(r'^delete/$', delete, name='delete'),
] 