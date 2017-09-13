from datetime import datetime, date, timedelta
from wsgiref.util import FileWrapper
import os, json, math, stripe, plaid
from copy import deepcopy

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone, encoding
from django.template import RequestContext, Context, loader
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from django.db.models import Q

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request

from .models import *
from .serializers import *

from scripts.dotdict import dotdict
from scripts.sss_pricing import product_price, cloud_price
from dynamicscrm.api import createAccount
from freshbooks import estimates

from weasyprint import HTML
import tempfile

stripe.api_key = settings.STRIPE_SECRET_KEY


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

def send_purchasesuccess_email(name, recipient, subject):
	to = [recipient]
	from_email = 'cs@mibura.com'

	print(name)

	ctx = {
		'name': name,
	}

	message = get_template('email/purchase_success.html').render(ctx)
	msg = EmailMessage(subject, message, to=to, from_email=from_email)
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
def plaid_credentials(request):
	# plaid.Client.config({'url': 'https://tartan.plaid.com'})

	if request.method == 'POST':
		data = json.loads(request.body.decode("utf-8"))
		# data = json.loads(request.body)
		data = dotdict(data) # access properties with . instead of []

		plaid_account_id = data.ach_account_id
		plaid_link_public_key = data.ach_public_key
		print("plaid_account_id", plaid_account_id)
		print("plaid_link_public_key", plaid_link_public_key)

		client = plaid.Client(settings.PLAID_CLIENT_ID,
				settings.PLAID_SECRET_KEY,
				settings.PLAID_PUBLIC_KEY,
				'sandbox')
		print("client", client.__dict__)
		exchange_token_response = client.Item.public_token.exchange(plaid_link_public_key)
		print("exchange_token_response", exchange_token_response)
		access_token = exchange_token_response['access_token']
		stripe_response = client.Processor.stripeBankAccountTokenCreate(access_token, plaid_account_id)
		bank_account_token = stripe_response['stripe_bank_account_token']

		return HttpResponse(bank_account_token, status=200)


	return HttpResponse("failed", status=400)

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

		# if not data.client:
			# HttpResponse("No Client ID", status=400)

		client = get_object_or_404(Client, pk=data.client)

		# client = Client.objects.get(pk=data.client)
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
					prod_obj = Product(brand=prod.brand, model=prod.model, category=cat, sku='NONE', approved=False, release=date.today() - timedelta(1))
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

def estimate_pdf(request):
	"""Generate pdf."""
	# Model data
	# people = Person.objects.all().order_by('last_name')
	if request.method == 'GET':
		data = json.loads(request.body.decode("utf-8"))

		data = dotdict(data)

	cart = get_object_or_404(Cart, pk=data.cart_id)

	template = loader.get_template('accounting/estimate.html')

	context = {'cart': cart}

	html = template.render(request=request, context=context)

	# Rendered
	# html_string = render_to_string('accounting/estimate.html', context)
	# html = HTML(string=html_string)
	# result = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()


	# result = html.write_pdf()


	# Creating http response
	response = HttpResponse(content_type='application/pdf;')

	# Try
	HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response)

	response['Content-Disposition'] = 'inline; filename=MiburaEstimate.pdf'
	response['Content-Transfer-Encoding'] = 'binary'
	# with tempfile.NamedTemporaryFile(delete=True) as output:
	# 	output.write(result)
	# 	output.flush()
	# 	# output = open(output.name, 'r', "utf-8")
	# 	output = open(output.name, mode='rb', encoding=None, buffering=1)
	# 	response.write(output.read())
	return response

