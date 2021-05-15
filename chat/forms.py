from .models import ChatMessage
from django import forms


class ChatMessageForm(forms.ModelForm):
    text = forms.CharField(max_length=100, widget=forms.Textarea(
                                attrs={'class': "form-control",'placeholder': 'Введите сообщение',"cols":30,'rows':3}))

    class Meta:
        model = ChatMessage
        fields = ('text',)
