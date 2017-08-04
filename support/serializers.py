from rest_framework import serializers

from .models import *


class ProductSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Product
		lookup_field = 'sku'
		fields = (
			'brand', 
			'model', 
			'sku', 
			'category',
			'price_silver',
			'price_gold',
			'price_black',
			'with_cloud',
			'release',
		)

class CloudSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Cloud
		fields = (
			'name', 
			'image', 
			'price_modifier',
			'pk',
		)

class ClientSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Client
		fields = (
			'pk',
			'first_name', 
			'last_name', 
			'email',
			'phone',
			'company',
			'street',
			'street2',
			'city',
			'state',
			'country',
			'zipcode'
		)

class CartSerializer(serializers.ModelSerializer):
	class Meta:
		model = Cart
		fields = (
			'pk',
			'email', 
			'client', 
			'reference',
			'products',
		)