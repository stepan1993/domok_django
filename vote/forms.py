from .models import Vote, VOTE_TYPES, QUORUM_CHOICES
from django import forms
from datetime import datetime,date
class VoteForm(forms.ModelForm):
    question = forms.CharField(required=True, max_length=100, widget=forms.TextInput(
                                attrs={'class': "form-control",'placeholder': 'Вопрос'}))
    description = forms.CharField(required=False,widget=forms.Textarea(
                                attrs={'class': "form-control",'placeholder': 'Описание'}))
    start_date = forms.DateField(required=True,widget=forms.DateInput(
                                attrs={'class': "form-control"}))
    end_date = forms.DateField(required=True, widget=forms.DateInput(
                                attrs={'class': "form-control"}))
    vote_type = forms.TypedChoiceField(choices = VOTE_TYPES,coerce = str,
                    widget=forms.Select(attrs={'class': "form-control"}))
    quorum = forms.TypedChoiceField(choices = QUORUM_CHOICES,coerce = str,
                    widget=forms.Select(attrs={'class': "form-control"}))
    created_by_id = forms.IntegerField(widget=forms.TextInput(attrs={'class': "hidden"}))
    object_id = forms.IntegerField(widget=forms.TextInput(attrs={'class': "hidden"}))
    class Meta:
        model = Vote
        fields = ('question','description','start_date','end_date','vote_type','quorum','created_by_id','object_id')

    def save(self, commit=True):
        news = super(VoteForm, self).save(commit=False)
        news.created_by_id = self.cleaned_data['created_by_id']
        news.object_id = self.cleaned_data['object_id']
        news.save()
        return news

    def clean_start_date(self):
        if self.cleaned_data.get('start_date') < date.today():
            raise forms.ValidationError("Дата начала не может быть в прошлом даты.")
        return self.cleaned_data.get('start_date')
    def clean_end_date(self):
        if self.cleaned_data.get('start_date'):
            if self.cleaned_data.get('end_date') <= self.cleaned_data.get('start_date'):
                raise forms.ValidationError("Дата окончания не может быть меньше даты начала.")
        return self.cleaned_data.get('end_date')
