from main.service import get_homes
from django.shortcuts import render
from .models import *

def problem(request):
    homes = get_homes(request)
    context = {"homes":homes['homes'], "current":homes['current']}
    return render(request,'problem/problem.html',context)

def details(request):
    homes = get_homes(request)
    context = {"homes":homes['homes'], "current":homes['current']}
    return render(request,'problem/details.html',context)
def add(request):
    homes = get_homes(request)
    context = {"homes":homes['homes'], "current":homes['current']}
    return render(request,'problem/add.html',context)
