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
	url(r'^save-client/$', views.save_client_json, name="save_client"),
	url(r'^save-cart/$', views.save_cart_json, name="save_cart"),
]

urlpatterns += [
	url(r'^api/', include(router.urls)),
]