from main.service import get_homes
from django.shortcuts import redirect, render
from .models import *
from .forms import NewsForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required

@login_required(login_url="/accounts/login/")
def news(request, pk):
    news = News.objects.get(id=pk)
    homes = get_homes(request)
    context = {'news':news,"homes":homes['homes'], "current":homes['current']}
    return render(request,'news/news.html', context)

@login_required(login_url="/accounts/login/")
def edit(request, pk):
    news = News.objects.get(id=pk) if pk != 0 else None
    initials = {"creator_id":request.user.id}
    news_objects = Object.objects.filter(object_moderators__id=request.user.id)
    form = NewsForm(instance=news,news_objects=news_objects, initial = initials)
    if request.method == 'POST':
        print(form.is_valid())
        print(form.errors)
        form = NewsForm(request.POST or None,instance=news,news_objects=news_objects, initial = initials)   
        if form.is_valid():
            form.save()
            return redirect(reverse('main:index'))
        else:
            form.errors
    else:
        form = NewsForm(instance=news,news_objects=news_objects, initial = initials) 
    homes = get_homes(request)
    context = {
        'form': form,
        "homes":homes['homes'], 
        "current":homes['current']
        }
    return render(request,'news/edit.html', context)

def delete(request):
    News.objects.get(id=request.GET.get('id')).delete()
    return redirect(reverse("main:index"))
