from rest_framework import serializers

from .models import *

class ProductCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductCategory
		fields = ('name', 'category_code', 'yearly_tax', 'price_multiplier')

class ProductSerializer(serializers.ModelSerializer):
	category = ProductCategorySerializer(many=False)

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
			'release',
		)

class CloudSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Cloud
		fields = (
			'name', 
			'image', 
			'price_multiplier',
			'quantity_multiplier',
			'pk',
		)

class DiscountSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Discount
		fields = (
			'year_threshold', 
			'discount_percent', 
			'pk',
		)


class PlanSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Plan
		fields = (
			'name',
			'color',
			'short_name', 
			'price', 
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
			'client',
			'length',
			'reference',
			'products',
			'plan'
		)

class CartSerializer2(serializers.ModelSerializer):
	class Meta:
		model = Cart
		fields = (
			'pk',
			'client',
			'length',
			'reference',
			'products',
			'cloud',
			'plan'
		)		