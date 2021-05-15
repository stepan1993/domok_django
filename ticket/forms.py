from service.models import Service
from .models import Comment, Ticket, TicketFile
from django import forms

class TicketForm(forms.ModelForm):
    whom = forms.ModelChoiceField(queryset = Service.objects.all(),
                    widget=forms.Select(attrs={'class': "form-control",'placeholder': 'Кому'}))
    problem = forms.CharField(required=True, max_length=100, widget=forms.TextInput(
                                attrs={'class': "form-control",'placeholder': 'Проблема'}))
    description = forms.CharField(required=False,widget=forms.Textarea(
                                attrs={'class': "form-control",'placeholder': 'Подробнее о проблеме'}))
    author_id = forms.IntegerField(required=False,widget=forms.TextInput(attrs={'class': "hidden"}))
    object_id = forms.IntegerField(required=False,widget=forms.TextInput(attrs={'class': "hidden"}))

    class Meta:
        model = Ticket
        fields = ('whom','problem','description','author_id','object_id')

    def save(self, commit=True):
        ticket = super(TicketForm, self).save(commit=False)
        ticket.author_id = self.cleaned_data['author_id']
        ticket.object_id = self.cleaned_data['object_id']
        ticket.save()
        return ticket


class CommentForm(forms.ModelForm):
    comment = forms.CharField(required=False,widget=forms.Textarea(
                                attrs={'class': "form-control","cols":30,"rows":5,'placeholder': 'Комментарий'}))
    author_id = forms.IntegerField(required=False,widget=forms.TextInput(attrs={'class': "hidden"}))
    ticket_id = forms.IntegerField(required=False,widget=forms.TextInput(attrs={'class': "hidden"}))
    class Meta:
        model = Comment
        fields = ('comment','author_id','ticket_id')

    def save(self, commit=True):
        ticket = super(CommentForm, self).save(commit=False)
        ticket.author_id = self.cleaned_data['author_id']
        ticket.ticket_id = self.cleaned_data['ticket_id']
        ticket.save()
        return ticket

