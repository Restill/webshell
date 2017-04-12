from django.conf.urls import url
from filebrowser import views
urlpatterns = [
    url(r'filebrowser.html',views.filebrowser),
    url(r'getfile.html',views.getfile),
]