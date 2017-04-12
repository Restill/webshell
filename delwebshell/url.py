from django.conf.urls import url
from delwebshell import views
urlpatterns = [
    url(r'del.html',views.delete)
]