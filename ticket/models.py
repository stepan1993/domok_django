from django.db.models.query import NamedValuesListIterable
from service.models import Service
from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from location.models import Object
from users.models import CustomUser
STATUS_CHOICES = [
    (1,"На рассмотрении"),
    (3,"Принято к исполнению"),
    (3,"Выполнено")
]

class Ticket(models.Model):
    object = models.ForeignKey(Object, on_delete=CASCADE, null=False, blank=False, related_name="object_tickets")
    author = models.ForeignKey(CustomUser, on_delete=CASCADE, null=False, blank=False, related_name="user_tickets")
    problem = models.CharField(max_length=500,null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    whom = models.ForeignKey(Service, on_delete=PROTECT, null=False, blank=False)
    status = models.IntegerField(choices=STATUS_CHOICES,  null=False, blank=False, default=1)
    accepted = models.BooleanField(default=False)
    accepted_by = models.ForeignKey(CustomUser, on_delete=CASCADE, null=True, blank=True)
    finished = models.BooleanField(default=False)
    finish_accepted = models.BooleanField(default=False)

class TicketFile(models.Model):
    ticket = models.ForeignKey(Ticket, null=False, blank=False, on_delete=CASCADE, related_name="ticket_files")
    file = models.FileField(null=True)
    size = models.CharField(max_length=255,null=False, blank=False)

    def __str__(self):
        return f"{self.file.url} ({self.size} Кб)"

class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, null=False, blank=False, on_delete=CASCADE, related_name="ticket_comments")
    comment = models.TextField(null=True)
    author = models.ForeignKey(CustomUser, on_delete=CASCADE, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.comment}"

class CommentFile(models.Model):
    comment = models.ForeignKey(Comment, null=False, blank=False, on_delete=CASCADE, related_name="comment_files")
    file = models.FileField(null=True)
    size = models.CharField(max_length=255,null=False, blank=False)

    def __str__(self):
        return f"{self.file.url} ({self.size} Кб)"

class TicketStatusHistory(models.Model):
    ticket = models.ForeignKey(Ticket, null=False, blank=False, on_delete=CASCADE, related_name="ticket_status_histories")
    user = models.ForeignKey(CustomUser, on_delete=CASCADE, null=False, blank=False)
    status = models.IntegerField(choices=STATUS_CHOICES, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    