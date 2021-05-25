from django.http.response import JsonResponse
from chat.forms import ChatMessageForm
from main.service import get_homes
from django.shortcuts import render
from .models import *
import datetime
from django.contrib.auth.decorators import login_required

@login_required(login_url="/accounts/login/")
def chat(request):
    try:
        messages = ChatMessage.objects.filter(object_id=request.session.get('current_object'))
        messages.exclude(user_id = request.user.id).update(is_opened=True, opened_at = datetime.datetime.now())
    except:
        messages = None
    
    if request.method == "POST":
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            message = ChatMessage(text= form.cleaned_data['text'])
            message.object_id = request.session.get('current_object')
            message.user_id=request.user.id
            message.save()
            image = ""
            try:
                image = message.user.image.url
            except:
                image="/static/img/noavatar.png"
            return JsonResponse({
                "text":message.text,
                "name":message.user.first_name+" "+message.user.last_name,
                "image":image,
                "created_at":message.created_at
            }, safe=False)
    form = ChatMessageForm(initial={"user_id":request.user.id, "object_id":request.session.get('current_object')})
    homes = get_homes(request)
    context = {"homes":homes['homes'], "current":homes['current'], 'messages':messages, "form":form}
    return render(request,'chat/chat.html',context)

def get_new_messages(request):
    messages = ChatMessage.objects.filter(object_id=request.session.get('current_object'),
                                            is_opened=False).exclude(user_id = request.user.id)
    if messages.count()==0:
        obj = {
            "has_new":False,
            "messages":[]
        }
    else:
        mess = []
        for message in messages:
            try:
                image = message.user.image.url
            except:
                image="/static/img/noavatar.png"
            message.is_opened=True
            message.opened_at = datetime.datetime.now()
            message.save()
            mess.append({
                "text":message.text,
                "name":message.user.first_name+" "+message.user.last_name,
                "image":image,
                "created_at":message.created_at
            })
        obj  = {
            "has_new":True,
            "messages":mess
        }
    return JsonResponse(obj,safe=False)