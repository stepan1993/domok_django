from location.models import Object
from django.db import models
from django.db.models.deletion import DO_NOTHING
from ckeditor_uploader.fields import  RichTextUploadingField
from users.models import CustomUser

class News(models.Model):
    title = models.CharField(max_length=255,null=False,blank=False, verbose_name="Название")
    short_description = models.TextField(null=False,blank=False, verbose_name="Коротко")
    text = RichTextUploadingField(verbose_name="Контент")
    creator = models.ForeignKey(CustomUser, on_delete=DO_NOTHING, null=False, blank=True, verbose_name="Создатель")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    news_objects = models.ManyToManyField(Object, blank=True, null=True)
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'Новости'
        verbose_name = 'Новост'
