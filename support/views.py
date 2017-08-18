from datetime import datetime
from wsgiref.util import FileWrapper
import os, json, math, stripe
from copy import deepcopy

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone, encoding
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request

from .models import *
from .serializers import *

from freshbooks import estimates
from scripts.dotdict import dotdict
from scripts.sss_pricing import product_price, cloud_price

stripe.api_key = settings.PINAX_STRIPE_SECRET_KEY

#################
# Email
#################

def send_quote_email(name, recipient, subject, file):
	to = [recipient]
	from_email = 'cs@mibura.com'

	print(name)

	ctx = {
		'name': name,
	}

	message = get_template('email/quote.html').render(ctx)
	msg = EmailMessage(subject, message, to=to, from_email=from_email)
	msg.attach_file(file)
	msg.content_subtype = 'html'
	return msg.send()


#################
# Pages
#################

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
	
	return render(
		request,
		'support/purchase.html',
		context
	)

#################
# Api endpoints 
#################

@csrf_exempt
def get_create_client(request):
	if request.method == 'POST':
		data = json.loads(request.body.decode("utf-8"))
		# data = json.loads(request.body)
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
			obj.state = data.state
			obj.country = data.country
			obj.zipcode = data.zipcode
			obj.save()

			return HttpResponse(obj.pk, status=201)
		else:
			obj.save()
			for field,value in obj.__dict__.items():
				if not value and field in data:
					setattr(obj, field, data[field])
			# After loop, save object and return
			obj.save()

			return HttpResponse(obj.pk, status=200)

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
		client = Client.objects.get(pk=data.client)
		cart,created = Cart.objects.get_or_create(client=client, reference=data.reference, email=data.email)
		cart.products.clear()

		for prod in data.products:
			prod = dotdict(prod)
			
			if prod.type == "cloud":
				cloud = Cloud.objects.get(name=prod.brand)
				cart.cloud.add(cloud)
			else:
				try:
					prod_obj = Product.objects.get(brand=prod.brand, model=prod.model)
				except ObjectDoesNotExist:
					cat = ProductCategory.objects.get(category_code="none")
					prod_obj = Product(brand=prod.brand, model=prod.model, category=cat, sku='NONE', approved=False)
					prod_obj.save()

				obj,created = ClientProduct.objects.get_or_create(client=client, brand=prod.brand, model=prod.model, serial_number=prod.sn, product=prod_obj)

				if not obj in cart.products.all():
					cart.products.add(obj)
				
		cart.plan = data.plan
		cart.length = data.length
		cart.save()
		serializer_context = {
			'request': Request(request),
		}
		serialized = CartSerializer(cart, context=serializer_context)
		response_json = JSONRenderer().render(serialized.data)

		return HttpResponse(response_json, status=200)

@csrf_exempt
def get_previous_estimate(request):
	if request.method == 'POST':
		data = json.loads(request.body.decode("utf-8"))
		data = dotdict(data)

		estimate_ref = data.estimate_ref

		estimate_data = estimates.get_estimate(estimate_ref)

		response_json = json.dumps(estimate_data)

		return HttpResponse(response_json, content_type="application/json", status=200)

@csrf_exempt
def email_estimate_pdf(request):
	if request.method == 'POST':
		data = json.loads(request.body.decode("utf-8"))
		data = dotdict(data)

		cart_ref = data.cart_ref

		cart = get_object_or_404(Cart, reference=cart_ref)

		if not cart.freshbooks_id:
			return HttpResponse('No Freshbooks id', status=400)

		pdf_status = estimates.get_estimate_pdf(cart.freshbooks_id)
		
		file_name = "Mibura_SmartSupport_Estimate.pdf"
		path_to_file = '/tmp/' + file_name

		f = open(path_to_file)
		print(f)

		print("cart email", cart.email)

		email_sent = send_quote_email(cart.client.get_full_name(), cart.email, "Mibura Smart Support Quote", path_to_file)
		print('email_sent', email_sent)
		if email_sent:
			return HttpResponse(status=200)

	return HttpResponse(status=400)

