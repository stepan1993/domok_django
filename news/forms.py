from django.forms.widgets import CheckboxSelectMultiple
from location.models import Object
from .models import News
from django import forms
from ckeditor.widgets import CKEditorWidget


class NewsForm(forms.ModelForm):
    title = forms.CharField(max_length=100, widget=forms.TextInput(
                                attrs={'class': "form-control",'placeholder': 'Название новости'}))
    short_description = forms.CharField(max_length=100,widget=forms.Textarea(
                                attrs={'class': "form-control",'placeholder': 'Коротко', "rows":5}))
    creator_id = forms.IntegerField(widget=forms.TextInput(attrs={'class': "hidden"}))
    text = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = News
        fields = ('title','short_description','text','creator_id', 'news_objects')

    def __init__(self, *args, **kwargs):
        self.objs = kwargs.get('news_objects', None)
        del kwargs['news_objects']
        super(NewsForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['news_objects'].initial = self.instance.news_objects.all()
        self.fields["news_objects"].widget = CheckboxSelectMultiple()
        self.fields["news_objects"].queryset = self.objs
        self.fields["news_objects"].required = True
    def save(self, commit=True):
        news = super(NewsForm, self).save(commit=False)
        if commit:
            news.creator_id = self.cleaned_data['creator_id']
            news.save()
        if news.pk:
            news.news_objects.set(self.cleaned_data['news_objects'])
            self.save_m2m()
        return news