@csrf_exempt
def get_estimate_pdf(request):
	if request.method == 'POST':
		data = json.loads(request.body.decode("utf-8"))

		data = dotdict(data)
		
		client = get_object_or_404(Client, pk=int(data.client['pk']))
		cart = get_object_or_404(Cart, reference=data.cart_reference)
		discount_list = Discount.objects.all()
		plan_obj = Plan.objects.get(short_name=cart.plan)
		categories = ProductCategory.objects.all()

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

		active_discount = 0.0

		for index, dis in enumerate(discount_list):
			if float(length) >= dis.year_threshold:
				if dis.discount_percent > active_discount:
					active_discount = dis.discount_percent


		line_items = []
		for index,item in enumerate(items):
			line_item = {

			}
			cat = categories.get(category_code=item['category'])

			if item['type'] == 'product':
				estimate_text = EstimateText.objects.get(plan=plan_obj, category=cat)
				desc = estimate_text.description.replace('[product]', item['brand'] + " " + item['model']).replace('[length]', str(cart.length) + ' years.')

			elif item['type'] == 'cloud':
				cloud = Cloud.objects.get(name=item['name'])
				desc = estimate_text.description

			line_item['name'] = estimate_text.item
			line_item['description'] = desc
			line_item['unit_cost'] = {
				'amount': str(round(item['cost'], 2)),
				'code': 'USD'
			}
			line_item['qty'] = 1
			line_item['type'] = 0

			line_items.append(line_item)
		
		client.get_freshbooks_id()

		terms = 'Estimate for ' + cart.plan + ' plan for ' + str(cart.length) + ' years.'
		notes = 'Mibura Smart Support Estimate'
		estimate_id = estimates.create_estimate(client.__dict__, cart.plan, cart.length, line_items, active_discount, terms, notes)
		
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
		
		# pdf_status = estimates.get_estimate_pdf(estimate_id)

		template = loader.get_template('accounting/estimate.html')
		context = {
			'items': line_items,
			'client': client,
			'cart': cart,
			'terms': terms,
			'notes': notes
		}
		html = template.render(request=request, context=context)
		response = HttpResponse(content_type='application/pdf;')

		HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response)

		response['Content-Disposition'] = 'inline; filename=MiburaEstimate.pdf'
		response['Content-Transfer-Encoding'] = 'binary'
		return response
		
		# file_name = "Mibura_SmartSupport_Estimate.pdf"
		# path_to_file = '/tmp/' + file_name
		# pdf = FileWrapper(open(path_to_file, 'rb'))

		# response = HttpResponse(pdf, content_type='application/pdf')
		# response['Content-Disposition'] = 'attachment; filename=%s' % encoding.smart_str(file_name)
		# response['Content-Length'] = os.path.getsize(path_to_file)
		# return response
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

		discount_list = Discount.objects.all()

		active_discount = 0.0

		for index, dis in enumerate(discount_list):
			if float(cart.length) >= dis.year_threshold:
				if dis.discount_percent > active_discount:
					active_discount = dis.discount_percent
		
		discount_total = total - total*active_discount
		stripe_total = math.floor(discount_total*100)
		stripe.Charge.create(
			amount=stripe_total,
			currency="usd",
			source=data.stripe_token, # obtained with Stripe.js
			description="SSS " + cart.plan + " purchase for " + client.email + ", length: " + str(cart.length) + " years."
		)
		time = datetime.now()
		sub = Subscription(
			client=client, 
			plan=cart.plan, 
			length=data.length,
			discount_percent=active_discount,
			cart=cart,
			subtotal=total,
			price=discount_total, 
			date_begin=time)
		sub.save()
		sub.products.add(*cart.products.all())
		sub.cloud.add(*cart.cloud.all())

		crm_res = createAccount({
			"company": client.company,
			"phone": client.phone,
			"email": client.email,
			"client_name": client.get_full_name(),
			"address1": client.street,
			"address2": client.street2,
			"city": client.city,
			"state": client.state,
			"zipcode": client.zipcode,
			"country": client.country,
			"description": "Smart Support " + cart.plan + " for " + str(cart.length) + " years. Django Subscription ID for product reference: " + str(sub.pk)
		})
		send_purchasesuccess_email(client.get_full_name(), client.email, "Your New Smart Support Purchase")
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
		queryset = Product.objects.order_by('-model')
		query_str = self.request.query_params.get('s', None)
		# model = self.request.query_params.get('model', None)
		if query_str:
			for i in query_str.split(' '):
				# queryset = queryset.filter(brand__icontains=brand)
				queryset = queryset.filter(Q(brand__icontains=i) | Q(model__icontains=i))
				# if not model:
				# 	items, item_ids = [], []
				# 	for item in queryset:
				# 		if item.brand not in item_ids:
				# 			items.append(item)
				# 			item_ids.append(item.brand)
				# 			queryset = items
		
		return queryset

# @api_view(['GET', 'POST'])
# def support_cart_create(request):
# 	"""
# 	List all snippets, or create a new snippet.
# 	"""
# 	if request.method == 'GET':
# 		snippets = Product.objects.all()
# 		serializer = SnippetSerializer(snippets, many=True)
# 		return Response(serializer.data)

# 	elif request.method == 'POST':
# 		serializer = SnippetSerializer(data=request.data)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return Response(serializer.data, status=status.HTTP_201_CREATED)
# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
