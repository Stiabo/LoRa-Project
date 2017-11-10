from django.conf.urls import include, url

from . import views

app_name = 'demo'
urlpatterns = [
    url(r'^$', views.home, name='home'),
]
