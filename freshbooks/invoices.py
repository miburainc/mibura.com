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

try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET

def create_invoice(client, plan, length, items):
	discount_list = Discount.objects.all()
	plan_obj = Plan.objects.get(short_name=plan)
	categories = ProductCategory.objects.all()

	active_discount = 0.0

	for index, dis in enumerate(discount_list):
		if float(length) >= dis.year_threshold:
			if dis.discount_percent > active_discount:
				active_discount = dis.discount_percent

	tree = ET.ElementTree(file='freshbooks/xml_templates/create_invoice.xml')
	root = tree.getroot()
	invoice = root[0]

	clientid = invoice.find('client_id')
	clientid.text = str(client['freshbooks_id'])

	discount = invoice.find('discount')
	discount.text = str(int(active_discount*100))

	terms = invoice.find('terms')
	terms.text = 'Invoice for ' + plan + ' plan for ' + str(length) + ' years.'

	first_name = invoice.find('first_name')
	first_name.text = client['first_name']

	last_name = invoice.find('last_name')
	last_name.text = client['last_name']

	organization = invoice.find('organization')
	organization.text = client['company']

	street1 = invoice.find('p_street1')
	street1.text = client['street']

	street2 = invoice.find('p_street2')
	if client['street2']:
		street2.text = client['street2']
	else:
		invoice.remove(street2)

	city = invoice.find('p_city')
	city.text = client['city']

	state = invoice.find('p_state')
	state.text = client['state']

	country = invoice.find('p_country')
	country.text = client['country']

	zipcode = invoice.find('p_code')
	zipcode.text = str(client['zipcode'])

	lines = invoice.find('lines')

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
			print("NAME", item['name'])
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
	invoice_id = root[0]
	return invoice_id.text