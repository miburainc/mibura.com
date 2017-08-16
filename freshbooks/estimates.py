from django.conf import settings

import sys, requests

try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET

from support.models import *

def create_estimate(client, plan, length, items):
	plan_obj = Plan.objects.get(short_name=plan)
	categories = ProductCategory.objects.all()

	tree = ET.ElementTree(file='freshbooks/xml_templates/create_estimate.xml')
	root = tree.getroot()
	estimate = root[0]

	clientid = estimate.find('client_id')
	clientid.text = client['freshbooks_id']

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

def get_estimate(estimate_id):
	tree = ET.ElementTree(file='freshbooks/xml_templates/get_estimate.xml')
	root = tree.getroot()
	eid = root.find('estimate_id')
	eid.text = estimate_id
	input_xml = ET.tostring(root)

	data = input_xml
	headers = {'Content-Type': 'application/xml'}
	r = requests.get(settings.FRESHBOOKS_URL, auth=(settings.FRESHBOOKS_AUTH, ''), headers=headers, data=data)
	# print(r)
	root = ET.fromstring(r.content)
	return True


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