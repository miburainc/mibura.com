from django.conf import settings

import sys, requests, json

from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request

try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET

from support.models import *
from support.serializers import ClientSerializer, CartSerializer, CloudSerializer, ProductSerializer

def remove_namespace(doc, namespace):
	"""Remove namespace in the passed document in place."""
	ns = u'{%s}' % namespace
	nsl = len(ns)
	for elem in doc.getiterator():
		if elem.tag.startswith(ns):
			elem.tag = elem.tag[nsl:]

def create_estimate(client, plan, length, items):
	discount_list = Discount.objects.all()
	plan_obj = Plan.objects.get(short_name=plan)
	categories = ProductCategory.objects.all()

	active_discount = 0.0

	for index, dis in enumerate(discount_list):
		if float(length) >= dis.year_threshold:
			if dis.discount_percent > active_discount:
				active_discount = dis.discount_percent


	tree = ET.ElementTree(file='freshbooks/xml_templates/create_estimate.xml')
	root = tree.getroot()
	estimate = root[0]

	clientid = estimate.find('client_id')
	clientid.text = client['freshbooks_id']

	discount = estimate.find('discount')
	discount.text = str(int(active_discount*100))

	terms = estimate.find('terms')
	terms.text = 'Estimate for ' + plan + ' plan for ' + str(length) + ' years.'

	first_name = estimate.find('first_name')
	first_name.text = client['first_name']

	last_name = estimate.find('last_name')
	last_name.text = client['last_name']

	organization = estimate.find('organization')
	organization.text = client['company']

	street1 = estimate.find('p_street1')
	street1.text = client['street']

	street2 = estimate.find('p_street2')
	if client['street2']:
		street2.text = client['street2']
	else:
		estimate.remove(street2)

	city = estimate.find('p_city')
	city.text = client['city']

	state = estimate.find('p_state')
	state.text = client['state']

	country = estimate.find('p_country')
	country.text = client['country']

	zipcode = estimate.find('p_code')
	zipcode.text = str(client['zipcode'])

	lines = estimate.find('lines')

	for index,item in enumerate(items):
		print("item type:",item['type'])
		print(item)
		cat = categories.get(category_code=item['category'])
		line = ET.Element('line')
		name = ET.SubElement(line, 'name')
		description = ET.SubElement(line, 'description')
		if item['type'] == 'product':
			text = EstimateText.objects.get(plan=plan_obj, category=cat)
			name.text = text.item
			desc = text.description.replace('[product]', item['brand'] + " " + item['model']).replace('[length]', str(length) + ' years.')
		elif item['type'] == 'cloud':
			cloud = Cloud.objects.get(name=item['name'])
			print("cloud: ",cloud)
			text = EstimateText.objects.get(category=cat, cloud=cloud)
			name.text = text.item
			desc = text.description
		description.text = desc
		unit_cost = ET.SubElement(line, 'unit_cost')
		unit_cost.text = str(round(item['cost'], 2))
		quantity = ET.SubElement(line, 'quantity')
		quantity.text = '1'
		_type = ET.SubElement(line, 'type')
		_type.text = 'item'# item['type']
		lines.extend((line,))

	data = ET.tostring(root)

	headers = {'Content-Type': 'application/xml'}
	r = requests.post(settings.FRESHBOOKS_URL, auth=(settings.FRESHBOOKS_AUTH, ''), headers=headers, data=data)
	root = ET.fromstring(r.content)
	estimate_id = root[0]
	return estimate_id.text

def get_estimate_pdf(estimate_id):
	tree = ET.ElementTree(file='freshbooks/xml_templates/get_estimate_pdf.xml')
	root = tree.getroot()
	_id = root[0]
	_id.text = str(estimate_id)

	input_xml = ET.tostring(root)
	data = input_xml
	headers = {'Content-Type': 'application/xml'}
	r = requests.get(settings.FRESHBOOKS_URL, auth=(settings.FRESHBOOKS_AUTH, ''), headers=headers, data=data)
	# print(r)
	file_name = "Mibura_SmartSupport_Estimate.pdf"
	path_to_file = '/tmp/' + file_name
	with open(path_to_file, 'wb') as f:
		f.write(r.content)

	return r.content

def list_estimates(client_id):
	tree = ET.ElementTree(file='freshbooks/xml_templates/list_estimates.xml')
	root = tree.getroot()
	_id = root.find('estimate_id')
	_id.text = client_id
	input_xml = ET.tostring(root)

	data = input_xml
	headers = {'Content-Type': 'application/xml'}
	r = requests.get(settings.FRESHBOOKS_URL, auth=(settings.FRESHBOOKS_AUTH, ''), headers=headers, data=data)
	# print(r)
	print(r.content)
	print('\n')
	root = ET.fromstring(r.content)
	print(root)
	estimates = root[0]
	print(estimates)
	for e in estimates:
		print('estimate_id', e.find('{http://www.freshbooks.com/api/}estimate_id').text)

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
	tree = ET.ElementTree(file='freshbooks/xml_templates/list_estimates.xml')
	root = tree.getroot()

	# Remove client id filter from list_estimates.xml
	cid = root.find('client_id')
	root.remove(cid)

	input_xml = ET.tostring(root)

	data = input_xml
	headers = {'Content-Type': 'application/xml'}
	r = requests.get(settings.FRESHBOOKS_URL, auth=(settings.FRESHBOOKS_AUTH, ''), headers=headers, data=data)

	response = {}

	response_root = ET.fromstring(r.content)	

	remove_namespace(response_root, u'http://www.freshbooks.com/api/')

	estimates = response_root[0]
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