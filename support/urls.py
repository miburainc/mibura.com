from django.conf.urls import url, include

from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r'products', views.ProductViewSet)
router.register(r'productcomplete', views.ProductAutocompleteViewSet)
router.register(r'cloud', views.CloudViewSet)
router.register(r'categories', views.CategoriesViewSet)
router.register(r'discounts', views.DiscountViewSet)

urlpatterns = [
	url(r'^$', views.index, name="index"),
	url(r'^purchase/$', views.purchase, name="purchase"),
	
	# API
	url(r'^save-client/$', views.save_client_json, name="save_client"),
	url(r'^get-or-create-cart/$', views.get_create_cart, name="get_create_cart"),
	url(r'^get-or-create-client/$', views.get_create_client, name="get_create_client"),
	url(r'^get-estimate-pdf/$', views.get_estimate_pdf, name="get_estimate_pdf"),
	url(r'^send-quote-email/$', views.email_estimate_pdf, name="send_quote_email"),
	url(r'^get-previous-estimate/$', views.get_previous_estimate, name="get_previous_estimate"),
	url(r'^checkout/$', views.checkout, name="checkout"),
	url(r'^plaid-credentials/$', views.plaid_credentials, name="plaid_credentials"),
]

urlpatterns += [
	url(r'^api/', include(router.urls)),
]