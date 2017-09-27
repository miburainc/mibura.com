from django.conf import settings
from django.utils import timezone
from django.utils.dateformat import DateFormat

import sys, requests, json, re
from datetime import datetime

from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request

from .models import *
from support.models import *
from support.serializers import ClientSerializer, CartSerializer, CloudSerializer, ProductSerializer

try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET

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
	clientid.text = str(client['freshbooks_id'])

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
		print("CATEGORY!!!!!",cat)
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
		elif item['type'] == 'unknown':
			text = EstimateText.objects.get(plan=plan_obj, category=cat)
			name.text = text.item
			desc = text.description.replace('[product]', item['model']).replace('[length]', str(length) + ' years.')

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
			return estimate_id
	return False

def get_estimate_pdf(estimate_id):
	tree = ET.ElementTree(file='freshbooks/xml_templates/get_estimate_pdf.xml')
	root = tree.getroot()
	_id = root[0]
	_id.text = str(estimate_id)

	input_xml = ET.tostring(root)
	data = input_xml
	headers = {'Content-Type': 'application/xml'}
	r = requests.get(settings.FRESHBOOKS_URL, auth=(settings.FRESHBOOKS_AUTH, ''), headers=headers, data=data, stream=True)
	
	r.raise_for_status()


	file_name = "Mibura_SmartSupport_Estimate.pdf"
	path_to_file = settings.MEDIA_ROOT + file_name
	with open(path_to_file, 'wb') as f:
		f.write(r.content)
	# with open(path_to_file, 'wb') as f:
		# for chunk in r.iter_content(1024):
			# f.write(chunk)
	pdf = open(path_to_file, 'rb')
	return pdf #open(path_to_file, 'r')


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

def find_estimate(estimate_reference_number):
	"""  """
	tree = ET.ElementTree(file='freshbooks/xml_templates/list_estimates.xml')
	root = tree.getroot()
	input_xml = ET.tostring(root)

	data = input_xml
	headers = {'Content-Type': 'application/xml'}
	r = requests.get(settings.FRESHBOOKS_URL, auth=(settings.FRESHBOOKS_AUTH, ''), headers=headers, data=data)
	# print(r)
	root = ET.fromstring(r.content)
	estimates = root[0]
	for e in estimates:
		e_num = e.find('{http://www.freshbooks.com/api/}number').text
		estimate_id = e.find('{http://www.freshbooks.com/api/}estimate_id').text
		if e_num == estimate_reference_number:
			# response = {
			# 	'client_id': client_id,
			# }
			print('ID', e_num)
			print(estimate_id)
			return estimate_id