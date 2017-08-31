"""mibura_new URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static

from django.contrib.sitemaps.views import sitemap


from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', views.index, name="index"),
    url(r'^index/', views.index, name="index"),
    url(r'^.well-known/pki-validation/$', views.ssl_verification, name="ssl-verification"),
    url(r'^company/', include('company.urls')),
    url(r'^datacenter/', include('datacenter.urls', namespace="datacenter")),
    url(r'^cloud/', include('cloud.urls', namespace="cloud")),
    url(r'^support/', include('support.urls', namespace="support")),
    url(r'^staffing/', include('staffing.urls', namespace="staffing")),
    
    # SEO
    url(r'^robots\.txt$', views.robot_txt),
    url(r'^sitemap\.xml$', views.sitemap),

    # Staticfiles
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)