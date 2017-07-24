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
        	'price_silver',
        	'price_gold',
        	'price_black',
        	'with_cloud',
        )

class CloudSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cloud
        fields = (
            'name', 
            'image', 
            'price_modifier', 
        )