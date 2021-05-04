from news.models import News
from django.contrib import admin
from django.utils.html import format_html

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    fields = ('title', 'short_description','is_active','text')
    list_display = ('title', 'short_description',  'creator','created_at','is_active','change_button')
    search_fields = ['title']
    readonly_fields = ( 'creator','created_at',)


    def save_model(self, request, obj, form, change):
        obj.creator = request.user
        obj.save()
    
    def change_button(self, obj):
        return format_html('<a class="btn deletelink" href="/admin/news/news/{}/delete/"></a>', obj.id,obj.id)
    change_button.short_description=" "
