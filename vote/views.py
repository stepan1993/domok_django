from main.service import get_homes
from django.shortcuts import render
from .models import *

def vote(request):
    homes = get_homes(request)
    context = {"homes":homes['homes'], "current":homes['current']}
    return render(request,'vote/vote.html',context)

def details(request):
    homes = get_homes(request)
    context = {"homes":homes['homes'], "current":homes['current']}
    return render(request,'vote/details.html',context)
