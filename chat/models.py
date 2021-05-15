from django.db.models.deletion import CASCADE
from location.models import Object
from django.db import models
from users.models import CustomUser

class ChatMessage(models.Model):
    user = models.ForeignKey(CustomUser, null=False,blank=False, related_name="user_messages", on_delete=CASCADE)
    object = models.ForeignKey(Object, null=False, blank=False, related_name="object_messages",on_delete=CASCADE)
    text = models.TextField(null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    opened_at = models.DateTimeField(null=True, blank=True)
    is_opened = models.BooleanField(default=False)

    def __str__(self):
        return self.text
