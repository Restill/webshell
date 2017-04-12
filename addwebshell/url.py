from django.conf.urls import url
from addwebshell import views
urlpatterns = [
    url(r'add.html',views.add)
]