@csrf_exempt
def get_estimate_pdf(request):
	if request.method == 'POST':
		data = json.loads(request.body.decode("utf-8"))

		data = dotdict(data)

		if not data.client:
			HttpResponse("No Client ID", status=400)
		
		client = get_object_or_404(Client, pk=int(data.client['pk']))
		cart = get_object_or_404(Cart, reference=data.cart_reference)

		items = []

		for client_prod in cart.products.all():
			items.append({
				**client_prod.__dict__,
				'type': 'product',
				'category': client_prod.product.category,
				'cost': product_price(client_prod, cart.plan, cart.length)
			})

		for cloud in cart.cloud.all():
			items.append({
				'name': cloud.name,
				'type': 'cloud',
				'category': 'cloud',
				'cost': cloud_price(cloud, cart.plan, cart.length)
			})
		
		client.get_freshbooks_id()
		estimate_id = estimates.create_estimate(client.__dict__, cart.plan, cart.length, items)
		
		if cart.freshbooks_id:
			old_cart = deepcopy(cart)
			cart.reference = "replaced"
			cart.replaced = True
			cart.save()

			cart.pk = None
			cart.save()
			cart.replaced = False
			cart.products.add(*old_cart.products.all())
			cart.cloud.add(*old_cart.cloud.all())
			cart.freshbooks_id = estimate_id
			cart.reference = old_cart.reference
			cart.save()
		else:
			cart.freshbooks_id = estimate_id
			cart.save()
		
		pdf_status = estimates.get_estimate_pdf(estimate_id)
		
		file_name = "Mibura_SmartSupport_Estimate.pdf"
		path_to_file = '/tmp/' + file_name
		pdf = FileWrapper(open(path_to_file, 'rb'))

		response = HttpResponse(pdf, content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename=%s' % encoding.smart_str(file_name)
		response['Content-Length'] = os.path.getsize(path_to_file)
		return response
	return HttpResponse('Not POST', status=400)

@csrf_exempt
def checkout(request):
	if request.method == 'POST':
		print("Checkout View")
		data = json.loads(request.body.decode("utf-8"))
		data = dotdict(data)
		print(data)
		client = get_object_or_404(Client, pk=data.client)
		cart = get_object_or_404(Cart, reference=data.cart)
		total = cart.get_total_price()
		print(total)
		stripe_total = math.floor(total*100)
		stripe.Charge.create(
			amount=stripe_total,
			currency="usd",
			source=data.stripe_token, # obtained with Stripe.js
			description="Charge for " + client.email
		)
		time = datetime.now()
		print("time", time)
		sub = Subscription(client=client, plan=cart.plan, length=data.length, price=total, date_begin=time)
		sub.save()
		sub.products.add(*cart.products.all())

		print(data.client)
		print(data.cart)
		print(data.stripe_token)
	return HttpResponse({'result': True}, status=200)

# Django Rest Framework

class CloudViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Cloud.objects.all().order_by('name')
	serializer_class = CloudSerializer

	def get_queryset(self):
		cloud = self.request.query_params.get('cloud', None)
		if cloud:
			queryset = Cloud.objects.filter(name__icontains=cloud)
		else:
			queryset = Cloud.objects.all().order_by('name')
		return queryset


class CategoriesViewSet(viewsets.ReadOnlyModelViewSet):
	"""
	API endpoint that allows products to be viewed or edited.
	"""
	queryset = ProductCategory.objects.all().order_by('-name')
	serializer_class = ProductCategorySerializer
	lookup_field = 'name'

class DiscountViewSet(viewsets.ReadOnlyModelViewSet):
	"""
	API endpoint that allows products to be viewed or edited.
	"""
	queryset = Discount.objects.all().order_by('year_threshold')
	serializer_class = DiscountSerializer
	lookup_field = 'pk'

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
		queryset = Product.objects.all().order_by('-model')
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
