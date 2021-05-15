from users.models import Account
from vote.forms import VoteForm
from main.service import get_homes
from django.shortcuts import redirect, render
from .models import *
from django.urls import reverse

def vote(request):
    if request.user.role == "moderator":
        votes = Vote.objects.filter(object_id=request.session.get('current_object'))
    else:
        votes = Vote.objects.filter(start_date__lte=datetime.date.today(),object_id=request.session.get('current_object'))
    search_word = request.GET.get('name') if request.GET.get('name') else ""
    if search_word != "":
        votes = votes.filter(question__icontains=search_word)
    homes = get_homes(request)
    context = {"homes":homes['homes'], "current":homes['current'],"votes":votes.order_by('-id'),"search_word":search_word}
    return render(request,'vote/vote.html',context)

def add(request, id):
    initials = {"created_by_id":request.user.id,'object_id':request.session.get('current_object')}
    vote = Vote.objects.get(id=id) if id!=0 else None
    form = VoteForm(instance=vote,initial=initials)
    if request.method == 'POST':
        form = VoteForm(request.POST,initial=initials,instance=vote)   
        if form.is_valid():
            form.save()
            return redirect(reverse('vote:vote'))
        else: 
            form.errors
            form = VoteForm(request.POST,initial=initials)
    homes = get_homes(request)
    context = {"homes":homes['homes'], "current":homes['current'],"form":form}
    return render(request,'vote/add.html',context)

def set_vote(request, id):
    vote = Vote.objects.get(id=id)
    try:
        vote_member = VoteMember.objects.get(vote_id=id, member_id = request.user.id)
    except:
        vote_member = None
    if request.method=="POST":
        data = request.POST
        if vote_member is None:
            vote_member = VoteMember(vote_id=id, member_id = request.user.id,point=data['vote'])
            vote_member.save()
        else:
            vote_member.point = data['vote']
            vote_member.save()
        return redirect("/vote/set-vote/"+str(id))
    homes = get_homes(request)
    context = {"homes":homes['homes'], "current":homes['current'],"vote":vote,"vote_member":vote_member}
    return render(request,'vote/set-vote.html',context)

def result(request, id):
    vote = Vote.objects.get(id=id)  
    homes = get_homes(request)
    context = {"homes":homes['homes'], "current":homes['current'],"vote":vote}
    return render(request,'vote/result.html',context)

def members(request, id):
    vote = Vote.objects.get(id=id)  
    members = vote.vote_members.all()    
    homes = get_homes(request)
    context = {"homes":homes['homes'], "current":homes['current'],"vote":vote,"members":members}
    return render(request,'vote/members.html',context)
