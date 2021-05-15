from ticket.forms import CommentForm, TicketForm
from main.service import get_homes
from django.shortcuts import render, redirect
from .models import *
from django.urls import reverse
STATUSES = {
    1:"На рассмотрении",
    2:"На рассмотрении",
    3:"Выполнено"
}

def ticket(request):
    tickets = Ticket.objects.filter(object_id = request.session.get('current_object')).order_by('-id')
    homes = get_homes(request)
    context = {"homes":homes['homes'], "current":homes['current'],"tickets":tickets}
    return render(request,'ticket/ticket.html',context)

def details(request, pk):
    ticket = Ticket.objects.get(id = pk)
    ticket_files = ticket.ticket_files.all()
    status = STATUSES[ticket.status]
    initials = {"author_id":request.user.id,'ticket_id': pk}
    form = CommentForm(initial=initials)
    if request.method == 'POST':
        form = CommentForm(request.POST, initial=initials)   
        if form.is_valid():
            comment = form.save(commit=False)
            for afile in request.FILES.getlist('file[]'):
                handle_uploaded_file(afile,"media/ticket/comment/"+str(comment.id))
                file = CommentFile(comment_id=comment.id, file = str(comment.id)+afile.name, size = round(afile.size/1024,2))
                file.save()
            ticket.save()
            form=CommentForm(initial=initials)   
        else:
            form.errors
            form = CommentForm(request.POST,initial=initials)
    comments = [(comment,comment.comment_files.all()) for comment in ticket.ticket_comments.all()]

    homes = get_homes(request)
    context = {"homes":homes['homes'], "current":homes['current'],"ticket":ticket, 
                    "status":status,"ticket_files":ticket_files,"comment_form":form,"comments":comments}
    return render(request,'ticket/details.html',context)
    
def add(request):
    initials = {"author_id":request.user.id,'object_id': request.session.get('current_object')}
    form = TicketForm(initial=initials)
    if request.method == 'POST':
        form = TicketForm(request.POST, initial=initials)   
        if form.is_valid():
            ticket = form.save(commit=False)
            for afile in request.FILES.getlist('file[]'):
                handle_uploaded_file(afile,"media/ticket/")
                file = TicketFile(ticket_id=ticket.id, file = afile.name,size = round(afile.size/1024,2))
                file.save()
            ticket.save()
            TicketStatusHistory(user=request.user, ticket=ticket, status=1).save()
            return redirect(reverse('ticket:ticket'))
        else:
            form.errors
            form = TicketForm(request.POST,initial=initials)
    homes = get_homes(request)
    context = {"homes":homes['homes'], "current":homes['current'], "form":form}
    return render(request,'ticket/add.html',context)

def handle_uploaded_file(f, path):
    destination = open(path+f.name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

def subscribe(request, pk):
    ticket = Ticket.objects.get(id=pk)
    ticket.status = 2
    ticket.accepted = True
    ticket.accepted_by = request.user
    ticket.save()
    TicketStatusHistory(user=request.user, ticket=ticket, status=2).save()
    return redirect("/ticket/details/"+str(pk))

def unsubscribe(request, pk):
    ticket = Ticket.objects.get(id=pk)
    ticket.status = 1
    ticket.accepted = False
    ticket.accepted_by = None
    ticket.finished = False
    ticket.finish_accepted = False
    ticket.save()
    TicketStatusHistory(user=request.user, ticket=ticket, status=1).save()
    return redirect("/ticket/details/"+str(pk))

def finish(request, pk):
    ticket = Ticket.objects.get(id=pk)
    ticket.status = 3
    ticket.finished = True
    ticket.finish_accepted = False
    ticket.save()
    TicketStatusHistory(user=request.user, ticket=ticket, status=3).save()
    return redirect("/ticket/details/"+str(pk))

def accept_finish(request, pk):
    ticket = Ticket.objects.get(id=pk)
    ticket.finish_accepted = True
    ticket.save()
    TicketStatusHistory(user=request.user, ticket=ticket, status=3).save()
    return redirect("/ticket/details/"+str(pk))

def decline_finish(request, pk):
    ticket = Ticket.objects.get(id=pk)
    ticket.status = 2
    ticket.finished = False
    ticket.finish_accepted = False
    ticket.save()
    TicketStatusHistory(user=request.user, ticket=ticket, status=2).save()
    return redirect("/ticket/details/"+str(pk))
