from django.conf.urls import url,include
from django.contrib import admin

urlpatterns = [
    url(r'',include('index.url')),
    url(r'', include('addwebshell.url')),
    url(r'', include('delwebshell.url')),
    url(r'', include('filebrowser.url')),
    url(r'', include('command.url')),
    url(r'^admin/', admin.site.urls),
]