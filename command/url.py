from django.conf.urls import url
from command import views
urlpatterns = [
    url(r'cmd.html',views.command),
    url(r'^runcommand.html', views.runcommand),
]