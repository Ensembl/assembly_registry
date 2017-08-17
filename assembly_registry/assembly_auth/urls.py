from django.conf.urls import url
import assembly_auth.views
from django.conf import settings
from assembly_auth.views import CustomObtainAuthToken

try:
    base_html_dir = settings.BASE_HTML_DIR
except AttributeError:
    base_html_dir = ''


# Registration URLs
urlpatterns = [
               url(r'^register/$', assembly_auth.views.register),
               url(r'^register/complete/$', assembly_auth.views.registration_complete),
               ]

urlpatterns += [
    url(r'^get_auth_token/$', CustomObtainAuthToken.as_view(), name='get_auth_token'),
    url(r'^fetch_auth_token/$', assembly_auth.views.fetch_auth_token, name='fetch_auth_token')

 ]
