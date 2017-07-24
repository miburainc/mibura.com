from django.conf.urls import url, include

from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r'products', views.ProductViewSet)
router.register(r'productcomplete', views.ProductAutocompleteViewSet)
router.register(r'cloud', views.CloudViewSet)


urlpatterns = [
	url(r'^$', views.index, name="index"),
	url(r'^purchase/$', views.purchase, name="purchase"),
]

urlpatterns += [
	url(r'^api/', include(router.urls)),
]