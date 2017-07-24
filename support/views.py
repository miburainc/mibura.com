from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product, Cloud
from .serializers import ProductSerializer, CloudSerializer



# Pages

def index(request):
	"""
	View function for home page of site.
	"""
	# Render the HTML template index.html with the data in the context variable
	return render(
		request,
		'support/support.html',
		{}
	)

def purchase(request):
	"""
	View function for home page of site.
	"""

	# Render the HTML template index.html with the data in the context variable
	return render(
		request,
		'support/purchase.html',
		
	)


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