from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.validation, name='validation'),
	url(r'^logout$', views.logout, name='logout'),
	url(r'^appointment$', views.index, name='index'),
	url(r'^appointment/(?P<id>\d+)$', views.show, name='show'),
	url(r'^appointment/(?P<id>\d+)/destroy$', views.destroy, name='destroy'),
]
