from django.urls import path
from .views import *
app_name = "problem"
urlpatterns = [
    path('problem', problem, name="problem"),
    path('details', details, name="details"),
    path('add', add, name="add"),
] 