from django.conf.urls import url
from index import views
urlpatterns = [
    url(r'^$|^index.html$',views.index)
]