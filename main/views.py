from django.db.models.query_utils import Q
from main.service import get_homes
from django.http.response import HttpResponse, JsonResponse
from users.models import Account, CustomUser
from django.shortcuts import redirect, render
from news.models import News
from django.core.paginator import Paginator
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from users.forms import RegistrationForm
from django.urls import reverse

def registration(request):
    initials = {'phone_number':""}
    form = RegistrationForm(request.POST or None,initial=initials)
    if request.method=="POST":
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return render(request,'registration/registration.html',context={"succeed":True})
        else: 
            form.errors
            form = RegistrationForm(request.POST,initial=initials)
    context = {'form':form}
    return render(request,'registration/registration.html',context)

def validate_username(request):
        username = request.GET.get('username')
        if Account.objects.filter(account=username).count()==0:
            return JsonResponse({"is_valid":False,"message":"Лицевой счет не найден"})
        if CustomUser.objects.filter(username=username).count()>0:
            return JsonResponse({"is_valid":False,"message":"По данному лицевому счету уже зарегистрирован пользователь"})
        return JsonResponse({"is_valid":True,"message":""})

def logout_view(request):
    logout(request)
    return redirect('registration/login.html')

@login_required(login_url="/accounts/login/")
def index(request):
    try:
        news = News.objects.filter(is_active=True).filter(Q(creator__role = "administrator") | 
                                                    Q(news_objects__id =request.session['current_object'])).order_by("-id")
    except:
        news = News.objects.filter(is_active=True).filter(Q(creator__role = "administrator")).order_by("-id")
    paginator = Paginator(news, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    homes = get_homes(request)
    context = { 'news':page_obj,"homes":homes['homes'], "current":homes['current']}
    return render(request,'main/index.html', context)

def change_current_home(request):
    request.session['current_object'] = request.GET.get('id')
    return redirect(reverse('main:index'))
