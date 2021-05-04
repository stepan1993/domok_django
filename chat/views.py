from main.service import get_homes
from django.shortcuts import render
from .models import *

def chat(request):
    homes = get_homes(request)
    context = {"homes":homes['homes'], "current":homes['current']}
    return render(request,'chat/chat.html',context)
