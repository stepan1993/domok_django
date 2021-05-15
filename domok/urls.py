from django.contrib import admin
from django.urls import path
from django.contrib.auth.models import Group, User
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import include, url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('news/', include('news.urls')),
    path('chat/', include('chat.urls')),
    path('vote/', include('vote.urls')),
    path("ticket/",include('ticket.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('main.urls')),
    path('accounts/', include('django.contrib.auth.urls')), # ne
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.unregister(Group)
# admin.site.unregister(User)
admin.site.site_header = "ДомOK"
admin.site.site_title = "ДомOK"
admin.site.name = "ДомOK"