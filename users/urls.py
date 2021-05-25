from main.views import validate_username
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from django.urls import  re_path
from .views import (account, contacts, owner,  owners, profile, set_password, upload,  
upload_account, upload_faktura, upload_fakturas,  upload_owner_image)
app_name = 'users'

urlpatterns = [
    re_path(r'^set-password/(?P<pk>\w+)/$', set_password, name='set-password'),
    path('upload-account/',upload_account),
    path('upload-fakturas/',upload_fakturas),
    path('contacts', contacts,name="contacts"),
    path('owners', owners,name="owners"),
    path('account', account,name="account"),
    path('upload-faktura', upload_faktura,name="upload-faktura"),
    path('profile', profile,name="profile"),
    path('upload', upload,name="upload"),
    path('upload-owner-image/<int:pk>', upload_owner_image,name="upload-owner-image"),
    path('owner/<int:pk>', owner,name="owner"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
