from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse

from django.conf import settings

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request

from .models import Product, Cloud, Client, Cart, ClientProduct
from .serializers import CartSerializer, ProductSerializer, CloudSerializer, ClientSerializer

from scripts.dotdict import dotdict

import json
import stripe

# Pages

def index(request):
	"""
	View function for home page of site.
	"""
	# Render the HTML template index.html with the data in the context variable
	context = {}
	context['DEBUG'] = settings.DEBUG

	return render(
		request,
		'support/support.html',
		context
	)

def purchase(request):
	"""
	View function for home page of site.
	"""

	# Render the HTML template index.html with the data in the context variable
	context = {}
	context['DEBUG'] = settings.DEBUG
	print(context)
	return render(
		request,
		'support/purchase.html',
		context
	)

@csrf_exempt
def get_create_client(request):
	if request.method == 'POST':
		data = json.loads(request.body.decode("utf-8"))
		data = dotdict(data) # access properties with . instead of []

		obj,created = Client.objects.get_or_create(email=data.email)
		if created:
			obj.first_name = data.first_name
			obj.last_name = data.last_name
			obj.phone = data.phone
			obj.company = data.company
			obj.street = data.street
			if data.street2:
				obj.street2 = data.street2
			obj.city = data.city
			obj.country = data.country
			obj.zipcode = data.zipcode
			obj.save()
			serialized = ClientSerializer(obj)
			response_json = JSONRenderer().render(serialized.data)

			return HttpResponse(response_json, status=201)
		else:
			for field,value in obj.__dict__.items():
				print(field)
				if not value and field in data:
					setattr(obj, field, data[field])
					obj.save()
				print(value)
		serialized = ClientSerializer(obj)
		response_json = JSONRenderer().render(serialized.data)

		return HttpResponse(response_json, status=200)

@csrf_exempt
def save_client_json(request):
	if request.method == 'POST':
		data = json.loads(request.body.decode("utf-8"))
		print('Raw Data: "%s"' % data)
	return HttpResponse("OK")

@csrf_exempt
def get_create_cart(request):
	if request.method == 'POST':
		data = json.loads(request.body.decode("utf-8"))
		data = dotdict(data)

		if not data.client:
			HttpResponse("No Client ID", status=400)
		print(data.client)
		client = Client.objects.get(pk=data.client)
		cart,created = Cart.objects.get_or_create(client=client, reference=data.reference)
		
		for prod in data.products:
			prod = dotdict(prod)
			obj,created = ClientProduct.objects.get_or_create(client=client, brand=prod.brand, model=prod.model, serial_number=prod.sn)
			if not obj in cart.products.all():
				cart.products.add(obj)
		print(data.plan)
		cart.plan = data.plan
		cart.save()
		serializer_context = {
			'request': Request(request),
		}
		serialized = CartSerializer(cart, context=serializer_context)
		response_json = JSONRenderer().render(serialized.data)

	return HttpResponse(response_json, status=200)


# API

class CloudViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Cloud.objects.all().order_by('-name')
	serializer_class = CloudSerializer

	def get_queryset(self):
		cloud = self.request.query_params.get('cloud', None)
		if cloud:
			queryset = Cloud.objects.filter(name__icontains=cloud)
		else:
			queryset = Cloud.objects.all()
		return queryset

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
	"""
	API endpoint that allows products to be viewed or edited.
	"""
	queryset = Product.objects.all().order_by('-model')
	serializer_class = ProductSerializer
	lookup_field = 'sku'

class ProductAutocompleteViewSet(viewsets.ReadOnlyModelViewSet):
	"""
	API endpoint that allows products to be viewed or edited.
	"""
	queryset = Product.objects.all().order_by('-model')
	serializer_class = ProductSerializer
	
	def get_queryset(self):
		queryset = Product.objects.all()
		brand = self.request.query_params.get('brand', None)
		model = self.request.query_params.get('model', None)
		if brand:
			queryset = queryset.filter(brand__icontains=brand)
			if not model:
				items, item_ids = [], []
				for item in queryset:
					if item.brand not in item_ids:
						items.append(item)
						item_ids.append(item.brand)
						queryset = items
		if model:
			queryset = queryset.filter(model__icontains=model)
		
			

		return queryset

@api_view(['GET', 'POST'])
def support_cart_create(request):
	"""
	List all snippets, or create a new snippet.
	"""
	if request.method == 'GET':
		snippets = Product.objects.all()
		serializer = SnippetSerializer(snippets, many=True)
		return Response(serializer.data)

	elif request.method == 'POST':
		serializer = SnippetSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)