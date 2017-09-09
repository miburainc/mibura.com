from django.conf.urls import url, include

from . import views


urlpatterns = [
	url(r'^$', views.index, name='company'),
	url(r'^thanks/$', views.index, name='company-thanks'),
	url(r'^career/(?P<slug>[\w-]+)/$', views.job, name='career'),
]