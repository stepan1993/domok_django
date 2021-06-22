from django.shortcuts import render
from .models import *

def problem(request):
    return render(request,'problem/problem.html')

def details(request):
    return render(request,'problem/details.html')
def add(request):
    return render(request,'problem/add.html')
