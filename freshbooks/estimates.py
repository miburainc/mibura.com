from django.conf import settings
from django.utils import timezone
from django.utils.dateformat import DateFormat

import sys, requests, json
from datetime import datetime

from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request

from .models import *
from support.models import *
from support.serializers import ClientSerializer, CartSerializer, CloudSerializer, ProductSerializer


def create_estimate(client, plan, length, items, discount, terms, notes):
	freshbooks_auth = FreshbooksAuth.objects.get(pk=1)

	payload = {
		'estimate': {
			'email': client['email'],
			'create_date': DateFormat(datetime.now()).format('Y-m-d'),
			'customerid': client['freshbooks_id'],
			'discount_value': str(discount*100),
			'terms': terms,
			'notes': notes,
			'fname': client['first_name'],
			'lname': client['last_name'],
			'organization': client['company'],
			'street': client['street'],
			'street2': client['street2'],
			'city': client['city'],
			'state': client['state'],
			'country': client['country'],
			'code': str(client['zipcode']),
			'lines': items
		}
	}

	url = "https://api.freshbooks.com/accounting/account/VY6wd/estimates/estimates"
	headers = {'Authorization': 'Bearer ' + freshbooks_auth.get_auth_token(), 'Api-Version': 'alpha', 'Content-Type': 'application/json'}

	res = requests.post(url, data=json.dumps(payload), headers=headers)
	print(res)
	print(res.content)
	json_response = res.json()

	if res.status_code == 200:
		return json_response['response']['result']['estimate']
	else:
		return False

def list_estimates(page):
	url = "https://api.freshbooks.com/accounting/account/VY6wd/estimates/estimates?page=" + str(page)
	headers = {'Authorization': 'Bearer ' + freshbooks_auth.get_auth_token(), 'Api-Version': 'alpha', 'Content-Type': 'application/json'}
	
	res = request.get(url, data=None, headers=headers)
	json_response = res.json()
	estimates = json_response['response']['result']['estimates']

	return estimates

def process_estimates(estimates, estimate_num):
	response = {}
	for estimate in estimates:
		estimate_id = str(int(estimate.find('estimate_id').text))
		num = estimate.find('number')
		if num.text == estimate_num:
			client_id = estimate.find('client_id').text
			client = Client.objects.get(freshbooks_id=client_id)

			serialized = ClientSerializer(client)
			response_json = JSONRenderer().render(serialized.data)

			response['client'] = serialized.data

			lines = estimate.find('lines')
			response['cart_items'] = []
			cart = Cart.objects.get(freshbooks_id=estimate_id)
			
			serialized = CartSerializer(cart)
			response_json = JSONRenderer().render(serialized.data)
			response['cart'] = serialized.data

			for item in cart.products.all():
				serialized = ProductSerializer(item.product)
				response_json = JSONRenderer().render(serialized.data)
				if not item.additional_info:
					item.additional_info = ""
				
				prod_info = serialized.data#json.load(response_json)

				clientprod_info = {
					"serial_number": item.serial_number,
					"device_age": item.device_age,
					"additional_info": item.additional_info
				}
				# final_json = {key: value for (key, value) in (prod_info.items() + clientprod_info.items())}
				# final_json = prod_info.update(clientprod_info)
				final_json = {
					**clientprod_info,
					**prod_info
				}
				response['cart_items'].append(final_json)
			for cloud in cart.cloud.all():
				serialized = CloudSerializer(cloud)
				final_obj = {
					**serialized.data,
					"category": {
						"category_code": "cloud",
						"name": "Cloud"
					}
				}
				response['cart_items'].append(final_obj)
	return response

def get_estimate(estimate_num):
	estimates = list_estimates()
	estimate_list_current_page = estimates.attrib['page']
	estimate_list_pages = estimates.attrib['pages']
	for page_index in range(1,int(estimate_list_pages)+1):
		if int(estimate_list_current_page) == page_index:
			response = process_estimates(estimates.findall('estimate'), estimate_num)
			if response != {}:
				break
		else:
			# Get next page
			xml_page_num = root.find('page')
			xml_page_num.text = str(page_index)

			input_xml = ET.tostring(root)

			data = input_xml
			headers = {'Content-Type': 'application/xml'}
			r = requests.get(settings.FRESHBOOKS_URL, auth=(settings.FRESHBOOKS_AUTH, ''), headers=headers, data=data)

			response = {}

			response_root = ET.fromstring(r.content)	

			remove_namespace(response_root, u'http://www.freshbooks.com/api/')

			estimates = response_root[0]

			response = process_estimates(estimates.findall('estimate'), estimate_num)
			if response != {}:
				break

	return response


def find_estimate(client_id, estimate_reference_number):
	"""  """
	tree = ET.ElementTree(file='freshbooks/xml_templates/list_estimates.xml')
	root = tree.getroot()
	_id = root.find('client_id')
	_id.text = client_id
	input_xml = ET.tostring(root)

	data = input_xml
	headers = {'Content-Type': 'application/xml'}
	r = requests.get(settings.FRESHBOOKS_URL, auth=(settings.FRESHBOOKS_AUTH, ''), headers=headers, data=data)
	# print(r)
	root = ET.fromstring(r.content)
	estimates = root[0]
	for e in estimates:
		print(e)
		e_num = e.find('{http://www.freshbooks.com/api/}number').text
		estimate_id = e.find('{http://www.freshbooks.com/api/}estimate_id').text
		if e_num == estimate_reference_number:
			# response = {
			# 	'client_id': client_id,
			# }
			return estimate_id