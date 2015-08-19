from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/', views.index),
 	url(r'^champions/([0-9]+)', views.champions),
 	url(r'^items/([0-9]+)', views.items),
]
 	