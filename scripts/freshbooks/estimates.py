from django.conf import settings

import sys
import requests

try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET

def create_estimate(client, plan, length, items):
	tree = ET.ElementTree(file='scripts/freshbooks/xml_templates/estimate_template.xml')
	root = tree.getroot()
	estimate = root[0]

	status = ET.SubElement(estimate, 'status')

	clientid = estimate.find('client_id')
	clientid.text = client['id']

	terms = estimate.find('terms')
	terms.text = 'Estimate for ' + plan + ' plan for ' + length + ' years.'

	first_name = estimate.find('first_name')
	first_name.text = client['first_name']

	last_name = estimate.find('last_name')
	last_name.text = client['last_name']

	organization = estimate.find('organization')
	organization.text = client['company']

	street1 = estimate.find('p_street1')
	street1.text = client['street1']

	street2 = estimate.find('p_street2')
	street2.text = client['street2']

	city = estimate.find('p_city')
	city.text = client['city']

	state = estimate.find('p_state')
	state.text = client['state']

	country = estimate.find('p_country')
	country.text = client['country']

	zipcode = estimate.find('p_code')
	zipcode.text = client['zipcode']

	lines = estimate.find('lines')

	for index,item in enumerate(items):
		print(item['name'])
		line = ET.Element('line')
		name = ET.SubElement(line, 'name')
		name.text = item['brand'] + ' ' + item['model']
		description = ET.SubElement(line, 'description')
		desc = 'SN: ' + item['serial_number'] + '\nAge: ' + item['age'] 
		description.text = desc
		unit_cost = ET.SubElement(line, 'unit_cost')
		unit_cost.text = item['cost']
		quantity = ET.SubElement(line, 'quantity')
		quantity.text = '1'
		_type = ET.SubElement(line, 'type')
		_type.text = item['type']
		lines.extend((line,))

	return ET.tostring(root)

def get_estimate_pdf(estimate_id):
	tree = ET.ElementTree(file='scripts/freshbooks/xml_templates/get_estimate_pdf.xml')
	root = tree.getroot()
	_id = root[0]
	_id.text = estimate_id

	input_xml = ET.tostring(root)
	data = input_xml
	headers = {'Content-Type': 'application/xml'}
	r = requests.get(settings.FRESHBOOKS_URL, auth=(settings.FRESHBOOKS_AUTH, ''), headers=headers, data=data)
	# print(r)
	return r.content

def list_estimates(client_id):
	tree = ET.ElementTree(file='scripts/freshbooks/xml_templates/list_estimates.xml')
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

def find_estimate(client_id, estimate_reference_number):
	"""  """
	tree = ET.ElementTree(file='scripts/freshbooks/xml_templates/list_estimates.xml')
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



