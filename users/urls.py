from main.views import validate_username
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from django.urls import include, re_path
from .views import account, contacts,  owners, profile, set_password, upload,  upload_account
app_name = 'users'

urlpatterns = [
    re_path(r'^set-password/(?P<pk>\w+)/$', set_password, name='set-password'),
    path('upload-account/',upload_account),
    
    path('contacts', contacts,name="contacts"),
    path('owners', owners,name="owners"),
    path('account', account,name="account"),
    path('profile', profile,name="profile"),
    path('upload', upload,name="upload"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)